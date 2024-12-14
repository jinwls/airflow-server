from airflow.hooks.base_hook import BaseHook
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

class SlackBot:
    """Airflow Callback 메시지를 생성하고 Slack으로 전송하는 클래스"""
    def __init__(self, conn_id, username):
        """
        param:
        - conn_id: Slack Webhook 연결 ID
        - username: Slack 메시지에 표시될 사용자 이름
        """
        self.conn_id = conn_id
        self.username = username

    def post_message(self, context, message):
        """Slack에 메시지를 전송"""
        slack_alert = SlackWebhookOperator(
            task_id='slack_alert',
            message=message,
            username=self.username,
            slack_webhook_conn_id=self.conn_id,
        )
        return slack_alert.execute(context=context)

    def __format_callback_message(self, context, **kwargs):
        """Slack 알림 메시지를 포맷팅"""
        options = {
            'icon': ':large_blue_circle:',
            'title': '[not provided]'
        }
        options.update(kwargs)
        slack_msg = """
==================================================
{icon} *{title}*
==================================================
*Task*: {task}
*Dag*: {dag}
*Execution Date:*: {execution_date}
*Log Url*: {log_url}
        """.format(
            icon=options['icon'],
            title=options['title'],
            task=context.get('task_instance').task_id,
            dag=context.get('task_instance').dag_id,
            execution_date=context.get('execution_date').astimezone(),
            log_url=context.get("task_instance").log_url # .replace('http://localhost:8080/', 'http://0.0000.0000.0000:8080/')
        )
        return slack_msg

    def post_alert(self, context, **kwargs):
        """작업 실패 알림 전송 (빨간 아이콘)"""
        kwargs['icon'] = ':red_circle:'
        message = self.__format_callback_message(context, **kwargs)
        return self.post_message(context, message)

    def post_info(self, context, **kwargs):
        """일반 정보 알림 전송 (녹색 아이콘)"""
        kwargs['icon'] = ':large_green_circle:'
        message = self.__format_callback_message(context, **kwargs)
        return self.post_message(context, message)

    def post_warning(self, context, **kwargs):
        """경고 알림 전송 (주황색 아이콘)"""
        kwargs['icon'] = ':large_orange_circle:'
        message = self.__format_callback_message(context, **kwargs)
        return self.post_message(context, message)

class CallbackNotifier:
    """Airflow 작업 상태 이상 시 Slack 알림을 호출하는 클래스"""

    SLACK_CONN_ID = 'slack_report'
    USERNAME = 'airflow'

    @staticmethod
    def on_failure_callback(context):
        """작업 실패 시 호출되는 콜백 함수"""
        bot = SlackBot(CallbackNotifier.SLACK_CONN_ID, CallbackNotifier.USERNAME)
        bot.post_alert(context, title="Failed Task Alert")

    @staticmethod
    def on_retry_callback(context):
        """작업 재시도 시 호출되는 콜백 함수"""
        bot = SlackBot(CallbackNotifier.SLACK_CONN_ID, CallbackNotifier.USERNAME)
        bot.post_warning(context, title="Retry Task Alert")
