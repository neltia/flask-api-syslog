# flask-api-syslog
- Flask-RESTX 라이브러리 활용 REST API 작성 예제
    - 파일 업로드
    - 사설 ssl 인증서 활용 https 적용
    - syslog msg handler

## 개발 환경
<pre>
python-dotenv==0.21.1
Flask==2.2.2
Werkzeug==2.2.2
flask-restx==1.2.0
</pre>


## 프로젝트 구성 방법
### 1. 사설 인증서 생성
<pre>
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
</pre>

### 2. 라이브러리 설치 및 실행
<pre>
sudo -i # 443 포트 실행은 root 권한으로 실행해야 가능
pip install -r requirements.txt
chmod +x run_app.sh
./run_app.sh 
</pre>

## 주의 사항
### rsyslog
- 기본적으로 syslog 자체에서 같은 메시지 반복 로깅을 방지하기 위해 중복 메시지 필터링이 적용돼 있음
- rsyslog의 경우 /etc/rsyslog.conf에 $RepeatedMsgReduction 옵션 기본 on 설정돼 있음
- 해당 옵션 변경 후 데몬 재시작
