from typing import List, Dict

import telebot
from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy import exists
from sqlalchemy.orm import Session

from app.core.config import TG_TOKEN, TG_ID
from app.dependencies.database.database import get_db
from app.models.order import Order
from app.models.status import Status
from app.schemas.order_schema import OrderSchema

Order_router = APIRouter(tags=['Orders Routers'], prefix='/order')

bot = telebot.TeleBot(TG_TOKEN)


@Order_router.post("/submit/")
async def submit_order(order_data: OrderSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    waiting_status_exists = db.query(exists().where(Status.name == "Waiting")).scalar()
    if not waiting_status_exists:
        waiting_status = Status(name="Waiting")
        db.add(waiting_status)
        db.commit()

    new_order = Order(name=order_data.name, phone=order_data.phone, product=order_data.product, link=order_data.link)

    waiting_status = db.query(Status).filter(Status.name == "Waiting").first()
    new_order.status = waiting_status

    db.add(new_order)
    db.commit()

    order_message = f"Новый заказ:\nИмя: {order_data.name}\nНомер телефона: {order_data.phone}\nТовар: {order_data.product}\nСсылка на poizon: {order_data.link}"
    background_tasks.add_task(send_telegram_message, order_message)

    return {"message": "Заказ успешно отправлен"}


def send_telegram_message(message):
    bot.send_message(TG_ID, message)


class StatusSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    id: int
    name: str
    phone: str
    product: str
    status_id: int
    link: str

    class Config:
        from_attributes = True


@Order_router.get("/orders/", response_model=List[OrderSchema])
async def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return [{
        "id": order.id,
        "name": order.name,
        "phone": order.phone,
        "product": order.product,
        "status_id": order.status_id,
        "link": order.link
    } for order in orders]


@Order_router.post("/status/create/", response_model=StatusSchema)
async def create_status(name: str, db: Session = Depends(get_db)):
    existing_status = db.query(Status).filter(Status.name == name).first()
    if existing_status:
        return {"message": f"Статус с именем {name} уже существует"}

    new_status = Status(name=name)
    db.add(new_status)
    db.commit()
    db.refresh(new_status)

    return new_status


@Order_router.get("/statuses/", response_model=List[StatusSchema])
async def get_statuses(db: Session = Depends(get_db)):
    return db.query(Status).all()


@Order_router.put("/order/{order_id}/status/{status_id}")
async def update_order_status(order_id: int, status_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        status = db.query(Status).filter(Status.id == status_id).first()
        if status:
            order.status = status
            db.commit()
            return {"message": "Статус заказа успешно обновлен"}
        return {"message": "Статус с указанным ID не найден"}, 404
    return {"message": "Заказ с указанным ID не найден"}, 404


@Order_router.get("/orders/status/{status_id}", response_model=List[OrderSchema])
async def get_orders_by_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(Status).filter(Status.id == status_id).first()
    if status:
        return status.orders
    return {"message": "Статус с указанным ID не найден"}, 404


@Order_router.get("/orders/ten_per_status", response_model=Dict[str, List[OrderSchema]])
async def get_first_ten_orders_per_status(db: Session = Depends(get_db)):
    statuses = db.query(Status).all()
    result = {}
    for status in statuses:
        result[status.name] = status.orders[:10] if status.orders else []
    return result

# @Order_router.delete("/clear_tables/")
# async def clear_tables(db: Session = Depends(get_db)):
#     try:
#         db.query(Order).delete()
#
#         db.query(Status).delete()
#
#         db.commit()
#
#         return {"message": "Таблицы успешно очищены"}
#     except Exception as e:
#         return {"error": str(e)}
