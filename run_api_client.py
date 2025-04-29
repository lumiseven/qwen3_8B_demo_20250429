#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
运行OpenAI API兼容服务客户端
这个脚本演示如何使用openai_api_client.py中的函数
"""

import sys
from openai_api_client import (
    call_openai_compatible_api_with_requests,
    call_openai_compatible_api_with_openai_lib,
    chat_with_model
)

def main():
    """主函数，根据命令行参数选择运行方式"""
    
    print("OpenAI API兼容服务测试")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        method = sys.argv[1].lower()
        
        if method == "requests":
            print("使用requests库方法调用API...")
            call_openai_compatible_api_with_requests()
        
        elif method == "openai":
            print("使用OpenAI库方法调用API...")
            call_openai_compatible_api_with_openai_lib()
        
        elif method == "custom":
            print("使用自定义参数调用API...")
            # 可以在这里自定义消息
            custom_messages = [
                {"role": "system", "content": "你是一个厨师助手"},
                {"role": "user", "content": "请给我一个简单的披萨食谱"}
            ]
            
            if len(sys.argv) > 2:
                # 如果提供了自定义问题
                custom_messages[1]["content"] = sys.argv[2]
            
            result = chat_with_model(custom_messages)
            if result:
                # 打印原始响应
                print("\n原始响应:")
                print(f"响应内容: {result}")
                
                # 打印推理内容（如果存在）
                if "choices" in result and len(result["choices"]) > 0 and "message" in result["choices"][0]:
                    message = result["choices"][0]["message"]
                    if "reasoning_content" in message:
                        print("\n推理过程:")
                        print(message["reasoning_content"])
                    
                    if "content" in message:
                        print("\n回复内容:")
                        print(message["content"])
                    else:
                        print("\n回复内容: 无内容")
                else:
                    print("\n无法解析响应")
        
        else:
            print(f"未知方法: {method}")
            print_usage()
    
    else:
        # 默认运行所有方法
        print("运行所有API调用方法...")
        
        print("\n1. 使用requests库方法:")
        call_openai_compatible_api_with_requests()
        
        print("\n2. 使用OpenAI库方法:")
        call_openai_compatible_api_with_openai_lib()
        
        print("\n3. 使用自定义参数方法:")
        custom_messages = [
            {"role": "system", "content": "你是一个厨师助手"},
            {"role": "user", "content": "请给我一个简单的披萨食谱"}
        ]
        
        result = chat_with_model(custom_messages)
        if result:
            # 打印原始响应
            print("\n原始响应:")
            print(f"响应内容: {result}")
            
            # 打印推理内容（如果存在）
            if "choices" in result and len(result["choices"]) > 0 and "message" in result["choices"][0]:
                message = result["choices"][0]["message"]
                if "reasoning_content" in message:
                    print("\n推理过程:")
                    print(message["reasoning_content"])
                
                if "content" in message:
                    print("\n回复内容:")
                    print(message["content"])
                else:
                    print("\n回复内容: 无内容")
            else:
                print("\n无法解析响应")

def print_usage():
    """打印使用说明"""
    print("\n使用方法:")
    print(f"  python {sys.argv[0]} [方法] [自定义问题]")
    print("\n可用方法:")
    print("  requests  - 使用requests库调用API")
    print("  openai    - 使用OpenAI库调用API")
    print("  custom    - 使用自定义参数调用API")
    print("\n示例:")
    print(f"  python {sys.argv[0]}                           # 运行所有方法")
    print(f"  python {sys.argv[0]} requests                  # 仅使用requests库方法")
    print(f"  python {sys.argv[0]} custom '如何做红烧肉?'     # 使用自定义问题")

if __name__ == "__main__":
    main()
