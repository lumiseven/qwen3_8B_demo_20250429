# OpenAI API 兼容服务客户端

这个项目提供了Python代码，用于访问OpenAI API兼容的服务，特别是访问本地部署的Qwen3-8B模型。

## 文件说明

- `openai_api_client.py`: 核心API客户端库，提供了三种不同的方法来调用API
- `run_api_client.py`: 运行脚本，提供了命令行界面来使用API客户端

## 安装依赖

在使用这些脚本之前，请确保安装了必要的依赖：

```bash
pip install requests openai
```

## 使用方法

### 直接运行API客户端

```bash
# 运行所有方法
./openai_api_client.py

# 或者使用python命令
python openai_api_client.py
```

### 使用运行脚本

```bash
# 运行所有方法
./run_api_client.py

# 仅使用requests库方法
./run_api_client.py requests

# 仅使用OpenAI库方法
./run_api_client.py openai

# 使用自定义参数和问题
./run_api_client.py custom "请问如何做红烧肉？"
```

## API调用方法

1. **使用requests库**：直接使用Python的requests库发送HTTP请求
2. **使用OpenAI库**：使用官方OpenAI Python库，但指定自定义的base_url
3. **自定义参数**：提供了一个灵活的函数，可以自定义消息和其他参数

## 特殊功能

- **推理过程展示**：脚本会检查并显示模型的推理过程（`reasoning_content`字段），这是Qwen3-8B模型的特殊功能，可以看到模型在生成回复前的思考过程

## 示例

```python
from openai_api_client import chat_with_model

# 自定义消息
messages = [
    {"role": "system", "content": "你是一个旅游顾问"},
    {"role": "user", "content": "推荐三个适合夏季旅游的城市"}
]

# 调用API
result = chat_with_model(messages)
if result:
    print(result["choices"][0]["message"]["content"])
```

## 注意事项

- 这些脚本假设API服务运行在 `http://192.168.3.73:8000/v1/chat/completions`
- 如果需要连接到其他地址，请修改脚本中的URL
- 本地服务可能不需要API密钥，但OpenAI库需要一个值，所以使用了一个占位符 `sk-no-key-required`
