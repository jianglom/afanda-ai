#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情感层 - 对人、对事的情感记忆
"""

from typing import Dict, Optional
from datetime import datetime
from enum import Enum


class EmotionLevel(Enum):
    TRUSTED = "trusted"  # 可信赖 (>50)
    POSITIVE = "positive"  # 积极 (20-50)
    NEUTRAL = "neutral"  # 中性 (-20-20)
    CAUTIOUS = "cautious"  # 谨慎 (-50 - -20)
    AVOID = "avoid"  # 避开 (-80 - -50)
    SCARRED = "scarred"  # 疤痕 (< -80)


class EmotionEngine:
    """情感引擎"""

    def __init__(self, data_manager, user_id: str):
        self.data = data_manager
        self.user_id = user_id
        self.name = "情感层"

        # 情感阈值
        self.SCAR_THRESHOLD = -80  # 疤痕阈值
        self.AVOID_THRESHOLD = -50  # 避开阈值
        self.CAUTIOUS_THRESHOLD = -20  # 谨慎阈值
        self.POSITIVE_THRESHOLD = 20  # 积极阈值
        self.TRUSTED_THRESHOLD = 50  # 可信赖阈值

        # 情感变化映射
        self.delta_map = {
            "very_good": 20,
            "good": 10,
            "neutral": 0,
            "bad": -10,
            "very_bad": -20,
            "traumatic": -30
        }

    def get_level(self, value: int) -> EmotionLevel:
        """根据情感值获取等级"""
        if value <= self.SCAR_THRESHOLD:
            return EmotionLevel.SCARRED
        elif value <= self.AVOID_THRESHOLD:
            return EmotionLevel.AVOID
        elif value <= self.CAUTIOUS_THRESHOLD:
            return EmotionLevel.CAUTIOUS
        elif value <= self.POSITIVE_THRESHOLD:
            return EmotionLevel.NEUTRAL
        elif value <= self.TRUSTED_THRESHOLD:
            return EmotionLevel.POSITIVE
        else:
            return EmotionLevel.TRUSTED

    def process(self, user_input: str, heat_result: Dict) -> Dict:
        """
        处理情感记忆

        Returns:
            {
                "emotions": 各事物的情感值,
                "levels": 各事物的情感等级,
                "message": 情感信息
            }
        """
        things = heat_result.get("things", [])
        heats = heat_result.get("heats", {})

        emotions = {}
        levels = {}
        messages = []

        for thing in things:
            # 获取当前情感值
            current = self.data.get_emotion(self.user_id, "thing", thing)

            # 根据热度结果确定情感变化
            heat = heats.get(thing, 50)
            if heat >= 80:
                delta = self.delta_map["good"]
                outcome = "good"
            elif heat <= 20:
                delta = self.delta_map["bad"]
                outcome = "bad"
            else:
                delta = self.delta_map["neutral"]
                outcome = "neutral"

            # 更新情感
            new_value = self.data.update_emotion(
                self.user_id, "thing", thing, delta, outcome
            )

            emotions[thing] = new_value
            level = self.get_level(new_value)
            levels[thing] = level.value

            # 生成情感提示
            if level == EmotionLevel.SCARRED:
                messages.append(f"⚠️ 关于{thing}，之前有过不愉快的经历。")
            elif level == EmotionLevel.AVOID:
                messages.append(f"😓 关于{thing}，之前有些不太愉快。")
            elif level == EmotionLevel.CAUTIOUS:
                messages.append(f"🤔 关于{thing}，需要谨慎对待。")
            elif level == EmotionLevel.POSITIVE:
                messages.append(f"😊 关于{thing}，之前体验不错。")
            elif level == EmotionLevel.TRUSTED:
                messages.append(f"✨ 关于{thing}，你一直很喜欢！")

        return {
            "emotions": emotions,
            "levels": levels,
            "message": "\n".join(messages) if messages else "情感状态正常。"
        }

    def get_state(self, target_type: str, target: str) -> Dict:
        """获取指定目标的情感状态"""
        value = self.data.get_emotion(self.user_id, target_type, target)
        level = self.get_level(value)

        return {
            "value": value,
            "level": level.value,
            "type": target_type,
            "target": target
        }