from flask import Flask
from flask import jsonify
from flask import json
from flask import request
import os
import sys
import urllib.request
import requests
import pyqrcode
from pyzbar.pyzbar import decode
from PIL import Image
import bus_api
import s3_upload

"""
필요 설치 모듈:
flask
urllib
pyqrcode
pyzbar
PIL(또는 Pillow)
boto3

번역은 papago NMT API를 사용했습니다.
문장 언어 감지는 papago 언어감지 API를 사용했습니다.
https://developers.naver.com/docs/nmt/reference/ <= NMT 번역 참고
https://developers.naver.com/docs/detectLangs/examples/#python <= 문장언어감지 참고

얼굴감정분석은 Clova Face Recognition API를 사용했습니다.
https://developers.naver.com/docs/clova/api/CFR/API_Guide.md#Overview <= 얼굴감정분석 참고
*얼굴감정분석의 url을 수정하면 연예인 닮을꼴 검색으로도 사용할 수 있습니다.

!! 버스api 관련 코드는 bus_api.py에 기입되어있습니다.
실시간버스서비스는 버스도착정보 조회 API를 사용했습니다.
https://www.data.go.kr/dataset/15000175/openapi.do <= 버스도착정보 조회 참고

각 버스의 특정 ID는 정류소정보조회 서비스 API의 getStaionsByPosList를 사용했습니다.
https://www.data.go.kr/dataset/15000303/openapi.do <= 정류소정보조회 서비스 참고


QR코드 인식은 pyqrcode 모듈을 사용했습니다.

QR코드 생성은 pyzbar 모듈, PIL 라이브러리를 사용했습니다.
*카카오톡 봇은 로컬파일을 전송하지 못합니다.
*그래서 AWS S3를 이용해 클라우드를 구축, boto3로 클라우드에 업로드를 한 후 링크를 이용하는 방식을 사용했습니다.


서버는 AWS(Amazon Web Service) EC2 (Elastic Compute Cloud)를 사용했습니다.
클라우드는 AWS(Amazon Web Service) S3를 사용했습니다.

Develop Laptop Specification:
laptop model name : HP Envy 13 (ad052tu)
CPU : Intel Core i5-7200U @ 2.50GHz (4CPUs), ~2.7GHz
RAM : 8912MB RAM
GPU : Intel HD Graphics 620 (CPU 내장그래픽)
OS : Windows 10 Home 64bit (10.0, 빌드 17134)


AWS EC2 Specification :
Kind of instance : t2.micro
OS : Ubuntu 16.04.4 LTS (GNU/Linux 4.4.0-1066-aws x86_64)


"""

app = Flask(__name__)
status = "none"
null = "null"


"""
!!!
네이버 파파고 NMT api를 위한 client_id와 secret
!!!
"""
client_id = "YOUR_APP_ID" #네이버 파파고 NMT api
client_secret = "YOUR_APP_SECRET" #상동

"""
papago langdetect
"""
def langdetect(source_text):
    encQuery = urllib.parse.quote(source_text)
    data = "query=" + encQuery
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        response_body_decode = response_body.decode('utf-8')
        response_body_dict = eval(response_body_decode)
        result = response_body_dict["langCode"]
        return result
    else:
        return "error"

"""
papago NMT
"""
def translate(source_text , target_lan):
    source_lan = langdetect(source_text)  # 번역할 문장의 언어
    if (langdetect(source_text) == "error"):
        return "문장의 언어가 감지되지 않았습니다."
    # target_lan = "ko"  # 번역된 문장의 언어 <= 파라미터로 받아서 생략
    encText = urllib.parse.quote(source_text)
    data = "source=" + source_lan + "&target=" + target_lan + "&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request_trans = urllib.request.Request(url)
    request_trans.add_header("X-Naver-Client-Id", client_id)
    request_trans.add_header("X-Naver-Client-Secret", client_secret)
    response_trans = urllib.request.urlopen(request_trans, data=data.encode("utf-8"))
    rescode = response_trans.getcode()
    if (rescode == 200):
        response_body = response_trans.read()
        result = response_body.decode('utf-8')
        result_dict = eval(result)
        translated_text = result_dict["message"]["result"]["translatedText"]
        return translated_text

    else:
        print("Error Code:" + rescode)

"""
얼굴인식할때 카톡으로 받은 이미지가 url로 주어지는데 files = {'image': open('./temp.jpg', 'rb')} 에서 url을 오픈하면 에러나므로 파일을 다운 후 열기 위해서 img_dl 함수 정의
"""
def img_dl(url):
    img_name = "temp.png"
    urllib.request.urlretrieve(url, img_name)

"""
qrcode generator
"""
def qr_write(content):
    qr_write = pyqrcode.create(content)
    qr_write.png("qr_code.png", scale=6)
    return 0

"""
qrcode decoder
"""
def qr_read(content):
    try:
        img_dl(content)
        convert_jpg = Image.open('./temp.png')
        convert_jpg.save('./temp.jpg', "JPEG")
        result = decode(Image.open('./temp.jpg'))
        decode_result = result[0].data.decode("utf-8")
        return decode_result
    except:
        return "error"



"""
face recognition
"""
def face_recog(content):
    global null
    url = "https://openapi.naver.com/v1/vision/face"  # 얼굴감지
    # url = "https://openapi.naver.com/v1/vision/celebrity" #유명인 얼굴인식
    img_dl(content) #웹 이미지 다운로드
    files = {'image': open('./temp.png', 'rb')}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
    response = requests.post(url, files=files, headers=headers)
    rescode = response.status_code
    if (rescode == 200):
        print(response.text)
        result = eval(response.text)
        face_count = result["info"]["faceCount"]
        result_return = ""
        if (face_count == 1):
            result_return = result_return + "감지된 얼굴의 개수 : 1\n"
            result_return = result_return + "성별 : {0} / 정확도 : {1} %\n".format(result["faces"][0]["gender"]["value"], round(result["faces"][0]["gender"]["confidence"] * 100 , 1))
            result_return = result_return + "나이 : {0} / 정확도 : {1} %\n".format(result["faces"][0]["age"]["value"],round(result["faces"][0]["age"]["confidence"] * 100 , 1))
            result_return = result_return + "감정 : {0} / 정확도 : {1} %\n".format(result["faces"][0]["emotion"]["value"],round(result["faces"][0]["emotion"]["confidence"] * 100 , 1))
            result_return = result_return + "자세 : {0} / 정확도 : {1} %\n".format(result["faces"][0]["pose"]["value"],round(result["faces"][0]["pose"]["confidence"] * 100 , 1))
            return result_return
        else:
            result_return = result_return + "감지된 얼굴의 개수 : {0}\n".format(face_count)
            for i in range(face_count):
                result_return = result_return + "{0}번째 얼굴 :\n".format(i+1)
                result_return = result_return + "성별 : {0} / 정확도 : {1} %\n".format(result["faces"][i]["gender"]["value"], round(result["faces"][i]["gender"]["confidence"] * 100 , 1))
                result_return = result_return + "나이 : {0} / 정확도 : {1} %\n".format(result["faces"][i]["age"]["value"],round(result["faces"][i]["age"]["confidence"] * 100 , 1))
                result_return = result_return + "감정 : {0} / 정확도 : {1} %\n".format(result["faces"][i]["emotion"]["value"],round(result["faces"][i]["emotion"]["confidence"] * 100 , 1))
                result_return = result_return + "자세 : {0} / 정확도 : {1} %\n".format(result["faces"][i]["pose"]["value"],round(result["faces"][i]["pose"]["confidence"] * 100 , 1))
            return result_return
    else:
        return "얼굴이 인식되지 않았습니다."



@app.route("/keyboard")
def keyboard():
    return jsonify(type="text")



@app.route("/message", methods=["POST"])
def message():
    data = json.loads(request.data)
    print(data)
    content = data["content"]
    global status

    if (status == "qrcode_write"):
        status = "none"
        qr_write(content) # qr_gen.png 생성
        print("성공")
        response = {
            "message": {
                "text":
                    "링크 :\n" + s3_upload.app("qr_code.png") + "\n유의사항 : 링크는 7일 후 만료됩니다."

            }
        }
    elif (status == "bus"):
        status = "none"
        result = bus_api.bus_status(content)
        response = {
            "message": {
                "text": result
            }
        }
    elif (content.find("얼굴분석") == 0):
        status = "emotion"
        response = {
            "message": {
                "text": '사진을 보내주세요!'
            }
        }

    elif (content.find("실시간학교정류장상황") == 0 or content.find("실시간") == 0):
        status = "bus"
        response = {
            "message":{
                "text": '어느 정류장의 정보를 알고싶으신가요?\n'
                        '1. 외대앞(체대앞/정건 방면)\n'
                        '2. 외대앞(선승관/생대 방면)\n'
                        '3. 경희대정문(맥날앞)\n'
                        '4. 경희대정문(선승관/생대 방면)'
            }
        }
    elif (content.find("qr코드") == 0 or content.find("QR코드") == 0 or content.find("큐알코드") == 0):
        if (content.find("생성") == 4):
            status = "qrcode_write"
            response = {
                "message": {
                    "text": 'QR코드를 생성할 텍스트/사이트주소를 보내주세요!'
                }
            }
        else:
            status = "qrcode_read"
            response = {
                "message": {
                    "text": 'QR코드 이미지를 보내주세요!'
                }
            }
    elif (data["type"]  == 'photo'):
        if (status == "none"):
            response = {
                "message": {
                    "text": '어떤 작업을 하실껀가요?'
                }
            }
        elif (status == "emotion"):
            face_result = face_recog(content)
            response = {
                "message": {
                    "text": face_result
                }
            }
            status = "none"
        elif (status == "qrcode_read"):
            status = "none"
            read_result = qr_read(content)
            if (read_result == "error"):
                response = {
                    "message": {
                        "text": "QR코드가 인식되지 않았습니다."
                    }
                }
            else:
                response = {
                    "message": {
                        "text": "QR코드 내용:\n" + read_result
                    }
                }


    elif (content.find("번역") == 0):
        slash = content.find("/")
        content = content[slash+1:]
        slash = content.find("/")
        content_target_lan = content[0:slash]
        content = content[slash+1:]
        source_text = content
        print(content)
        translation_result = translate(source_text, content_target_lan)

        response = {
            "message": {
                "text": "번역결과 :\n" + translation_result
            }
        }



    elif (content.find("메아리") == 0):
        response = {
            "message": {
              "text": content[4:]
         }
        }
        
    else:
        response = {
            "message": {
              "text": "수행가능기능목록:\n1. 번역\n2. 실시간학교정류장상황\n3. 얼굴분석\n4. QR코드인식 및 생성\n5. 메아리\n"
                "사용법은 https://devleti.github.io/how_to_use_bot <= 이곳을 참고해주세요!"
         }
        }

    response = json.dumps(response, ensure_ascii=False)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888) #포트 번호는 필요한 포트로!