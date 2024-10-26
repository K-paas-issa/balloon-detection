from sqlalchemy import Column, BIGINT, DOUBLE, String, BOOLEAN, INT
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BalloonReport(Base):
    __tablename__ = "balloon_report"

    id = Column(BIGINT, nullable=False, primary_key=True)
    center_latitude = Column(DOUBLE, nullable=False)
    center_longitude = Column(DOUBLE, nullable=False)
    is_checked_status = Column(BOOLEAN, nullable=False)
    reported_latitude = Column(DOUBLE, nullable=False)
    reported_longitude = Column(DOUBLE, nullable=False)
    serial_code = Column(String, nullable=False)
    street_address = Column(String, nullable=False)
    image_path = Column(String, nullable=False)

class CityDistrict(Base):
    __tablename__ = "city_district"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    code = Column(String(15), nullable=False, unique=True)
    city = Column(String(10), nullable=False)
    district = Column(String(20), nullable=False)
    country = Column(String(20), nullable=False)
    latitude = Column(DOUBLE, nullable=False)
    longitude = Column(DOUBLE, nullable=False)