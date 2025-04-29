# OpenAI API 兼容服务压力测试

这个脚本用于对OpenAI API兼容服务进行压力测试，测试服务器的处理能力。

## 功能特点

- 每秒发送1个请求（1 QPS）
- 持续30秒
- 使用30个不同的问题
- 记录响应时间和成功率
- 生成详细的测试报告

## 使用方法

### 前提条件

确保已安装必要的依赖：

```bash
pip install openai statistics
```

### 运行测试

1. 激活conda环境：

```bash
conda activate pyt20250429
```

2. 运行压力测试：

```bash
# 直接运行（使用默认参数：1 QPS，持续30秒）
./pressure_test.py

# 或者使用python命令
python pressure_test.py
```

## 测试结果

测试完成后，脚本会：

1. 在控制台显示测试摘要，包括：
   - 总请求数
   - 成功请求数
   - 失败请求数
   - 成功率
   - 平均响应时间
   - 最小响应时间
   - 最大响应时间

2. 生成一个详细的测试报告文件（`pressure_test_results_YYYYMMDD_HHMMSS.txt`），包含：
   - 测试参数
   - 每个请求的详细信息
   - 响应预览
   - 错误信息（如果有）

## 自定义测试

如果需要自定义测试参数，可以修改脚本中的以下部分：

1. 修改QPS和持续时间：
   ```python
   # 在脚本末尾修改
   run_pressure_test(qps=1, duration=30)
   ```

2. 修改问题列表：
   ```python
   # 修改QUESTIONS列表
   QUESTIONS = [
       "问题1",
       "问题2",
       # ...
   ]
   ```

3. 修改API参数：
   ```python
   # 在make_api_request函数中修改
   response = client.chat.completions.create(
       model="Qwen3-8B",
       messages=[...],
       temperature=0.6,
       # 其他参数...
   )
   ```

## 注意事项

- 测试会生成大量日志，可能会占用终端空间
- 如果服务器负载过高，可能会导致请求失败或响应时间增加
- 测试结果会保存在当前目录下的文本文件中
