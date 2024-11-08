# 作业说明
在 GitHubSentinel v0.5 基础上，扩展实现 Hacker News 趋势报告生成。实现优先级：Daemon（Required） > Graido > Command

# 作业解析
1. 了解 Hacker News 网页
2. 将Hacker News 网页的内容解析为结构化数据
3. 生成 Hacker News 趋势报告

## 了解 Hacker News 网页
hacker News 网页链接: https://news.ycombinator.com/

## 将Hacker News 网页的内容解析为结构化数据
爬虫类解析html可以使用库
- BeautifulSoup

## 生成 Hacker News 趋势报告
- 生成报告的内容可以包括：标题、链接、评论数、发布时间等
- 核心思路是解析网页内容，提取出需要的信息，然后提交给gpt进行总结

## 其他要求
由于hacker news需要科学上网, 因此记得使用代理

# 作业解析
## 1. 抓取hacker news的热门新闻
```python
import requests  # 导入requests库用于HTTP请求
from bs4 import BeautifulSoup  # 导入BeautifulSoup库用于解析HTML内容
from datetime import datetime  # 导入datetime模块用于获取日期和时间
import os  # 导入os模块用于文件和目录操作


class HackerNewsClient:
    def __init__(self):
        self.url = 'https://news.ycombinator.com/'  # Hacker News的URL

    def fetch_top_stories(self):
        print("准备获取Hacker News的热门新闻。")
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            top_stories = self.parse_stories(response.text)  # 解析新闻数据
            return top_stories
        except Exception as e:
            print(f"获取Hacker News的热门新闻失败：{str(e)}")
            return []

    def parse_stories(self, html_content):
        print("解析Hacker News的HTML内容。")
        soup = BeautifulSoup(html_content, 'html.parser')
        stories = soup.find_all('tr', class_='athing')  # 查找所有包含新闻的<tr>标签

        top_stories = []
        for story in stories:
            title_tag = story.find('span', class_='titleline').find('a')
            if title_tag:
                title = title_tag.text
                link = title_tag['href']
                top_stories.append({'title': title, 'link': link})

        print(f"成功解析 {len(top_stories)} 条Hacker News新闻。")
        return top_stories

    def export_top_stories(self, save_dir_path="hacker_news", date=None, hour=None):
        print("准备导出Hacker News的热门新闻。")
        top_stories = self.fetch_top_stories()  # 获取新闻数据

        if not top_stories:
            print("未找到任何Hacker News的新闻。")
            return None

        # 如果未提供 date 和 hour 参数，使用当前日期和时间
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        if hour is None:
            hour = datetime.now().strftime('%H')

        # 构建存储路径
        dir_path = os.path.join(save_dir_path, date)
        os.makedirs(dir_path, exist_ok=True)  # 确保目录存在

        file_path = os.path.join(dir_path, f'{hour}.md')  # 定义文件路径
        with open(file_path, 'w') as file:
            file.write(f"# Hacker News Top Stories ({date} {hour}:00)\n\n")
            for idx, story in enumerate(top_stories, start=1):
                file.write(f"{idx}. [{story['title']}]({story['link']})\n")

        print(f"Hacker News热门新闻文件生成：{file_path}")
        return file_path


if __name__ == "__main__":
    client = HackerNewsClient()
    dir_path = "/tmp/hacker_news"
    client.export_top_stories(dir_path)  # 默认情况下使用当前日期和时间

```

执行完毕之后可见到诸如下述输出
```
准备导出Hacker News的热门新闻。
准备获取Hacker News的热门新闻。
解析Hacker News的HTML内容。
成功解析 30 条Hacker News新闻。
Hacker News热门新闻文件生成：/tmp/hacker_news/2024-11-04/20.md
```

存储的文本内容诸如:
```
# Hacker News Top Stories (2024-11-04 20:00)

1. [Cheap Thrills, an album cover by Robert Crumb (2020)](https://musicaficionado.blog/2020/01/28/cheap-thrills-an-album-cover-by-robert-crumb/)
2. [The history of Unix's ioctl and signal about window sizes](https://utcc.utoronto.ca/~cks/space/blog/unix/WindowSizeIoctlAndSignal)
3. [Scientists glue two proteins together, driving cancer cells to self-destruct](https://med.stanford.edu/news/all-news/2024/10/protein-cancer.html)
4. [Is yt-dlp/yt-dlp compromised?](https://github.com/yt-dlp/yt-dlp/releases)
5. [An embarrassingly simple approach to recover unlearned knowledge for LLMs](https://arxiv.org/abs/2410.16454)
6. [PropelAuth (YC W22) is hiring Fullstack and Rust engineers](https://www.ycombinator.com/companies/propelauth/jobs)
7. [The Saga of a Celebrated Scientist – and His Rodent Dystopia](https://www.chronicle.com/article/the-saga-of-a-celebrated-scientist-and-his-rodent-dystopia)
8. [Project Sid: Many-agent simulations toward AI civilization](https://github.com/altera-al/project-sid)
9. [The Secret of Ramsey Numbers](https://cacm.acm.org/news/the-secret-of-ramsey-numbers/)
10. [Hertz-dev, the first open-source base model for conversational audio](https://si.inc/hertz-dev/)
11. [I've had a change of heart regarding employee metrics](http://rachelbythebay.com/w/2024/11/03/metrics/)
12. [Touchscreens are out, and tactile controls are back](https://spectrum.ieee.org/touchscreens)
13. [A Hamiltonian Circuit for Rubik's Cube](https://bruce.cubing.net/ham333/rubikhamiltonexplanation.html)
14. [pg_flo – Stream, transform, and re-route PostgreSQL data in real-time](https://www.pgflo.io/)
15. [Ritonavir Form III: A Coincidental Concurrent Discovery](https://pubs.acs.org/doi/10.1021/acs.cgd.2c01017)
16. [Open-source wheeled biped robot](https://github.com/upkie/upkie)
17. [The Submerged Nabataean Temple in Puteoli at Pozzuoli, Italy](https://www.cambridge.org/core/journals/antiquity/article/submerged-nabataean-temple-in-puteoli-at-pozzuoli-italy-first-campaign-of-underwater-research/446AE61E8E3ECBC6CFA7DF6239452967)
18. [Programming languages that blew my mind (2023)](https://yoric.github.io/post/programming-languages-that-blew-my-mind/)
19. [PacCam: Pac-Man controlled with your face](https://eieio.games/paccam/)
20. [Interview gone wrong](https://www.ashu1461.com/interview-gone-wrong/)
21. [gptel: a simple LLM client for Emacs](https://github.com/karthink/gptel)
22. [Top discoveries about ancient people from DNA in 2023](https://johnhawks.net/weblog/the-top-10-discoveries-about-ancient-people-from-dna-in-2023/)
23. [It's a Palworld After All a Lawyer Explains Nintendo vs. Palworld [video]](https://www.youtube.com/watch?v=8apzrwv75i0)
24. [Show HN: Tinder, but to Decide What to Eat](https://whatdinner.com/)
25. [Ask HN: What would you preserve if the internet were to go down tomorrow?](item?id=42030832)
26. [Missing open-source contributor presents a dilemma when accepting their PR](https://bettersoftware.uk/2024/11/03/missing-open-source-contributor-presents-a-dilemma-when-accepting-their-contribution/)
27. [Venvstacks: Virtual Environment Stacks for Python](https://lmstudio.ai/blog/venvstacks)
28. [Unix core utilities implemented in Haskell](https://github.com/Gandalf-/coreutils)
29. [The performance of hashing for similar function detection](https://edmcman.github.io/blog/2024-01-11--fuzzy-hashing-for-code-comparisons/)
30. [Big Data for the Leviathan](https://www.lrb.co.uk/the-paper/v46/n20/tom-johnson/big-data-for-the-leviathan)

```

## 2. Daemon中调用HackerNewsClient
主要通过修改src/daemon_process.py来实现
步骤为2个
1. 定时每天抓取日志并保存到文件. 可见上述的HackerNewsClient
2. 读取md文件并调用llm进行总结
3. 调用对应的notifier进行通知
追加诸如下述
```python
def hn_daily_job(hacker_news_client, report_generator, notifier):
    print("[开始执行定时任务]Hacker News 今日前沿技术趋势")
    # 获取当前日期，并格式化为 'YYYY-MM-DD' 格式
    date = datetime.now().strftime('%Y-%m-%d')
    # 生成每日汇总报告的目录路径
    directory_path = os.path.join('hacker_news', date)
    # 生成每日汇总报告并保存
    report, _ = report_generator.generate_hn_daily_report(directory_path)
    notifier.notify_hn_report(date, report)
    print(f"[定时任务执行完毕]")


# 安排 hn_daily_job 每天早上10点执行一次
schedule.every().day.at("10:00").do(hn_daily_job, hacker_news_client, report_generator, notifier)

```
其中 report_generator.generate_hn_daily_report(directory_path) 用于生成每日汇总报告
可修改src/report_generator.py来实现
- 追加诸如下述.
  - 通过读取目录下的所有文件并合并内容
  - 将其交给llm进行总结
  - 最后将结果保存到文件
```python

    def generate_hn_daily_report(self, directory_path):
        """
        生成 Hacker News 每日汇总的报告，并保存到 hacker_news/tech_trends/ 目录下。
        这里的输入是一个目录路径，其中包含所有由 generate_hn_topic_report 生成的 *_topic.md 文件。
        """
        markdown_content = self._aggregate_topic_reports(directory_path)
        system_prompt = self.prompts.get("hacker_news_daily_report")

        base_name = os.path.basename(directory_path.rstrip('/'))
        report_file_path = os.path.join("hacker_news/tech_trends/", f"{base_name}_trends.md")

        # 确保 tech_trends 目录存在
        os.makedirs(os.path.dirname(report_file_path), exist_ok=True)
        
        report = self.llm.generate_report(system_prompt, markdown_content)
        
        with open(report_file_path, 'w+') as report_file:
            report_file.write(report)
        
        print(f"Hacker News 每日汇总报告已保存到 {report_file_path}")
        return report, report_file_path


    def _aggregate_topic_reports(self, directory_path):
        """
        聚合目录下所有以 '_topic.md' 结尾的 Markdown 文件内容，生成每日汇总报告的输入。
        """
        markdown_content = ""
        for filename in os.listdir(directory_path):
            if filename.endswith("_topic.md"):
                with open(os.path.join(directory_path, filename), 'r') as file:
                    markdown_content += file.read() + "\n"
        return markdown_content
```

## gradio这里就略过了. 比较不属于核心内容.