from pathlib import Path


def get_project_dir(ctx) -> Path:
    """
    `git rev-parse --show-toplevel` 명령어를 실행하여 Git 프로젝트의 루트 디렉토리
    
    - 반환값: Git 리포지토리의 루트 디렉토리를 나타내는 `Path` 객체
    """
    return Path(ctx.run("git rev-parse --show-toplevel").stdout.strip())


def docker_compose_command(ctx, command):
    """
    `docker-compose` 명령어를 실행하기 위한 명령어 구성 및 실행

    매개변수: 
    - command (str): 실행할 `docker-compose` 명령어
    """
    docker_compose_folder_path = get_project_dir(ctx).joinpath("docker-compose")
    compose_files = ["airflow"]
    cmd = f"docker-compose {' '.join([f'-f {docker_compose_folder_path.joinpath(file)}.yml' for file in compose_files])} {command}"
    print(cmd)
    ctx.run(cmd)
