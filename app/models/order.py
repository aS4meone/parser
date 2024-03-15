from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.dependencies.database.database import Base
from app.schemas.order_schema import OrderSchema


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, index=True)
    product = Column(String)
    status_id = Column(Integer, ForeignKey('statuses.id'))
    status = relationship("Status", back_populates="orders")
    link = Column(String)


def submit_order(order_data: OrderSchema, db_session):
    order = Order(name=order_data.name, phone=order_data.phone, product=order_data.product, link=order_data.link)
    db_session.add(order)
    db_session.commit()
    return order
