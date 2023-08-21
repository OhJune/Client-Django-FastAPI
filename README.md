# Client and Django and FastAPI Connection

**클라이언트는 웹 브라우저이고, 서버는 장고와 FastAPI입니다.** 

웹 브라우저에서 사용자가 양식을 작성하면 클라이언트(JQuery와 AJAX를 사용한 JavaScript)가 이 정보를 서버(Django 및 FastAPI)로 전송합니다. 웹 페이지상에서 작동하는 JavaScript는 클라이언트 쪽 코드이고, 장고 및 FastAPI 서버 애플리케이션은 각각 서버 측 코드입니다.

1. 클라이언트: 웹 페이지에서 작성된 JavaScript 코드. 서버에 요청을 보내고 결과를 표시함.
2. 장고: 요청을 처리하고 자체 데이터베이스를 관리하는 웹 프레임워크입니다. FastAPI에서 추가 처리를 위해 데이터를 전달받고 결과를 반환.
3. FastAPI: FastAPI 서비스에 API로 구현되어 있습니다. 더 빠른 처리와 ML 모델 실행 제공.

**따라서 클라이언트는 웹 브라우저와 JavaScript, 서버는 장고와 FastAPI로 구성됩니다.**

https://oh-um.tistory.com/30

+) 사용자가 증가할 경우 비동기 처리방식으로 celery와 브로커인 rabbitmq를 사용

![image](https://github.com/OhJune/Client-Django-FastAPI/assets/124857930/44acfce7-9f12-45ac-81bf-36cac69b70f0)

--
## FastAPI 기능

1. model 서빙 : 학습된 모델인 word2vec을 이용하여 사용자의 플레이리스트에 따른 추천곡 10곡을 DB에서 조회 후 response

2. GPT추천 값 서빙 : 학습된 모델에 없는 플레이리스트가 들어올 경우 chatgpt api를 사용하여 response 


