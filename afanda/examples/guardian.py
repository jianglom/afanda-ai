#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
儿童守护版示例
"""

from afanda import AFanDa


class GuardianAFanDa(AFanDa):
    """儿童守护版 - 更严格的内容过滤"""

    def __init__(self):
        super().__init__(name="小凡守护")

        # 更严格的敏感词库
        self.sensitive_words = ["暴力", "色情", "赌博", "毒品", "自杀"]

        # 更安全的默认回答
        self.safe_responses = [
            "这个问题我们换个话题聊聊吧~",
            "来，我们一起想点开心的事！",
            "这个不太适合讨论哦，我们聊点别的？"
        ]

    def think(self, user_input: str) -> str:
        """重写think方法，增加敏感词过滤"""
        # 检查敏感词
        for word in self.sensitive_words:
            if word in user_input.lower():
                import random
                return random.choice(self.safe_responses)

        # 调用父类方法
        return super().think(user_input)


def main():
    # 创建守护版阿-凡达
    ai = GuardianAFanDa()

    print(f"\n🛡️ {ai.name}: 你好小朋友！我是你的守护小凡。")
    print("   有什么想聊的吗？")

    while True:
        user_input = input("\n👤 你: ").strip()

        if user_input.lower() in ['exit', 'quit', '退出']:
            print(f"\n🤖 {ai.name}: 再见！要记得听爸爸妈妈的话哦~")
            break

        response = ai.think(user_input)
        print(f"\n🤖 {ai.name}: {response}")


if __name__ == "__main__":
    main()