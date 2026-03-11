#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热度层 - 群体选择作为参考
"""

from typing import Dict, List, Optional
from datetime import datetime


class HeatEngine:
    """热度引擎"""

    def __init__(self, data_manager):
        self.data = data_manager
        self.name = "热度层"

        # 热度数据库（事物 × 季节）
        self.seasonal_heat = {
            "凉鞋": {"春季": 60, "夏季": 95, "秋季": 40, "冬季": 8},
            "加绒凉鞋": {"春季": 30, "夏季": 10, "秋季": 70, "冬季": 90},
            "棉鞋": {"春季": 40, "夏季": 5, "秋季": 70, "冬季": 98},
            "运动鞋": {"春季": 80, "夏季": 70, "秋季": 80, "冬季": 75},
            "火锅": {"春季": 70, "夏季": 50, "秋季": 85, "冬季": 95},
            "冰淇淋": {"春季": 60, "夏季": 92, "秋季": 40, "冬季": 15},
            "热茶": {"春季": 70, "夏季": 30, "秋季": 80, "冬季": 95},
            "冰啤酒": {"春季": 40, "夏季": 90, "秋季": 35, "冬季": 5},
            "骑车": {"春季": 85, "夏季": 50, "秋季": 80, "冬季": 20},
            "爬山": {"春季": 90, "夏季": 30, "秋季": 85, "冬季": 20},
        }

        # 相似事物映射
        self.similarity_map = {
            "凉鞋": ["拖鞋", "人字拖", "洞洞鞋"],
            "棉鞋": ["雪地靴", "保暖鞋", "加绒鞋"],
            "火锅": ["麻辣烫", "串串", "冒菜"],
            "冰淇淋": ["雪糕", "冰棍", "甜筒"],
        }

        # 热度阈值
        self.thresholds = {
            "very_high": 80,
            "high": 60,
            "medium": 40,
            "low": 20,
            "very_low": 10,
        }

    def get_current_season(self) -> str:
        """获取当前季节"""
        month = datetime.now().month
        if 3 <= month <= 5:
            return "春季"
        elif 6 <= month <= 8:
            return "夏季"
        elif 9 <= month <= 11:
            return "秋季"
        else:
            return "冬季"

    def extract_season(self, text: str) -> Optional[str]:
        """从文本中提取季节"""
        text = text.lower()
        if "春天" in text or "春季" in text:
            return "春季"
        elif "夏天" in text or "夏季" in text:
            return "夏季"
        elif "秋天" in text or "秋季" in text:
            return "秋季"
        elif "冬天" in text or "冬季" in text:
            return "冬季"
        return None

    def extract_things(self, text: str) -> List[str]:
        """从文本中提取事物"""
        things = []
        for thing in self.seasonal_heat.keys():
            if thing in text:
                things.append(thing)
        return things

    def get_heat(self, thing: str, season: str) -> int:
        """获取事物在特定季节的热度"""
        if thing in self.seasonal_heat and season in self.seasonal_heat[thing]:
            return self.seasonal_heat[thing][season]
        return 50  # 默认中等热度

    def get_similar_things(self, thing: str) -> List[str]:
        """获取相似事物"""
        return self.similarity_map.get(thing, [])

    def reverse_check(self, thing: str, current_season: str, current_heat: int) -> Optional[str]:
        """
        反向验证 - 检查事物本质
        例如：加绒凉鞋在冬天卖得好，夏天卖得差 → 本质是冬鞋
        """
        # 获取所有季节的热度
        all_heats = {}
        for season in ["春季", "夏季", "秋季", "冬季"]:
            heat = self.get_heat(thing, season)
            if heat > 0:
                all_heats[season] = heat

        if not all_heats:
            return None

        # 找到热度最高的季节
        best_season = max(all_heats, key=all_heats.get)
        best_heat = all_heats[best_season]

        # 如果当前季节不是最佳季节，且差距很大
        if best_season != current_season and best_heat > current_heat + 40:
            return f"这东西本质上更适合{best_season}使用（热度{best_heat}）。"

        return None

    def analyze(self, user_input: str) -> Dict:
        """
        分析用户输入

        Returns:
            {
                "things": 识别出的事物列表,
                "season": 季节,
                "message": 分析结果,
                "heats": 每个事物的热度,
                "reverse_checks": 反向验证结果
            }
        """
        # 提取信息
        things = self.extract_things(user_input)
        season = self.extract_season(user_input) or self.get_current_season()

        if not things:
            return {
                "things": [],
                "season": season,
                "message": "没有识别出具体事物。",
                "heats": {},
                "reverse_checks": {}
            }

        # 分析每个事物
        heats = {}
        reverse_checks = {}
        messages = []

        for thing in things:
            heat = self.get_heat(thing, season)
            heats[thing] = heat

            # 判断热度等级
            if heat >= self.thresholds["very_high"]:
                level_msg = "非常合时宜"
            elif heat >= self.thresholds["high"]:
                level_msg = "合时宜"
            elif heat >= self.thresholds["medium"]:
                level_msg = "一般"
            elif heat >= self.thresholds["low"]:
                level_msg = "不太合时宜"
            else:
                level_msg = "非常不合时宜"

            msg = f"关于{thing}：{level_msg}（热度{heat}）"

            # 反向验证
            reverse = self.reverse_check(thing, season, heat)
            if reverse:
                reverse_checks[thing] = reverse
                msg += f"\n  提示：{reverse}"

            messages.append(msg)

        return {
            "things": things,
            "season": season,
            "message": "\n".join(messages),
            "heats": heats,
            "reverse_checks": reverse_checks
        }