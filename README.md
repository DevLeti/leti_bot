# 레티봇(LETi_Bot)

## 사용한 서비스 - API, AWS
1. AWS EC2
2. AWS S3
3. [Naver Papago Langdetect API](https://developers.naver.com/docs/detectLangs/examples/#python)
4. [Naver Papago NMT(Neural Machine Translation) API](https://developers.naver.com/docs/nmt/reference/)
5. [Clova Face Recognition API](https://developers.naver.com/docs/clova/api/CFR/API_Guide.md#Overview)
6. [버스도착정보조회서비스 API](https://www.data.go.kr/dataset/15000175/openapi.do)
7. [정류장정보조회서비스 API](https://www.data.go.kr/dataset/15000303/openapi.do)

## 사용한 파이선 모듈
1. flask
2. pyqrcode
3. pyzbar
4. Pillow(또는 PIL도 가능하나, Pillow를 추천합니다.)
5. boto3
6. urllib(기본 모듈)

## 가동하기위해 필요한 것
1. Naver API, Clova API에 사용할 "client_id" 및 "client_secret"
2. 버스 관련 api들에 사용할 각각의 "user_key"
3. AWS EC2, S3를 사용하기 위한 AWS 계정(Free tier도 가능)
4. 파이선의 boto3 모듈로 S3에 업로드 하기 위해 필요한 엑세스 키 ID 및 보안 엑세스 키

## API 발급 방법 및 AWS 엑세스 키 (S3)
- Naver APi와 Clove API에 사용할 "clinet_id" 및 "client_secret"은 [이곳](https://developers.naver.com)에서 어플리케이션을 등록하면 얻을 수 있습니다.
- 버스 관련 api 두가지 각각의 "user_key"는 먼저 [데이터공공포털](https://data.go.kr)에 회원가입을 하신 후 [이곳](https://www.data.go.kr/dataset/15000759/openapi.do)과 [이곳](https://www.data.go.kr/dataset/15000175/openapi.do)에 활용신청을 하면 됩니다. 1시간마다 "user_key"가 동기화 되므로 활용신청 1시간 후 API 사용가능합니다.
- AWS 계정은 [이곳](https://aws.amazon.com/ko/)에서 회원가입 하시면 됩니다.
- 엑세스 키 ID 및 보안 엑세스 키는 [이곳](https://keichee.tistory.com/298)을 참고하시면 됩니다.
