# Invoke는 파이썬으로 작성된 명령줄 작업을 정의하고 실행할 수 있게 해주는 라이브러리
from invoke import Collection

from .docker_compose import docker_compose_collection

ns = Collection()
# docker_compose_collection을 "compose"라는 이름으로 컬렉션에 추가
# 내 태스크들을 "compose"라는 접두사로 실행할 수 있도록 함
ns.add_collection(docker_compose_collection, "compose")
