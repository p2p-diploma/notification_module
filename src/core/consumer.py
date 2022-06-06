import enum
import time

import orjson
from redis import Redis, exceptions
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from core.config import app_settings
from core.configs import service_logger
from db.session import async_session
from schemas.notification import NotificationCreate

key: str = "transaction_status_changed"
group: str = "transaction-notification-group"

redis = Redis(host=app_settings.REDIS_HOST, port=6379)


class TransactionStatus(enum.Enum):
    CREATED = 10
    ON_PAYMENT_WAIT = 20
    ON_APPROVE = 30
    EXPIRED = 40
    SUCCESS = 50
    CANCELED = 99


async def _proceed_transaction_notification(
    result: list,  # type: ignore
):
    obj = result[1][0][1]
    obj = orjson.loads(obj[b"data"])
    status = TransactionStatus(obj["status"])
    title = "Your trade status changed!"
    message = ""
    receivers = []

    if status == TransactionStatus.ON_PAYMENT_WAIT:
        receivers = [obj["buyer_email"]]
        message = f"Please, approve payment and proceed trade!\nTrade Link: {app_settings.SERVICE_API}/lots/{obj['lot_id']}{obj['id']}"

    if status == TransactionStatus.ON_APPROVE:
        receivers = [obj["seller_email"]]
        message = f"Please, approve payment and proceed trade!" \
                  f"\nTrade Link: {app_settings.SERVICE_API}/lots/{obj['lot_id']}{obj['id']}"

    if status == TransactionStatus.SUCCESS:
        receivers = [obj["seller_email"], obj["buyer_email"]]
        message = f"Your trade successfully proceeded\nTrade Link: {app_settings.SERVICE_API}/lots/{obj['lot_id']}{obj['id']}"

    if status == TransactionStatus.EXPIRED:
        receivers = [obj["buyer_email"]]
        message = f"Your trade is expired\nTrade Link: {app_settings.SERVICE_API}/lots/{obj['lot_id']}{obj['id']}"

    description = f"""
        New status: {TransactionStatus(obj['status']).name}
        {message}
    """.strip()

    for receiver in receivers:
        notif = NotificationCreate(title=title, description=description, owner=receiver)
        async with async_session() as db:
            _ = await crud.notifications.create(db, obj_in=notif)


async def start_consuming():
    try:
        redis.xgroup_create(key, group)
    except exceptions.ResponseError:
        service_logger.info("Group is already exists!")

    while True:
        try:
            results = redis.xreadgroup(group, key, {key: ">"}, None)
            if results:
                for result in results:
                    await _proceed_transaction_notification(result)

        except Exception as e:
            print(str(e))

        time.sleep(3)
