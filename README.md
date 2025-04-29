# 本地 qwen3-8B 测试

## modelscope 下载模型

```sh
cd ~/D2/qwen
modelscope download --model="Qwen/Qwen3-8B" --local_dir ./Qwen3-8B
```

## 使用vllm 启动

```sh
cd ~/D2/qwen
vllm serve Qwen3-8B --dtype=half --enable-reasoning --reasoning-parser deepseek_r1 --max_model_len=15840 --gpu_memory_utilization=0.91
```

## 使用sglang 启动

```sh
uv pip install "sglang[all]>=0.4.6"
```

```sh
sudo apt install gcc-11 g++-11
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 110
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 110
```

```sh
cd ~/D2/qwen
python -m sglang.launch_server --model-path Qwen3-8B --reasoning-parser qwen3 --host 0.0.0.0
# default port 30000
```

## curl 测试

```sh
curl --location 'http://192.168.3.73:8000/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data '{
  "model": "Qwen3-8B",
  "messages": [
    {"role": "system", "content": "你是一个助手"},
    {"role": "user", "content": "如何制作西红柿炒鸡蛋"}
  ],
  "temperature": 0.6,
  "top_p": 0.95,
  "top_k": 20,
  "max_tokens": 12800
}
'
```

## openai-api compatible 测试

```sh
conda create --name pyt20250429 python==3.12
```

[API 测试](API_README.md)

## 简单的压力测试

(使用了: `"chat_template_kwargs": {"enable_thinking": false}`)

[pressure_test.py](pressure_test.py)
