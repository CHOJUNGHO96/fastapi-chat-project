# Fastapi Chat Project
> Fastapi의 웹소켓 기능을 활용하여 간단한 채팅서비스 구축

![Static Badge](https://img.shields.io/badge/Python-%233776AB)
![Static Badge](https://img.shields.io/badge/Fastapi-%23009688)
![Static Badge](https://img.shields.io/badge/PostgreSql-%234169E1)
![Static Badge](https://img.shields.io/badge/Sqlalchemy-%23D71F00)
![Static Badge](https://img.shields.io/badge/MongoDb-%2347A248)
![Static Badge](https://img.shields.io/badge/Dependency_Injector-blue)
![Static Badge](https://img.shields.io/badge/Poetry-%2360A5FA)

파이썬 Fastapi프레임워크를 기반으로 Fastapi공식문서에 나온 웹소켓 기능과 Dependency_Injector라이브러리를 활용하여 웹채팅서비스 구축하였습니다.
채팅내역 저장은MongDb를 사용하고 나머지 상태저장은 Postgresql을 사용했습니다.

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
5. ```http://127.0.0.1:5051/api/v1/auth/login```로 접속하여 ui가 잘나오는지 확인한다.<br>
![image](https://github.com/CHOJUNGHO96/fastapi-chat-project/assets/61762674/458b9eb6-7dc0-4ad0-9e3c-89ffe1b0354f)


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
