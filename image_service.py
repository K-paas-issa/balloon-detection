from geopy.geocoders import Nominatim
import s3utils
from ImageRequestDto import ImageRequest
from detect import prediction
import repository

def image_process(image_request : ImageRequest):
    image_path = s3utils.download_csv(image_request.path)
    if prediction(image_path) == False: # 풍선이 아닌 다른 이미지로 판별된다면
        repository.updateStatusFalse(image_request.balloonReportId)
        return
    
    balloon = repository.findById(image_request.balloonReportId)
    street_address = get_administrative_district(balloon.reported_latitude, balloon.reported_longitude)

    if street_address == None:
            print('street_address is none')
    else:
        print('district = {}'.format(street_address))
        district_arr = street_address.split(',')
    city_district = get_center_coordinate(district_arr)
    repository.updateReportedBalloon(balloon.id, city_district)
    return

def get_administrative_district(lat, lng):
    print('convert to district start')

    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    res = geolocoder.reverse([lat, lng], exactly_one=True, language='ko')
    if res==None:
        return None
    print('res = {}'.format(res))
    return res.address

def rearrange_district(district_arr):
    filtered_words = [word.strip() for word in district_arr if not word.strip().isdigit()]
    reversed_words = filtered_words[::-1]
    res_string = ' '.join(reversed_words)
    
    return res_string

def get_center_coordinate(district_arr):

    try:
        
        # Check the length of district_arr 단어가 2개 이하거나, 3개이면서 2번째 단어가 숫자일 경우
        if len(district_arr) < 3 or (len(district_arr) < 4 and district_arr[-2].isdigit() == True):
            return None
        
        # 숫자가 없는 경우. 태안군, 충청남도, 대한민국의 경우
        results = repository.findByCityAndDistrict(district_arr[-2].strip(), district_arr[-3].strip())
        if len(results) == 1:
            return results[0]

        # 숫자가 없는 경우. 일산동구, 고양시, 대한민국의 경우
        results = repository.findByOnlyDistrict(district_arr[-2].strip(), district_arr[-3].strip())
        if len(results) == 1:
            return results[0]
        
        # 세종특별자치시의 경우
        print(district_arr[-3])
        results = repository.findByCity(district_arr[-3].strip())
        if len(results) == 1:
            return results[0]
        
        # 양주시, 21341, 대한민국의 경우
        results = repository.findByDistrict(district_arr[-3].strip())
        if len(results) == 1:
            return results[0]
        
        # 설악로, 임천리, 양양군, 강원특별자치도, 25035, 대한민국의 경우
        results = repository.findByCityAndDistrict(district_arr[-3].strip(), district_arr[-4].strip())
        if len(results) == 1:
            return results[0]

        # 풍산동, 일산동구, 고양시, 10442, 대한민국의 경우
        results = repository.findByOnlyDistrict(district_arr[-3].strip(), district_arr[-4].strip())
        if len(results) == 1:
            return results[0]
        
        # 전주시청, 기린대로, 서노송동, 완산구, 전주시, 전북특별자치도, 55032, 대한민국의 경우
        results = repository.findByCityAndDistricts(district_arr[-3].strip(), district_arr[-4].strip(), district_arr[-5].strip())
        if len(results) == 1:
            return results[0]
        return None, None
    except Exception as e:
        print(f"쿼리 실행 중 오류 발생: {e}")
    finally:
        print('save data end')