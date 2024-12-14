from invoke import Collection, task

from .utils import docker_compose_command


@task
def up_airflow(ctx, build=False):
    """`docker-compose up -d` 명령 실행 태스크"""
    services = [
        "airflow-metadata",
        "airflow-scheduler",
        "airflow-webserver",
        "airflow-init",
    ]
    docker_compose_command(
        ctx, f"up -d {'--build' if build else ''} {' '.join(services)}"
    )


@task
def down(ctx, volumes=False):
    """`docker-compose down` 명령 실행 태스크"""
    docker_compose_command(
        ctx, f"down {'--volumes' if volumes else ''}"
    )


@task
def stop(ctx):
    """`docker-compose` stop 명령 실행 태스크"""
    docker_compose_command(ctx, f"stop")


@task
def command(ctx, cmd):
    """사용자 지정 명령 실행 태스크"""
    docker_compose_command(ctx, cmd)


docker_compose_collection = Collection()
docker_compose_collection.add_task(up_airflow, name="up_airflow")
docker_compose_collection.add_task(down, name="down")
docker_compose_collection.add_task(stop, name="stop")
docker_compose_collection.add_task(command, name="cmd")
