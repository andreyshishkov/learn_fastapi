from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid


Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    title = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    count = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
