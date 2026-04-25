from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:1@db:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)


def init_db():
    Base.metadata.create_all(engine)

    session = SessionLocal()

    try:
        if not session.query(Device).first():
            devices = [
                Device(name="Futbolkalar", category="clothes"),
                Device(name="Shimlar", category="clothes"),
                Device(name="Smartfonlar", category="electronics"),
                Device(name="Noutbuklar", category="electronics"),
                Device(name="Non mahsulotlari", category="food"),
                Device(name="Shirinliklar", category="food"),
            ]
            session.add_all(devices)
            session.commit()
    finally:
        session.close()


def get_devices_by_category(category):
    session = SessionLocal()
    try:
        devices = session.query(Device).filter(Device.category == category).all()
        return [d.name for d in devices]
    finally:
        session.close()