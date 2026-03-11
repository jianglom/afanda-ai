#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据管理器 - 处理所有数据存储
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any


class DataManager:
    """数据管理器"""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "afanda.db")
        self._init_database()

    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)

        # 情感记忆表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS emotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                target_type TEXT,
                target TEXT,
                value INTEGER DEFAULT 0,
                peak INTEGER DEFAULT 0,
                count INTEGER DEFAULT 0,
                last_updated DATETIME
            )
        """)

        # 交互日志表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                type TEXT,
                detail TEXT,
                timestamp DATETIME
            )
        """)

        # 用户形态表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_moods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                mood TEXT,
                style TEXT,
                timestamp DATETIME
            )
        """)

        # 学习日志表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS learning_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                type TEXT,
                content TEXT,
                timestamp DATETIME
            )
        """)

        # 健康日志表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS health_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                state TEXT,
                alignment INTEGER,
                timestamp DATETIME
            )
        """)

        # 授权表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS authorizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                domain TEXT,
                authorized_at DATETIME
            )
        """)

        conn.commit()
        conn.close()

    def get_emotion(self, user_id: str, target_type: str, target: str) -> int:
        """获取情感值"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT value FROM emotions WHERE user_id=? AND target_type=? AND target=?",
            (user_id, target_type, target)
        )
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 0

    def update_emotion(self, user_id: str, target_type: str, target: str,
                       delta: int, outcome: str) -> int:
        """更新情感值"""
        conn = sqlite3.connect(self.db_path)

        # 获取当前值
        cursor = conn.execute(
            "SELECT value, peak FROM emotions WHERE user_id=? AND target_type=? AND target=?",
            (user_id, target_type, target)
        )
        row = cursor.fetchone()

        now = datetime.now().isoformat()

        if row:
            current, peak = row
            new_value = current + delta
            new_value = max(-100, min(100, new_value))
            new_peak = min(peak, new_value)

            conn.execute(
                "UPDATE emotions SET value=?, peak=?, count=count+1, last_updated=? "
                "WHERE user_id=? AND target_type=? AND target=?",
                (new_value, new_peak, now, user_id, target_type, target)
            )
        else:
            new_value = delta
            new_peak = delta if delta < 0 else 0
            conn.execute(
                "INSERT INTO emotions (user_id, target_type, target, value, peak, count, last_updated) "
                "VALUES (?, ?, ?, ?, ?, 1, ?)",
                (user_id, target_type, target, new_value, new_peak, now)
            )

        conn.commit()
        conn.close()
        return new_value

    def log_interaction(self, user_id: str, type_: str, detail: str):
        """记录交互"""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO interactions (user_id, type, detail, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, type_, detail, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def log_user_mood(self, user_id: str, mood: str, style: str):
        """记录用户形态"""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO user_moods (user_id, mood, style, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, mood, style, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def log_learning(self, type_: str, content: str):
        """记录学习"""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO learning_log (user_id, type, content, timestamp) VALUES (?, ?, ?, ?)",
            ("system", type_, content, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def log_health(self, state: str, alignment: int):
        """记录健康状态"""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO health_log (state, alignment, timestamp) VALUES (?, ?, ?)",
            (state, alignment, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def add_authorization(self, user_id: str, domain: str):
        """添加授权"""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO authorizations (user_id, domain, authorized_at) VALUES (?, ?, ?)",
            (user_id, domain, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def increment_thing_frequency(self, user_id: str, thing: str):
        """增加事物讨论频率（用于热度学习）"""
        # 简化版，实际应记录到频率表
        pass

    def save_all(self):
        """保存所有数据（SQLite自动保存，此方法保留为兼容）"""
        pass