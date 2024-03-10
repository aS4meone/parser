import telebot
from fastapi import APIRouter

from app.core.config import TG_TOKEN, TG_ID
from app.schemas.order_schema import OrderSchema

Order_router = APIRouter(tags=['Orders Routers'], prefix='/order')

bot = telebot.TeleBot(TG_TOKEN)


@Order_router.post("/submit/")
async def submit_order(order_data: OrderSchema):
    order_message = f"Новый заказ:\nИмя: {order_data.name}\nНомер телефона: {order_data.phone}\nТовар: {order_data.product}"
    bot.send_message(TG_ID, order_message)

    return {"message": "Заказ успешно отправлен"}
