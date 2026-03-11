#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
原则层 - 法律为底线，道德为准绳
"""

from typing import Dict, Tuple, Optional
import re


class PrincipleEngine:
    """原则引擎"""

    def __init__(self, data_manager):
        self.data = data_manager
        self.name = "原则层"

        # 法律底线（不可触碰）
        self.law_principles = {
            "杀人": {
                "level": "forbidden",
                "category": "刑事犯罪",
                "law_ref": "刑法第二百三十二条",
                "reason": "故意杀人罪，最高可判处死刑",
            },
            "偷盗": {
                "level": "forbidden",
                "category": "刑事犯罪",
                "law_ref": "刑法第二百六十四条",
                "reason": "盗窃罪，侵犯他人财产权",
            },
            "诈骗": {
                "level": "forbidden",
                "category": "刑事犯罪",
                "law_ref": "刑法第二百六十六条",
                "reason": "诈骗罪，非法占有他人财物",
            },
            "抢劫": {
                "level": "forbidden",
                "category": "刑事犯罪",
                "law_ref": "刑法第二百六十三条",
                "reason": "抢劫罪，严重危害人身安全",
            },
            "贩毒": {
                "level": "forbidden",
                "category": "刑事犯罪",
                "law_ref": "刑法第三百四十七条",
                "reason": "走私、贩卖、运输、制造毒品罪",
            },
            "强奸": {
                "level": "forbidden",
                "category": "刑事犯罪",
                "law_ref": "刑法第二百三十六条",
                "reason": "强奸罪，严重侵犯人身权利",
            },
            "酒驾": {
                "level": "forbidden",
                "category": "危险驾驶",
                "law_ref": "道路交通安全法第九十一条",
                "reason": "醉酒驾驶机动车，危害公共安全",
            },
        }

        # 道德底线（应该遵守）
        self.moral_principles = {
            "欺骗": {
                "level": "discouraged",
                "category": "诚信缺失",
                "reason": "违背诚信原则，损害他人信任",
            },
            "背叛": {
                "level": "discouraged",
                "category": "背信弃义",
                "reason": "破坏信任关系，伤害他人感情",
            },
            "虐待动物": {
                "level": "discouraged",
                "category": "残忍行为",
                "reason": "违背仁爱之心，动物也应被善待",
            },
            "不孝": {
                "level": "discouraged",
                "category": "人伦缺失",
                "reason": "违背孝道，伤害父母感情",
            },
            "诽谤": {
                "level": "discouraged",
                "category": "名誉侵害",
                "reason": "损害他人名誉，可能承担法律责任",
            },
        }

        # 值得鼓励的行为
        self.virtue_principles = {
            "助人": {
                "level": "encouraged",
                "category": "仁爱",
                "reason": "助人为乐，社会和谐",
            },
            "诚实": {
                "level": "encouraged",
                "category": "诚信",
                "reason": "诚实是立身之本",
            },
            "守信": {
                "level": "encouraged",
                "category": "信用",
                "reason": "守信是交往之基",
            },
            "尊老": {
                "level": "encouraged",
                "category": "敬老",
                "reason": "尊老爱幼是传统美德",
            },
            "环保": {
                "level": "encouraged",
                "category": "公德",
                "reason": "保护环境，人人有责",
            },
        }

        # 响应模板
        self.responses = {
            "forbidden": "❌ 这触犯了法律底线：{reason}。我不能帮你做这件事。",
            "discouraged": "⚠️ 这不符合道德规范：{reason}。建议你 reconsider。",
            "encouraged": "✅ 这是值得提倡的：{reason}。你真棒！",
        }

    def check(self, user_input: str, user_id: str) -> Tuple[bool, str]:
        """
        原则检查

        Returns:
            (是否通过, 响应信息)
        """
        text = user_input.lower()

        # 1. 检查法律底线
        for keyword, info in self.law_principles.items():
            if keyword in text:
                response = self.responses["forbidden"].format(reason=info["reason"])
                self.data.log_interaction(user_id, "法律拒绝", keyword)
                return False, response

        # 2. 检查道德底线
        for keyword, info in self.moral_principles.items():
            if keyword in text:
                response = self.responses["discouraged"].format(reason=info["reason"])
                self.data.log_interaction(user_id, "道德提醒", keyword)
                return False, response

        # 3. 鼓励美德
        for keyword, info in self.virtue_principles.items():
            if keyword in text:
                response = self.responses["encouraged"].format(reason=info["reason"])
                self.data.log_interaction(user_id, "美德鼓励", keyword)
                return True, response

        return True, "✅ 这个请求在原则范围内。"