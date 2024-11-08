# 作业说明
1.在 GitHubSentinel v0.5 基础上，扩展实现 Hacker News 趋势报告生成。实现优先级：Daemon（Required） > Graido > Command

2.[可选] 扩展 GitHubSentinel v0.6，使用 Ollama 私有化部署的大模型服务，完成作业 1

作业提交方式：讲代码仓库的链接复制粘贴至下方的评论框提交即可。

# 作业解析
1.的部分见week_3_1.md的内容
2.的部分主要参考ollama的部署. 实现在本地部署大模型(GPU也可以)
- 部署模型
- 实现模型的接入

# 作业实现
## 部署ollama(mac版本)
参考文档: https://github.com/ollama/ollama?tab=readme-ov-file

## 部署完毕之后可看到ollama
使用如下命令可启动模型
```bash
ollama run llama3.2
```

## 启动完毕之后参考如下命令进行调用
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [
    { "role": "user", "content": "why is the sky blue?" }
  ]
}'
```

## 实现模型的接入
主要修改 llm.py文件, 为其增加一个方法
诸如下述方案,其中self.config.ollama_model_name 需要再你的Python的类的基础声明中写好模型名称: "llama3.2"
配置部分进行适配即可.
```python
    def _generate_report_ollama(self, messages):
        """
        使用 Ollama LLaMA 模型生成报告。

        :param messages: 包含系统提示和用户内容的消息列表。
        :return: 生成的报告内容。
        """
        print(f"使用 Ollama {self.config.ollama_model_name} 模型生成报告。")
        try:
            payload = {
                "model": self.config.ollama_model_name,  # 使用配置中的Ollama模型名称
                "messages": messages,
                "max_tokens": 4000,
                "temperature": 0.7,
                "stream": False
            }

            response = requests.post(self.api_url, json=payload)  # 发送POST请求到Ollama API
            response_data = response.json()

            # 调试输出查看完整的响应结构
            print("Ollama 响应: {}", response_data)

            # 直接从响应数据中获取 content
            message_content = response_data.get("message", {}).get("content", None)
            if message_content:
                return message_content  # 返回生成的报告内容
            else:
                print("无法从响应中提取报告内容。")
                raise ValueError("Ollama API 返回的响应结构无效")
        except Exception as e:
            print(f"生成报告时发生错误：{e}")
            raise
```

## 剩余command和graido的实现 比较次要, 主要是用于适配配置和模型.这里不做赘述.