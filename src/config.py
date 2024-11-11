import json
import os


class Config:
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            
            self.email = config.get('email', {})
            self.email['password'] = os.getenv('EMAIL_PASSWORD', self.email.get('password', ''))

            # 加载 GitHub 相关配置
            github_config = config.get('github', {})
            self.github_token = os.getenv('GITHUB_TOKEN', github_config.get('token'))
            self.subscriptions_file = github_config.get('subscriptions_file')
            self.freq_days = github_config.get('progress_frequency_days', 1)
            self.exec_time = github_config.get('progress_execution_time', "08:00")

            # 加载 LLM 相关配置
            llm_config = config.get('llm', {})
            self.llm_model_type = llm_config.get('model_type', 'openai')
            self.openai_model_name = llm_config.get('openai_model_name', 'gpt-4o-mini')
            self.openai_api_base = llm_config.get('openai_base_url', '')
            self.openai_api_key = llm_config.get('openai_api_key', '')
            if not self.openai_api_key:
                self.openai_api_key = os.getenv('OPENAI_API_KEY', '')

            self.ollama_model_name = llm_config.get('ollama_model_name', 'llama3')
            self.ollama_api_url = llm_config.get('ollama_api_url', 'http://localhost:11434/api/chat')

            # 加载报告类型配置
            self.report_types = config.get('report_types', ["github", "hacker_news", "science_news_hours_topic"])  # 默认报告类型

            # 加载 Slack 配置
            slack_config = config.get('slack', {})
            self.slack_webhook_url = slack_config.get('webhook_url')

            # 加载 science_news 配置
            self.science_news = config.get('science_news', {})
            self.science_news_url = self.science_news.get('url', "")
            self.scienct_news_key = self.science_news.get('key', "")

            # 加载企业微信webhook配置
            wecom_config = config.get('wecom_webhook', {})
            self.wecom_webhook_url = wecom_config.get('url', "")
            self.wecom_key = wecom_config.get('key', "")
