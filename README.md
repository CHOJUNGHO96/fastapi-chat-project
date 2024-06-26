# Fastapi Chat Project
> Fastapi의 웹소켓 기능을 활용하여 간단한 채팅서비스 구축

![Static Badge](https://img.shields.io/badge/Python-%233776AB)
![Static Badge](https://img.shields.io/badge/Fastapi-%23009688)
![Static Badge](https://img.shields.io/badge/PostgreSql-%234169E1)
![Static Badge](https://img.shields.io/badge/Sqlalchemy-%23D71F00)
![Static Badge](https://img.shields.io/badge/MongoDb-%2347A248)
![Static Badge](https://img.shields.io/badge/Dependency_Injector-blue)
![Static Badge](https://img.shields.io/badge/Poetry-%2360A5FA)
![Static Badge](https://img.shields.io/badge/Gunicorn-%23499848)
![Static Badge](https://img.shields.io/badge/Docker-%232496ED)
![Static Badge](https://img.shields.io/badge/JwtToken-red)

## 해당프로젝트 상세내용
#### 1. 파이썬 Fastapi프레임워크를 기반으로 Fastapi공식문서에 나온 웹소켓 기능과 Dependency_Injector라이브러리를 활용하여 웹채팅서비스 구축하였습니다.<br>
#### FastApi웹소켓 공식문서 참고 URL : https://fastapi.tiangolo.com/ko/advanced/websockets/#handling-disconnections-and-multiple-clients
#### dependency-injector 공식문서 URL : https://python-dependency-injector.ets-labs.org/
#### 2. 채팅내역 저장은MongDb를 사용하고 나머지 상태저장은 Postgresql을 사용했습니다.
#### 3. 각채팅의 메세지ID는 Snowflake알고리즘을 사용하여 순서가 보장되고 유니크한값으로 설정했습니다.
#### 4. 나와 상대방의 채팅방 구분은 friend_ship라는 테이블에 각각 상대방과 나의기본키가 교차로 들어가서 교차된row의 pk값을 더해서 구분해준다.<br>
#### ex : 19번유저와 21번유저의 구분값은 아래에 나와있는 friendship_id의 합친값인 47이된다.<br>
![image](https://github.com/CHOJUNGHO96/fastapi-chat-project/assets/61762674/c1b479b8-eadf-4974-8168-833f408b7642)
#### 5. 기존공식문서 예제에는 웹소켓에 접속한 사용자들 전부 채팅을 공유했는데 나와 상대방만 채팅방을 공유하도록 ConnectionManager에 dict형태로 room_id를 키값을 추가하여 수정했습니다.<br>
### 공식문서코드
```py
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
```
### 수정한 코드 (src/app/chat/util/websocket_manager.py)
```py
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, room_id: int, websocket: WebSocket):
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
        await websocket.accept()

    def disconnect(self, room_id: int, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)
        if not self.active_connections[room_id]:
            del self.active_connections[room_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, room_id: int, message: str):
        for connection in self.active_connections.get(room_id, []):
            await connection.send_text(message)

```
#### 6. precommit을 사용하여 commit시 자동으로 black, flake8, toml-sort, isort 실행되도록해서 유효성검사 추가하였습니다.
#### 7. docker cpmpose를 이용하여 명령어입력하면 자동으로 빌드되도록 추가하였습니다.
#### 8. 마이그레이션을위한 alembic 추가하였습니다.
#### 9. ui구현을위해 chat gpt4를 활용하여 html파일 생성하였습니다.
#### 10. jwt token을 사용하여 사용자인증 구현 하였습니다.
#### 11. orm을 사용하기위해 sqlalchemy2.x 와 mongodb는 odmantic라이브러리 사용하였습니다.
#### 12. 유저정보 캐시에저장하기위해 redis 사용하였습니다.

![](../header.png)

## 개발 환경 설정
.env.example에있는 항목을채운뒤 .env로 변경해줍니다.
### ex</br>
![image](https://github.com/CHOJUNGHO96/fastapi-chat-project/assets/61762674/6dbe14f2-8a55-4468-b094-65fd64fd9d66) </br>
POSTGRES_SERVER과 REDIS_SERVER는 docker-compose컨테이너 명으로세팅을 해주고 만약 로컬에서 돌릴경우에 알맞은 서버ip로 값을 설정해줍니다.
MongDB 설정은 미리 MongDB클러스터 구성후에 구성한값들로 설정해줍니다.

## 실행 방법
winodws 기준
1. git clone을한다
2. docker desktop이없다면 설치하고 있으면 실행을시키고 cmd를열어서 fastapi-chat-project\src 경로에서 ```docker-compose up --build -d``` 실행
3. docker ps명령어를 입력하고 fastapi1의 컨테이너 아이디를 찾은후 ```docker exec -it 컨테이너ID /bin/bash``` 명령어를 입력하여 컨테이너에 접속한다.
4. 쉘에접속후 마이그레이션을 하기위해 ```/fastapi-chat-project/src```경로로 가서 alembic upgrade head 명령어 실행해준다</br>
ex
![image](https://github.com/CHOJUNGHO96/fastapi-chat-project/assets/61762674/0eb9e01d-ed79-41d1-ad04-89433089440b)
5. ```http://127.0.0.1:5051/api/v1/auth/login```로 접속하여 ui가 잘나오는지확인및 회원가입및 친구추가하고 채팅기능이 잘동작하는지 확인<br>
### 로그인 화면<br>
![image](https://github.com/CHOJUNGHO96/fastapi-chat-project/assets/61762674/458b9eb6-7dc0-4ad0-9e3c-89ffe1b0354f)
### 회원가입 화면<br>
![image](https://github.com/CHOJUNGHO96/fastapi-chat-project/assets/61762674/e3342bf8-6079-4e4d-9b23-48aabeb8a42b)
### 친구목록 화면<br>
![image](https://github.com/CHOJUNGHO96/fastapi-chat-project/assets/61762674/ea8cfff9-c578-4cd1-9ddf-1e20fbe1be23)
### 채팅방 화면<br>
![image](https://github.com/CHOJUNGHO96/fastapi-chat-project/assets/61762674/b57494ad-985e-421f-bf86-816264b37d5c)



## 업데이트 내역

* 1.0.0
    * 첫 릴리즈 완료

## 정보

조정호 – jo4186@naver.com

[https://github.com/CHOJUNGHO96/github-link](https://github.com/CHOJUNGHO96)

## 기여 방법

1. (<https://github.com/CHOJUNGHO96/fastapi-chat-project/fork>)을 포크합니다.
2. (`git checkout -b feature/fooBar`) 명령어로 새 브랜치를 만드세요.
3. (`git commit -am 'Add some fooBar'`) 명령어로 커밋하세요.
4. (`git push origin feature/fooBar`) 명령어로 브랜치에 푸시하세요. 
5. 풀리퀘스트를 보내주세요.

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
