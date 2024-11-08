import requests

from implement.notifier import Notifier as NotifierABC


# 下面是一个实现抽象类的具体类
class WebHookNotifierClient(NotifierABC):
    # 官方文档位置: https://developer.work.weixin.qq.com/document/path/91770
    def __init__(self, webhook_url, webhook_key):
        self.webhook_url = webhook_url
        self.webhook_key = webhook_key
        self.default_headers = {
            "Content-Type": "application/json"
        }

    def notify_by_mentioned(self, markdown_content, mentioned_list=None, mentioned_mobile_list=None):
        """
        通过企业微信群机器人发送消息，并@指定用户
        :param markdown_content: markdown格式的消息内容
        :param mentioned_list: eg: :["wangqing","@all"]
        :param mentioned_mobile_list: ["13800001111","@all"]
        :return:
        """
        request_header = self.default_headers
        query_params = {
            "key": self.webhook_key
        }
        data = {
            "msgtype": "text",
            "text": {
                "content": markdown_content,
            }
        }
        if mentioned_list or mentioned_mobile_list:
            data["text"]["mentioned_list"] = mentioned_list
            data["text"]["mentioned_mobile_list"] = mentioned_mobile_list

        resp = requests.post(self.webhook_url, headers=request_header, params=query_params, json=data)
        resp.raise_for_status()
        return resp.json()

    def notify(self, markdown_content):
        """
        通过企业微信群机器人发送消息
        :param markdown_content:
        :return:
        """
        request_header = self.default_headers
        query_params = {
            "key": self.webhook_key
        }
        data = {
            "msgtype": "text",
            "text": {
                "content": markdown_content
            }
        }
        resp = requests.post(self.webhook_url, headers=request_header, params=query_params, json=data)
        resp.raise_for_status()
        return resp.json()


if __name__ == '__main__':
    # 测试企业微信机器人
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
    webhook_key = "你的weebhook"
    notifier = WebHookNotifierClient(webhook_url, webhook_key)
    notifier.notify("Hello, World!")
    notifier.notify_by_mentioned("Hello, World!", mentioned_mobile_list=["企业微信群内部成员的手机号"])