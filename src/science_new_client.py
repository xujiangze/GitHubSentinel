# -*- coding: utf-8 -*-
import requests
import os
from logger import LOG  # 导入日志模块
from datetime import datetime  # 导入datetime模块用于获取日期和时间


class ScienceNewClient(object):
    # 科学探索API https://www.tianapi.com/gethttp/108
    def __init__(self, search_url, key):
        # https://apis.tianapi.com/networkhot/index
        self.search_url = search_url
        self.key = key

    def export_top_news(self, date=None, hour=None):
        LOG.debug("准备导出科学的热门新闻。")
        top_news = self.get_top_news()  # 获取新闻数据

        if not top_news:
            LOG.warning("未找到任何科学热门的新闻。")
            return None

        # 如果未提供 date 和 hour 参数，使用当前日期和时间
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        if hour is None:
            hour = datetime.now().strftime('%H')

        # 构建存储路径
        dir_path = os.path.join('science_news', date)
        os.makedirs(dir_path, exist_ok=True)  # 确保目录存在

        file_path = os.path.join(dir_path, f'{hour}.md')  # 定义文件路径
        with open(file_path, 'w') as file:
            file.write(f"#  科学探索热门新闻 ({date} {hour}:00)\n\n")
            i = 0
            for item in top_news:
                i += 1
                msg = f"{i}. [{item['title']}]({item['url']}) 详细内容: {item['description']}\n"
                file.write(msg)

        LOG.info(f"科学探索热门新闻生成：{file_path}")
        return file_path

    def get_top_news(self):
        """
        {
          "code": 200,
          "msg": "success",
          "result": {
            "curpage": 1,
            "allnum": 10,
            "newslist": [
              {
                "id": "a4be5e47245beca679767692b865af06",
                "ctime": "2024-11-08 18:00",
                "title": "测量精度最高达头发丝直径的十万分之一，上海交大发布中子谱仪“洛书”",
                "description": "上海交通大学今日宣布，以“洛书”命名的一台超长多模式中子小角散射谱仪，已于2024年10月28日顺利通过技术验收。",
                "source": "IT家科学探索",
                "picUrl": "https://img.ithome.com/newsuploadfiles/thumbnail/2024/11/809026_240.jpg?x-bce-process=image/format,f_auto",
                "url": "https://www.ithome.com/0/809/026.htm"
              },
            ]
          }
        }
        :return:
        """
        url = self.search_url
        params = {
            "key": self.key,
            "num": 10,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        resp = requests.get(url, params=params, headers=headers)
        resp.raise_for_status()
        ret = resp.json()

        if ret.get("code") == 200:
            return ret.get("result", {}).get("newslist", [])

        raise ValueError(f"获取新闻失败: {ret.get('msg')}")


if __name__ == '__main__':
    key = os.environ.get("TIAN_API_KEY")
    client = ScienceNewClient("https://apis.tianapi.com/sicprobe/index", key)
    client.export_top_news("daily_progress")
