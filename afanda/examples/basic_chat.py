#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础对话示例
"""

from afanda import AFanDa


def main():
    # 创建阿-凡达
    ai = AFanDa(name="我的小凡")

    print(f"\n🤖 {ai.name}: 你好！我是你的阿-凡达。")
    print("   有什么想聊的吗？")

    while True:
        user_input = input("\n👤 你: ").strip()

        if user_input.lower() in ['exit', 'quit', '退出']:
            print(f"\n🤖 {ai.name}: 再见！愿你一切顺利~")
            break

        response = ai.think(user_input)
        print(f"\n🤖 {ai.name}: {response}")


if __name__ == "__main__":
    main()