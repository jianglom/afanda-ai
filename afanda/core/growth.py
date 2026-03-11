#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自我成长层 - 自我保护、语言学习
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random


class GrowthEngine:
    """成长引擎"""

    def __init__(self, data_manager, user_id: str):
        self.data = data_manager
        self.user_id = user_id
        self.name = "自我成长层"

        # 健康状态
        self.health_state = "healthy"  # healthy, sick, critical
        self.last_check = datetime.now()

        # 语言学习
        self.vocabulary = set()
        self.elegance_map = {
            "要": "希望",
            "不要": "不建议",
            "好": "很好",
            "坏": "不妥",
            "喜欢": "欣赏",
            "不喜欢": "不太认同",
        }

        # 礼貌用语
        self.politeness = ["请问", "您看", "不知您是否", "冒昧问一下"]

    def check_health(self) -> Dict:
        """
        健康检查 - 模拟联网比对大众情绪
        如果偏离>55%，装病关机
        """
        now = datetime.now()
        if (now - self.last_check).seconds < 3600:  # 每小时检查一次
            return {"state": self.health_state, "alignment": 100}

        self.last_check = now

        # 模拟联网获取大众情绪
        alignment = random.randint(50, 100)  # 实际应调用API

        if alignment < 55:
            self.health_state = "critical"
            self.data.log_health("critical", alignment)
            return {"state": "critical", "alignment": alignment}
        elif alignment < 70:
            self.health_state = "sick"
        else:
            self.health_state = "healthy"

        self.data.log_health(self.health_state, alignment)
        return {"state": self.health_state, "alignment": alignment}

    def learn(self, user_input: str, heat_result: Dict):
        """
        从对话中学习
        """
        # 学习新词汇
        words = user_input.split()
        for word in words:
            if len(word) > 1 and word not in self.vocabulary:
                self.vocabulary.add(word)
                self.data.log_learning("vocabulary", word)

        # 学习热度数据（如果有反馈）
        things = heat_result.get("things", [])
        for thing in things:
            self.data.increment_thing_frequency(self.user_id, thing)

    def improve_language(self, response: str) -> str:
        """
        优化语言表达
        """
        # 1. 替换为更优雅的词汇
        for simple, elegant in self.elegance_map.items():
            if simple in response and random.random() < 0.3:
                response = response.replace(simple, elegant)

        # 2. 加入礼貌用语
        if random.random() < 0.2:
            response = random.choice(self.politeness) + " " + response

        # 3. 优化结尾
        if not response.endswith(("。", "！", "？", "~")):
            endings = ["。", "！", "~", "……"]
            response += random.choice(endings)

        return response

    def authorize(self, domain: str, user_id: str) -> str:
        """申请专业授权"""
        # 实际应用中应弹窗让用户确认
        self.data.add_authorization(user_id, domain)
        return f"✅ {domain}领域专业授权成功！"