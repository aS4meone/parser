from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.dependencies.database.database import Base


class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    orders = relationship("Order", back_populates="status")
