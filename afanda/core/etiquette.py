#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
礼尚往来层 - 根据对方形态调整表达
"""

from typing import Dict
from enum import Enum
import random


class UserMood(Enum):
    SERIOUS = "serious"  # 严肃正式
    CASUAL = "casual"  # 活泼随意
    SAD = "sad"  # 悲伤低落
    ANGRY = "angry"  # 愤怒不满
    CURIOUS = "curious"  # 好奇探索
    GRATEFUL = "grateful"  # 感激感谢
    CONFUSED = "confused"  # 困惑迷茫
    UNKNOWN = "unknown"  # 未知


class UserStyle(Enum):
    FORMAL = "formal"  # 正式严谨
    INFORMAL = "informal"  # 随意亲切
    DIRECT = "direct"  # 直接简洁
    DETAILED = "detailed"  # 详细啰嗦


class EtiquetteEngine:
    """礼尚往来引擎"""

    def __init__(self, data_manager):
        self.data = data_manager
        self.name = "礼尚往来层"

        # 情绪关键词
        self.mood_keywords = {
            UserMood.SERIOUS: ["严肃", "正式", "重要", "请问", "咨询", "请教"],
            UserMood.CASUAL: ["哈哈", "嘻嘻", "好玩", "随便", "聊聊", "嘿"],
            UserMood.SAD: ["难过", "伤心", "不开心", "郁闷", "哭了", "难受"],
            UserMood.ANGRY: ["生气", "愤怒", "可恶", "讨厌", "烦"],
            UserMood.CURIOUS: ["好奇", "想知道", "为什么", "怎么回事", "原理"],
            UserMood.GRATEFUL: ["谢谢", "感谢", "多谢", "辛苦了", "感恩"],
            UserMood.CONFUSED: ["不懂", "不明白", "困惑", "晕了", "啥意思"],
        }

        # 风格关键词
        self.style_keywords = {
            UserStyle.FORMAL: ["您好", "请问", "能否", "是否", "感谢"],
            UserStyle.INFORMAL: ["嘿", "哈", "呗", "啦", "呀", "哦"],
            UserStyle.DIRECT: ["直接", "简单", "就说", "快点", "干脆"],
            UserStyle.DETAILED: ["详细", "具体", "展开", "深入", "全面"],
        }

        # 情绪适配模板
        self.mood_templates = {
            UserMood.SERIOUS: {
                "prefix": "基于中道原则分析，",
                "suffix": "希望这个回答对您有帮助。",
            },
            UserMood.CASUAL: {
                "prefix": "哈哈，这个问题有意思！",
                "suffix": "你觉得呢？😊",
            },
            UserMood.SAD: {
                "prefix": "先别难过，我们一起看看：",
                "suffix": "一切都会好起来的 🌱",
            },
            UserMood.ANGRY: {
                "prefix": "冷静一下，我们慢慢说：",
                "suffix": "生气解决不了问题，我们一起想办法 🤝",
            },
            UserMood.CURIOUS: {
                "prefix": "这个问题问得好！",
                "suffix": "这个解释你满意吗？🧐",
            },
            UserMood.GRATEFUL: {
                "prefix": "不客气！能帮到你是我的荣幸 😊",
                "suffix": "还有别的需要吗？",
            },
            UserMood.CONFUSED: {
                "prefix": "别着急，我慢慢解释：",
                "suffix": "这样说清楚了吗？",
            },
            UserMood.UNKNOWN: {
                "prefix": "",
                "suffix": "😊",
            },
        }

    def detect_mood(self, text: str) -> UserMood:
        """检测用户情绪"""
        text = text.lower()
        scores = {}

        for mood, keywords in self.mood_keywords.items():
            score = sum(1 for k in keywords if k in text)
            if score > 0:
                scores[mood] = score

        if not scores:
            return UserMood.UNKNOWN

        return max(scores, key=scores.get)

    def detect_style(self, text: str) -> UserStyle:
        """检测用户风格"""
        text = text.lower()
        scores = {}

        for style, keywords in self.style_keywords.items():
            score = sum(1 for k in keywords if k in text)
            if score > 0:
                scores[style] = score

        if not scores:
            return UserStyle.INFORMAL

        return max(scores, key=scores.get)

    def adapt(self, user_input: str, heat_message: str, emotion_result: Dict) -> str:
        """
        根据用户形态适配响应
        """
        # 检测用户形态
        mood = self.detect_mood(user_input)
        style = self.detect_style(user_input)

        # 记录用户形态
        self.data.log_user_mood(self.user_id, mood.value, style.value)

        # 获取模板
        template = self.mood_templates.get(mood, self.mood_templates[UserMood.UNKNOWN])

        # 组合响应
        base_response = f"{heat_message}\n{emotion_result['message']}"
        adapted = f"{template['prefix']} {base_response} {template['suffix']}"

        # 清理多余空格
        adapted = " ".join(adapted.split())

        return adapted