#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenAI API 兼容服务客户端
这个脚本演示如何使用Python访问OpenAI API兼容的服务
"""

import json
import requests
from typing import Dict, List, Any, Optional

# 方法一：使用requests库直接发送请求
def call_openai_compatible_api_with_requests():
    """使用requests库直接调用OpenAI兼容API"""
    
    # API端点
    url = "http://192.168.3.73:8000/v1/chat/completions"
    
    # 请求头
    headers = {
        "Content-Type": "application/json"
    }
    
    # 请求体
    payload = {
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
    
    # 发送POST请求
    response = requests.post(url, headers=headers, json=payload)
    
    # 检查响应状态
    if response.status_code == 200:
        result = response.json()
        print("请求成功！")
        
        # 打印推理内容（如果存在）
        if "reasoning_content" in result["choices"][0]["message"]:
            print("\n推理过程:")
            print(result["choices"][0]["message"]["reasoning_content"])
        
        print("\n回复内容:")
        print(result["choices"][0]["message"]["content"])
        return result
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(response.text)
        return None

# 方法二：使用OpenAI库
def call_openai_compatible_api_with_openai_lib():
    """使用OpenAI库调用OpenAI兼容API"""
    try:
        import openai
    except ImportError:
        print("OpenAI库未安装，请先运行: pip install openai")
        return None
    
    # 配置客户端使用本地服务
    client = openai.OpenAI(
        base_url="http://192.168.3.73:8000/v1",
        api_key="sk-no-key-required"  # 本地服务可能不需要API密钥，但OpenAI库需要一个值
    )
    
    try:
        # 创建聊天完成请求
        response = client.chat.completions.create(
            model="Qwen3-8B",
            messages=[
                {"role": "system", "content": "你是一个助手"},
                {"role": "user", "content": "如何制作西红柿炒鸡蛋"}
            ],
            temperature=0.6,
            top_p=0.95,
            max_tokens=12800,
            # OpenAI库可能不直接支持top_k参数，但服务端会处理
        )
        
        print("请求成功！")
        
        # 打印推理内容（如果存在）
        if hasattr(response.choices[0].message, "reasoning_content"):
            print("\n推理过程:")
            print(response.choices[0].message.reasoning_content)
        
        print("\n回复内容:")
        print(response.choices[0].message.content)
        return response
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return None

# 自定义参数的函数
def chat_with_model(
    messages: List[Dict[str, str]], 
    model: str = "Qwen3-8B",
    temperature: float = 0.6,
    top_p: float = 0.95,
    top_k: int = 20,
    max_tokens: int = 12800
) -> Optional[Dict[str, Any]]:
    """
    与模型进行对话
    
    Args:
        messages: 对话消息列表
        model: 模型名称
        temperature: 温度参数
        top_p: top_p参数
        top_k: top_k参数
        max_tokens: 最大生成token数
        
    Returns:
        API响应或None（如果请求失败）
    """
    url = "http://192.168.3.73:8000/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_tokens": max_tokens
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    print("=== 使用requests库调用API ===")
    call_openai_compatible_api_with_requests()
    
    print("\n=== 使用OpenAI库调用API ===")
    call_openai_compatible_api_with_openai_lib()
    
    print("\n=== 使用自定义参数调用API ===")
    custom_messages = [
        {"role": "system", "content": "你是一个厨师助手"},
        {"role": "user", "content": "请给我一个简单的披萨食谱"}
    ]
    
    result = chat_with_model(custom_messages)
    if result:
        # 打印推理内容（如果存在）
        if "reasoning_content" in result["choices"][0]["message"]:
            print("\n推理过程:")
            print(result["choices"][0]["message"]["reasoning_content"])
            
        print("\n回复内容:")
        print(result["choices"][0]["message"]["content"])
