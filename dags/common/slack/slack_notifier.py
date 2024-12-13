from airflow.hooks.base_hook import BaseHook
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

class SlackBot:
    def __init__(self, conn_id, username):
        self.conn_id = conn_id
        self.username = username

    def post_message(self, context, message):
        slack_alert = SlackWebhookOperator(
            task_id='slack_alert',
            message=message,
            username=self.username,
            slack_webhook_conn_id=self.conn_id,
        )
        return slack_alert.execute(context=context)

    def __format_callback_message(self, context, **kwargs):
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
        kwargs['icon'] = ':red_circle:'
        message = self.__format_callback_message(context, **kwargs)
        return self.post_message(context, message)

    def post_info(self, context, **kwargs):
        kwargs['icon'] = ':large_green_circle:'
        message = self.__format_callback_message(context, **kwargs)
        return self.post_message(context, message)

    def post_warning(self, context, **kwargs):
        kwargs['icon'] = ':large_orange_circle:'
        message = self.__format_callback_message(context, **kwargs)
        return self.post_message(context, message)

class CallbackNotifier:
    SLACK_CONN_ID = 'slack_report'
    USERNAME = 'airflow'

    @staticmethod
    def on_failure_callback(context):
        bot = SlackBot(CallbackNotifier.SLACK_CONN_ID, CallbackNotifier.USERNAME)
        bot.post_alert(context, title="Failed Task Alert")

    @staticmethod
    def on_retry_callback(context):
        bot = SlackBot(CallbackNotifier.SLACK_CONN_ID, CallbackNotifier.USERNAME)
        bot.post_warning(context, title="Retry Task Alert")
