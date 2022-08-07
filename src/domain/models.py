from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

from src.adapters.orm import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True, server_default="true")


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    tax_id = Column(String, nullable=True)
    name = Column(String, nullable=False)
    legal_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    active = Column(Boolean, default=True, server_default="true")
    created_at = Column(DateTime, default=func.now(), server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    country = relationship("Country", back_populates="stores")


class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True, server_default="true")


class Worker(Base):
    __tablename__ = "workers"

    user_id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"), primary_key=True)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    store = relationship("Store", back_populates="workers")
    rol = relationship("Rol", back_populates="workers")
