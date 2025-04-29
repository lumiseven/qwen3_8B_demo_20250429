#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenAI API 兼容服务压力测试
每秒发送1个请求，持续30秒，使用30个不同的问题
使用异步方式确保每秒准确发送一个请求
"""

import time
import asyncio
import openai
import statistics
from datetime import datetime
from typing import Dict, List, Any, Optional

# 配置OpenAI客户端
client = openai.AsyncOpenAI(
    base_url="http://192.168.3.73:8000/v1",
    api_key="sk-no-key-required"  # 本地服务可能不需要API密钥，但OpenAI库需要一个值
)

# 30个不同的问题
QUESTIONS = [
    "什么是人工智能？",
    "如何学习编程？",
    "请介绍一下Python语言的特点",
    "量子计算的基本原理是什么？",
    "如何制作一个简单的网站？",
    "区块链技术有哪些应用？",
    "机器学习和深度学习的区别是什么？",
    "如何有效地学习一门外语？",
    "请推荐几本科幻小说",
    "如何保持健康的生活方式？",
    "气候变化对地球的影响有哪些？",
    "太阳系有哪些行星？",
    "如何做好时间管理？",
    "人类历史上最重要的发明是什么？",
    "如何培养创造力？",
    "大数据分析的基本步骤是什么？",
    "如何有效地进行团队协作？",
    "请介绍一下中国的传统节日",
    "如何制作一道简单的家常菜？",
    "世界上最高的山峰是哪座？",
    "如何应对工作压力？",
    "请介绍几种常见的投资方式",
    "如何保护个人隐私和数据安全？",
    "人工智能可能带来哪些伦理问题？",
    "如何提高阅读理解能力？",
    "请介绍几种有效的学习方法",
    "如何培养良好的阅读习惯？",
    "未来的交通工具可能是什么样的？",
    "如何开始写作？",
    "请介绍几种流行的音乐风格"
]

async def make_api_request(question: str, request_id: int) -> Dict[str, Any]:
    """
    异步发送API请求并返回结果
    
    Args:
        question: 要发送的问题
        request_id: 请求ID
        
    Returns:
        包含响应时间和响应内容的字典
    """
    print(f"开始请求 {request_id}: {question}")
    start_time = time.time()
    success = False
    response_content = ""
    error_message = ""
    content = ""
    reasoning_content = ""
    
    try:
        # 创建聊天完成请求
        response = await client.chat.completions.create(
            model="Qwen3-8B",
            messages=[
                {"role": "system", "content": "你是一个助手"},
                {"role": "user", "content": question}
            ],
            temperature=0.6,
            top_p=0.95,
            max_tokens=100,  # 限制token数量以加快响应速度
            extra_body={"chat_template_kwargs": {"enable_thinking": False}},  # 禁用推理
        )
        
        success = True
        response_dict = response.model_dump()
        
        # 尝试获取响应内容和推理内容
        try:
            # 尝试直接从字典中获取内容
            message_dict = response_dict.get('choices', [{}])[0].get('message', {})
            content = message_dict.get('content', '')
            reasoning_content = message_dict.get('reasoning_content', '')
            
            response_preview = ""
            if content:
                response_preview += f"内容: {content[:50]}..." if len(content) > 50 else f"内容: {content}"
            else:
                response_preview += "内容: 无"
                
            if reasoning_content:
                response_preview += f"\n推理内容: {reasoning_content[:50]}..." if len(reasoning_content) > 50 else f"\n推理内容: {reasoning_content}"
            else:
                response_preview += "\n推理内容: 无"
                
            response_content = response_preview
            
            # 如果从字典获取失败，尝试从对象中获取
            if not content and not reasoning_content:
                message = response.choices[0].message
                content = message.content if hasattr(message, 'content') else ""
                reasoning_content = message.reasoning_content if hasattr(message, 'reasoning_content') else ""
                
                response_preview = ""
                if content:
                    response_preview += f"内容: {content[:50]}..." if len(content) > 50 else f"内容: {content}"
                else:
                    response_preview += "内容: 无"
                    
                if reasoning_content:
                    response_preview += f"\n推理内容: {reasoning_content[:50]}..." if len(reasoning_content) > 50 else f"\n推理内容: {reasoning_content}"
                else:
                    response_preview += "\n推理内容: 无"
                    
                response_content = response_preview
        except Exception as e:
            response_content = f"无法获取响应内容: {str(e)}"
        
    except Exception as e:
        error_message = str(e)
    
    end_time = time.time()
    response_time = end_time - start_time
    
    result = {
        "request_id": request_id,
        "question": question,
        "success": success,
        "response_time": response_time,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "response_preview": response_content if success else "",
        "error": error_message if not success else "",
        "content": content if success and content else "",
        "reasoning_content": reasoning_content if success and reasoning_content else ""
    }
    
    # 打印结果
    if success:
        print(f"✅ 请求 {request_id} 成功 - 响应时间: {response_time:.2f}秒")
        print(f"预览: {result['response_preview']}")
    else:
        print(f"❌ 请求 {request_id} 失败 - 响应时间: {response_time:.2f}秒")
        print(f"错误: {error_message}")
    
    print("-" * 40)
    
    return result

async def run_pressure_test(qps: int = 1, duration: int = 30) -> None:
    """
    运行压力测试，确保每秒发送固定数量的请求
    
    Args:
        qps: 每秒查询数
        duration: 测试持续时间（秒）
    """
    print(f"开始压力测试: {qps} QPS, 持续 {duration} 秒")
    print("=" * 80)
    
    total_requests = min(duration * qps, len(QUESTIONS))
    results = []
    tasks = []
    
    # 创建一个事件循环来调度请求
    start_time = time.time()
    
    for i in range(total_requests):
        question = QUESTIONS[i % len(QUESTIONS)]
        
        # 计算这个请求应该在什么时间发送
        scheduled_time = start_time + (i / qps)
        
        # 等待直到应该发送请求的时间
        now = time.time()
        if scheduled_time > now:
            await asyncio.sleep(scheduled_time - now)
        
        # 创建请求任务并添加到任务列表
        task = asyncio.create_task(make_api_request(question, i+1))
        tasks.append(task)
    
    # 等待所有请求完成
    results = await asyncio.gather(*tasks)
    
    # 计算统计数据
    successful_requests = sum(1 for r in results if r["success"])
    failed_requests = total_requests - successful_requests
    success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
    
    response_times = [r["response_time"] for r in results if r["success"]]
    avg_response_time = statistics.mean(response_times) if response_times else 0
    min_response_time = min(response_times) if response_times else 0
    max_response_time = max(response_times) if response_times else 0
    
    # 打印测试结果
    print("\n测试结果摘要")
    print("=" * 80)
    print(f"总请求数: {total_requests}")
    print(f"成功请求: {successful_requests}")
    print(f"失败请求: {failed_requests}")
    print(f"成功率: {success_rate:.2f}%")
    print(f"平均响应时间: {avg_response_time:.2f}秒")
    print(f"最小响应时间: {min_response_time:.2f}秒")
    print(f"最大响应时间: {max_response_time:.2f}秒")
    
    # 保存详细结果到文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pressure_test_results_{timestamp}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("压力测试详细结果\n")
        f.write("=" * 80 + "\n")
        f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"QPS: {qps}\n")
        f.write(f"持续时间: {duration}秒\n")
        f.write(f"总请求数: {total_requests}\n")
        f.write(f"成功率: {success_rate:.2f}%\n")
        f.write(f"平均响应时间: {avg_response_time:.2f}秒\n\n")
        
        f.write("详细请求记录:\n")
        f.write("-" * 80 + "\n")
        
        # 按请求ID排序结果
        sorted_results = sorted(results, key=lambda r: r["request_id"])
        
        for result in sorted_results:
            f.write(f"请求 {result['request_id']}:\n")
            f.write(f"  问题: {result['question']}\n")
            f.write(f"  时间戳: {result['timestamp']}\n")
            f.write(f"  状态: {'成功' if result['success'] else '失败'}\n")
            f.write(f"  响应时间: {result['response_time']:.2f}秒\n")
            
            if result['success']:
                f.write(f"  响应预览:\n{result['response_preview'] if result['response_preview'] else '无响应内容'}\n")
                
                # 写入完整内容和推理内容
                if result['content']:
                    f.write(f"  完整内容: {result['content']}\n")
                if result['reasoning_content']:
                    f.write(f"  完整推理内容: {result['reasoning_content']}\n")
            else:
                f.write(f"  错误: {result['error']}\n")
            
            f.write("-" * 40 + "\n")
    
    print(f"\n详细结果已保存到文件: {filename}")

if __name__ == "__main__":
    # 默认参数: 1 QPS, 持续30秒
    asyncio.run(run_pressure_test(qps=1, duration=30))
