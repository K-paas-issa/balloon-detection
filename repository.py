from dbutils import engineconn
from db_models import BalloonReport, CityDistrict
from sqlalchemy.orm import Session
from sqlalchemy import and_

engine_conn = engineconn()

def findById(id):
    try:
        session: Session = engine_conn.get_session()
        reported_balloon = session.query(BalloonReport).filter(BalloonReport.id == id).first()
        if not reported_balloon:
            raise Exception("존재하지 않는 풍선입니다.")
        return reported_balloon
    except Exception as e:
        print(str(e))
        return str(e)
    finally:
        session.close()
    
def updateStatusFalse(id):
    try:
        session: Session = engine_conn.get_session()
        reported_balloon = session.query(BalloonReport).filter(BalloonReport.id == id).first()
        if not reported_balloon:
            raise Exception("존재하지 않는 풍선입니다.")
        reported_balloon.is_checked_status = False
        session.commit()
        session.refresh(reported_balloon)
        print('update false success')
        return
    except Exception as e:
        print(str(e))
        return str(e)
    finally:
        session.close()

def updateReportedBalloon(id, city_district: CityDistrict):
    try:
        session: Session = engine_conn.get_session()
        reported_balloon = session.query(BalloonReport).filter(BalloonReport.id == id).first()
        if not reported_balloon:
            raise Exception("존재하지 않는 풍선입니다.")
        
        reported_balloon.is_checked_status = True
        reported_balloon.center_latitude = city_district.latitude
        reported_balloon.center_longitude = city_district.longitude
        reported_balloon.street_address = f"{city_district.city} {city_district.district}"

        session.commit()
        session.refresh(reported_balloon)
        print('update success')
        return True
    except Exception as e:
        print(str(e))
        return str(e)
    finally:
        session.close()

def findByOnlyDistrict(district1, district2):
    try:
        session: Session = engine_conn.get_session()
        return session.query(CityDistrict).filter(
                and_(
                    CityDistrict.district.like(f"%{district1}%"),
                    CityDistrict.district.like(f"%{district2}%"),
                )
            ).all()
    finally:
        session.close()


def findByCityAndDistrict(city, district):
    try:
        session: Session = engine_conn.get_session()
        return session.query(CityDistrict).filter(
                and_(
                    CityDistrict.city.like(f"%{city}%"),
                    CityDistrict.district.like(f"%{district}%"),
                )
            ).all()
    finally:
        session.close()

def findByCity(city):
    try:
        session: Session = engine_conn.get_session()
        return session.query(CityDistrict).filter(
                CityDistrict.city.like(f"%{city}%")
            ).all()
    finally:
        session.close()

def findByDistrict(district):
    try:
        session: Session = engine_conn.get_session()
        return session.query(CityDistrict).filter(
                CityDistrict.district.like(f"%{district}%")
            ).all()
    finally:
        session.close()

def findByCityAndDistricts(city, district1, district2):
    try:
        session: Session = engine_conn.get_session()
        return session.query(CityDistrict).filter(
                and_(
                    CityDistrict.city.like(f"%{city}%"),
                    CityDistrict.district.like(f"%{district1}%"),
                    CityDistrict.district.like(f"%{district2}%")
                )
            ).all()
    finally:
        session.close()