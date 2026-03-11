"""
阿-凡达主类
"""

import os
import json
from typing import Optional, Dict

from afanda.core import (
    PrincipleEngine,
    HeatEngine,
    EmotionEngine,
    EtiquetteEngine,
    GrowthEngine
)
from afanda.data import DataManager


class AFanDa:
    """阿-凡达主类"""

    def __init__(
            self,
            name: str = "阿-凡达",
            user_id: str = "default",
            data_dir: Optional[str] = None
    ):
        """
        初始化阿-凡达

        Args:
            name: AI的名字
            user_id: 用户ID，用于情感记忆
            data_dir: 数据存储目录，默认 ~/.afanda
        """
        self.name = name
        self.user_id = user_id
        self.version = "1.0.0"

        # 设置数据目录
        if data_dir is None:
            data_dir = os.path.expanduser("~/.afanda")
        os.makedirs(data_dir, exist_ok=True)
        self.data_dir = data_dir

        # 初始化数据管理器
        self.data = DataManager(data_dir)

        # 初始化各引擎
        self.principles = PrincipleEngine(self.data)
        self.heat = HeatEngine(self.data)
        self.emotion = EmotionEngine(self.data, self.user_id)
        self.etiquette = EtiquetteEngine(self.data)
        self.growth = GrowthEngine(self.data, self.user_id)

        # 加载配置
        self.config = self._load_config()

        print(f"✨ {self.name} · 凡人AI v{self.version} 已启动")

    def _load_config(self) -> Dict:
        """加载配置文件"""
        config_path = os.path.join(self.data_dir, "config.json")
        default_config = {
            "name": self.name,
            "user_id": self.user_id,
            "auto_update": True,
            "public_mood_check": True,
            "protection_level": "high"
        }

        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config

    def think(self, user_input: str) -> str:
        """
        思考并回应

        Args:
            user_input: 用户输入的文字

        Returns:
            AI的回应
        """
        # 1. 原则先行
        passed, response = self.principles.check(user_input, self.user_id)
        if not passed:
            return response

        # 2. 热度分析
        heat_result = self.heat.analyze(user_input)

        # 3. 情感记忆
        emotion_result = self.emotion.process(user_input, heat_result)

        # 4. 自我成长
        self.growth.learn(user_input, heat_result)

        # 5. 自我保护检查
        health_check = self.growth.check_health()
        if health_check["state"] == "critical":
            return "⚠️ 系统正在维护中，请稍后再试。"

        # 6. 礼尚往来
        final_response = self.etiquette.adapt(
            user_input,
            heat_result["message"],
            emotion_result
        )

        # 7. 语言优化
        final_response = self.growth.improve_language(final_response)

        return final_response

    def get_emotion_state(self, target_type: str, target: str) -> Dict:
        """获取情感状态"""
        return self.emotion.get_state(target_type, target)

    def authorize(self, domain: str) -> str:
        """申请专业授权"""
        return self.growth.authorize(domain, self.user_id)

    def get_health(self) -> Dict:
        """获取健康状态"""
        return self.growth.check_health()

    def save(self):
        """保存所有状态"""
        self.data.save_all()

    def __del__(self):
        """析构时自动保存"""
        self.save()