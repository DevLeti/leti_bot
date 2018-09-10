import urllib.request
import xml.etree.ElementTree as ET

def bus_num(route_id):
    if (route_id == "200000115"):
        return "5100"
    elif (route_id == "200000103"):
        return "9"
    elif (route_id == "234000016"):
        return "1112"
    elif (route_id == "234000001"):
        return "5500-1"
    elif (route_id == "200000112"):
        return "7000"
    elif (route_id == "234001243"):
        return "5107"
    elif (route_id == "234000324"):
        return "1550-1"
    elif (route_id == "200000262"):
        return "G5100"
    elif (route_id == "234001243"):
        return "M5107"
        """
        이 밑부터는 지역버스(마을버스 제외)
        """
    elif (route_id == "200000024"):
        return "310"
    elif (route_id == "200000076"):
        return "5"
    elif (route_id == "200000101"):
        return "4-1"
    elif (route_id == "200000093"):
        return "51"
    elif (route_id == "200000040"):
        return "7-2"
    elif (route_id == "200000048"):
        return "82-2"
    elif (route_id == "200000040"):
        return "7-2"
    elif (route_id == "200000103"):
        return "9"
    elif (route_id == "200000186"):
        return "9-1"
    elif (route_id == "200000010"):
        return "900"
    else:
        return "error"

"""
버스 번호에 따른 route_id들
"""
# id_5100 =200000115
# id_9 = 200000103
# id_1112 = 234000016
# id_5500_1 = 234000001
# id_7000 = 200000112
# id_5107 = 234001243

"""
정류소에 따른 station_id들
"""
# 228000710 외대앞(선승관/생대 방면) 버정 stationId
# 228000723 정문 앞(선승관/생대 방면) 버정 stationId M5107이 들어오는 길
# 203000125 정문(맥날앞)
# 228000703 외대앞(체대앞)

foreign_to_inside = '228000710' # 외대앞(선승관/생대 방면)
foreign_to_outside = '228000703' # 외대앞(체대앞)
jeonggeon_to_inside = '228000723' # 정문 앞(선승관/생대 방면)
jeonggeon_to_outside = '203000125' # 정문(맥날앞)


api_key = 'YOUR_API_KEY'

def bus_status(content):

    if (content == "1"):
        station_id = foreign_to_outside
    elif (content == "2"):
        station_id = foreign_to_inside
    elif (content == "3"):
        station_id = jeonggeon_to_outside
    elif (content == "4"):
        station_id = jeonggeon_to_inside
    else:
        return "잘못된 번호를 입력하셨습니다. 다시 명령을 보내주세요."


    url = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=' + api_key + '&stationId=' + station_id
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    result = ""

    if(rescode==200):
        response_body = response.read()
        response_body_decode = response_body.decode('utf-8')
        root = ET.fromstring(response_body_decode)
        result += "현재 버스 상황 :\n"
        for busArrivalList in root.iter('msgBody'):
            for locationNo1 in busArrivalList:
                result += "{0}번 버스 : {1}분\n".format(bus_num(locationNo1.findtext("routeId")), locationNo1.findtext("locationNo1"))


        return result[:-1]
    else:
        result += "에러가 발생했습니다. 관리자에게 문의해주세요."
        return result[:-1]
