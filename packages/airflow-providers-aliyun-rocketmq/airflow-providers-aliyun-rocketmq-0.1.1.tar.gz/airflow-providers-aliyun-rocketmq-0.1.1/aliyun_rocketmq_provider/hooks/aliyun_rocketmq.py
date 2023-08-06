import json
from typing import Dict

from mq_http_sdk.mq_client import MQClient, MQProducer
from mq_http_sdk.mq_producer import TopicMessage

from airflow.hooks.base import BaseHook


class AliyunRocketMQHook(BaseHook):
    """Interact with Aliyun RocketMQ."""

    conn_name_attr = 'aliyun_rocketmq_conn_id'
    default_conn_name = 'aliyun_rocketmq_default'
    conn_type = 'aliyun_rocketmq'
    hook_name = 'AliyunRocketMQ'

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        return {
            "hidden_fields": ['port', 'extra'],
            "relabeling": {
                'login': 'Access ID',
                'password': 'Access Key',
                'schema': 'Instance ID'
            },
            "placeholders": {
                'login': 'access id',
                'password': 'access key',
                'schema': 'instance_id'
            },
        }

    def __init__(
        self,
        topic: str,
        aliyun_rocketmq_conn_id: str = default_conn_name
    ) -> None:
        super().__init__()
        self.topic = topic
        self.aliyun_rocketmq_conn_id = aliyun_rocketmq_conn_id

    def get_conn(self) -> MQProducer:
        """Returns mq producer."""
        conn = self.get_connection(self.aliyun_rocketmq_conn_id)
        client = MQClient(conn.host, conn.login, conn.password)
        return client.get_producer(conn.schema, self.topic)

    def run(self, data: Dict, tag: str = None, fail_silently: bool = False) -> TopicMessage:
        """Publish the data."""
        try:
            conn = self.get_conn()
            message = TopicMessage(json.dumps(data), (tag or "").lower())
            return conn.publish_message(message)
        except Exception as e:
            if not fail_silently:
                raise

            self.log.warning("Publish msg to {} failed: {}", self.topic, repr(e))
