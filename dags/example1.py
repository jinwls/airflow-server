from datetime import datetime, timedelta

from common.slack import CallbackNotifier

from airflow.models.dag import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

default_args = {
    "depends_on_past": False,
    # "retries": 1,
    # "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2022, 1, 1),
    "on_failure_callback": CallbackNotifier().on_failure_callback,
}

with DAG(
    dag_id="example1",
    default_args=default_args,
    catchup=False,
) as dag:
    
    @task
    def example_failed_task():
        from airflow.exceptions import AirflowFailException
        raise AirflowFailException(f"testing")



    t2 = BashOperator(task_id="t2", bash_command="sleep 5 && echo task 2")
    t3 = BashOperator(task_id="t3", bash_command="sleep 15 && echo task 3")
    t4 = BashOperator(task_id="t4", bash_command="echo task 4")
    [t2, t3] >> t4 >> example_failed_task()
