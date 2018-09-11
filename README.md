<h1>레티봇(LETi_Bot)</h1>
<br />
<br />

<h3>사용한 서비스 - API, AWS</h3>
<hr />

<ol>
  <li><a title="" href="https://console.aws.amazon.com/console/home">AWS EC2</a></li>
  <li><a title="" href="https://console.aws.amazon.com/console/home">AWS S3</a></li>
  <li><a title="" href="https://developers.naver.com/docs/detectLangs/examples/#python">Naver Papago Langdetect API</a></li>
  <li><a title="" href="https://developers.naver.com/docs/nmt/reference/">Naver Papago NMT(Neural Machine Translation) API</a></li>
  <li><a title="" href="https://developers.naver.com/docs/clova/api/CFR/API_Guide.md#Overview">Clova Face Recognition API</a></li>
  <li><a title="" href="https://www.data.go.kr/dataset/15000175/openapi.do">버스도착정보조회서비스 API</a></li>
  <li><a title="" href="https://www.data.go.kr/dataset/15000303/openapi.do">정류장정보조회서비스 API</a></li>
</ol>
<br />
<h3>사용한 파이선 모듈</h3>
<hr />
<ol>
  <li>flask</li>
  <li>pyqrcode</li>
  <li>pyzbar</li>
  <li>Pillow(또는 PIL도 가능하나, Pillow를 추천합니다.)</li>
  <li>boto3</li>
  <li>urllib(기본 모듈)</li>
</ol>
<br />

<h3>가동하기위해 필요한 것</h3>
<hr />
<ol>
  <li>Naver API, Clova API에 사용할 "client_id" 및 "client_secret"</li>
  <li>버스 관련 api들에 사용할 각각의 "user_key"</li>
  <li>AWS EC2, S3를 사용하기 위한 AWS 계정(Free tier도 가능)</li>
  <li>파이선의 boto3 모듈로 S3에 업로드 하기 위해 필요한 엑세스 키 ID 및 보안 엑세스 키</li>
</ol>
<br />

<h3>필요한 것들을 구하기 위한 방법</h3>
<hr />
<p>Naver APi와 Clove API에 사용할 "clinet_id" 및 "client_secret"은 <a title = "" href = "https://developers.naver.com">이곳</a>에서 어플리케이션을 등록하면 얻을 수 있습니다.</p>
<p>버스 관련 api 두가지 각각의 "user_key"는 먼저 <a title = "" href = "https://data.go.kr">데이터공공포털</a>에 회원가입을 하신 후<a title = "" href = "https://www.data.go.kr/dataset/15000759/openapi.do">이곳</a>과 <a title = "" href = "https://www.data.go.kr/dataset/15000175/openapi.do">이곳</a>에 활용신청을 하면 됩니다. 1시간마다 "user_key"가 동기화 되므로 활용신청 1시간 후 API 사용가능합니다.</p>
<p>AWS 계정은 <a> title = "" href = "">이곳</a>에서 회원가입 하시면 됩니다</p>
<p>엑세스 키 ID 및 보안 엑세스 키는 구글이 알려줄거에요^^</p>
<br />

<h3>파이팅!</h3>
<hr />
<p>자세한 구동 방법(EC2에 연결하는 putty 사용법 등)은 검색해보세요!</p>
