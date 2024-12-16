# Airflow-server

이 프로젝트는 Airflow 로컬 개발/테스트 환경을 구축하기 위한 프로젝트로 아래 절차를 따라 주세요.

## Requirements
- [python](https://www.python.org/downloads/) 3.8+
- [docker desktop](https://docs.docker.com/get-started/get-docker/) and [docker compose](https://docs.docker.com/compose/install/)
- Python 패키지 설치:
    ```shell
    pip install -r requirements.txt
    ```

### Development
코드 커밋 시 정해진 linter 규칙을 적용하려면, 아래 명령어로 pre-commit을 활성화하세요:
```shell
pre-commit install
```

## Airflow-server Deploy
Docker Desktop을 실행한 후, 아래 명령어로 Airflow 서버를 로컬 환경에 배포합니다:
```shell
# Default Airflow version: 2.10.3
invoke compose.up --build
```
서버가 정상적으로 실행되면, 웹 브라우저(`http://localhost:8080`)에 접속하고, 기본 계정 정보를 통해 로그인하세요.
- Username: airflow
- Password: airflow


## Airflow-server Stop
서버 사용이 끝난 후, 다음 명령어를 사용해 컨테이너를 관리하세요:
- 컨테이너 일시 정지:
    ```shell
    invoke compose.stop
    ```
- 컨테이너 삭제:
    ```shell
    invoke compose.down
    ```
- 컨테이너 및 볼륨 삭제:
    ```shell
    invoke compose.down --volumes
    ```

원작자 @hussein-awala via https://github.com/hussein-awala/airflow-server