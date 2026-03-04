"""
Money Tracker v2 - 数据库模块
支持多模块账本、版本迁移、勾选统计
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional

# 当前数据库版本
CURRENT_DB_VERSION = 2


class Database:
    """SQLite数据库管理类 - 支持多模块"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            app_data = os.path.join(os.path.expanduser("~"), ".money_tracker")
            os.makedirs(app_data, exist_ok=True)
            db_path = os.path.join(app_data, "transactions.db")
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON") # 开启外键约束
        self.cursor = self.conn.cursor()
        self._init_database()
    
    def _cleanup_orphans(self):
        """清理孤儿交易 (关联的模块已不存在)"""
        self.cursor.execute("DELETE FROM transactions WHERE module_id NOT IN (SELECT id FROM modules)")
        if self.cursor.rowcount > 0:
            print(f"Cleaned up {self.cursor.rowcount} orphaned transactions")
            self.conn.commit()

    def _get_db_version(self) -> int:
        """获取当前数据库版本"""
        self.cursor.execute("PRAGMA user_version")
        return self.cursor.fetchone()[0]
    
    def _set_db_version(self, version: int):
        """设置数据库版本"""
        self.cursor.execute(f"PRAGMA user_version = {version}")
        self.conn.commit()
    
    def _init_database(self):
        """初始化或迁移数据库"""
        current_version = self._get_db_version()
        
        if current_version == 0:
            # 全新安装
            self._create_tables_v2()
            self._set_db_version(CURRENT_DB_VERSION)
        elif current_version < CURRENT_DB_VERSION:
            # 需要迁移
            self._migrate_database(current_version)
        
        # 每次启动都清理孤儿数据
        self._cleanup_orphans()
    
    def _create_tables_v2(self):
        """创建v2版本数据表"""
        # 模块表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                icon TEXT DEFAULT '📁',
                color TEXT DEFAULT '#8b5cf6',
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 交易表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id INTEGER DEFAULT 1,
                amount REAL NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                source TEXT DEFAULT '',
                is_selected INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
            )
        ''')
        
        # 创建默认模块
        self.cursor.execute(
            "INSERT OR IGNORE INTO modules (id, name, icon, color) VALUES (1, '默认账本', '💰', '#8b5cf6')"
        )
        self.conn.commit()
    
    def _migrate_database(self, from_version: int):
        """数据库迁移"""
        if from_version < 2:
            # v1 -> v2: 添加模块支持
            # 检查是否已有旧表
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
            if self.cursor.fetchone():
                # 备份旧数据
                self.cursor.execute("ALTER TABLE transactions RENAME TO transactions_old")
                
            # 创建新表结构
            self._create_tables_v2()
            
            # 迁移旧数据
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions_old'")
            if self.cursor.fetchone():
                self.cursor.execute('''
                    INSERT INTO transactions (module_id, amount, type, source, created_at)
                    SELECT 1, amount, type, source, created_at FROM transactions_old
                ''')
                self.cursor.execute("DROP TABLE transactions_old")
            
            self.conn.commit()
        
        self._set_db_version(CURRENT_DB_VERSION)
    
    # ============ 模块管理 ============
    
    def add_module(self, name: str, icon: str = "📁", color: str = "#8b5cf6") -> int:
        """添加新模块"""
        self.cursor.execute(
            "SELECT MAX(sort_order) FROM modules"
        )
        max_order = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute(
            "INSERT INTO modules (name, icon, color, sort_order) VALUES (?, ?, ?, ?)",
            (name, icon, color, max_order + 1)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_all_modules(self) -> List[Tuple]:
        """获取所有模块"""
        self.cursor.execute(
            "SELECT id, name, icon, color FROM modules ORDER BY sort_order, id"
        )
        return self.cursor.fetchall()
    
    def update_module(self, module_id: int, name: str, icon: str, color: str):
        """更新模块信息"""
        self.cursor.execute(
            "UPDATE modules SET name=?, icon=?, color=? WHERE id=?",
            (name, icon, color, module_id)
        )
        self.conn.commit()
    
    def delete_module(self, module_id: int) -> bool:
        """删除模块（关联交易也会被删除）"""
        self.cursor.execute("DELETE FROM modules WHERE id=?", (module_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def delete_modules_batch(self, module_ids: list) -> int:
        """批量删除模块"""
        if not module_ids:
            return 0
        placeholders = ",".join("?" * len(module_ids))
        self.cursor.execute(f"DELETE FROM modules WHERE id IN ({placeholders})", module_ids)
        self.conn.commit()
        return self.cursor.rowcount
    
    def update_module_order(self, module_id: int, new_order: int):
        """更新模块排序"""
        self.cursor.execute(
            "UPDATE modules SET sort_order=? WHERE id=?",
            (new_order, module_id)
        )
        self.conn.commit()
    
    def get_modules_sorted_by_balance(self) -> list:
        """获取按余额排序的模块（从大到小）"""
        self.cursor.execute('''
            SELECT m.id, m.name, m.icon, m.color,
                   COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE -t.amount END), 0) as balance
            FROM modules m
            LEFT JOIN transactions t ON m.id = t.module_id
            GROUP BY m.id
            ORDER BY balance DESC
        ''')
        return self.cursor.fetchall()

    def get_modules_sorted_by_balance_asc(self) -> list:
        """获取按余额从小到大排序的模块"""
        self.cursor.execute('''
            SELECT m.id, m.name, m.icon, m.color,
                   COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE -t.amount END), 0) as balance
            FROM modules m
            LEFT JOIN transactions t ON m.id = t.module_id
            GROUP BY m.id
            ORDER BY balance ASC
        ''')
        return self.cursor.fetchall()

    def get_modules_sorted_by_created(self) -> list:
        """获取按创建时间排序的模块（最新创建在前）"""
        self.cursor.execute('''
            SELECT m.id, m.name, m.icon, m.color,
                   COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE -t.amount END), 0) as balance
            FROM modules m
            LEFT JOIN transactions t ON m.id = t.module_id
            GROUP BY m.id
            ORDER BY m.id DESC
        ''')
        return self.cursor.fetchall()

    def get_modules_sorted_by_updated(self) -> list:
        """获取按最近交易时间排序的模块（最近有动态在前）"""
        self.cursor.execute('''
            SELECT m.id, m.name, m.icon, m.color,
                   COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE -t.amount END), 0) as balance
            FROM modules m
            LEFT JOIN transactions t ON m.id = t.module_id
            GROUP BY m.id
            ORDER BY MAX(t.created_at) DESC NULLS LAST, m.id DESC
        ''')
        return self.cursor.fetchall()

    def get_modules_sorted_by_updated_asc(self) -> list:
        """获取按最早交易时间排序的模块（最早有动态在前）"""
        self.cursor.execute('''
            SELECT m.id, m.name, m.icon, m.color,
                   COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE -t.amount END), 0) as balance
            FROM modules m
            LEFT JOIN transactions t ON m.id = t.module_id
            GROUP BY m.id
            ORDER BY MAX(t.created_at) ASC NULLS LAST, m.id ASC
        ''')
        return self.cursor.fetchall()

    def get_modules_sorted_by_created_asc(self) -> list:
        """获取按创建时间升序排列的模块（最早创建在前）"""
        self.cursor.execute('''
            SELECT m.id, m.name, m.icon, m.color,
                   COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE -t.amount END), 0) as balance
            FROM modules m
            LEFT JOIN transactions t ON m.id = t.module_id
            GROUP BY m.id
            ORDER BY m.id ASC
        ''')
        return self.cursor.fetchall()

    def get_modules_sorted_by_income_desc(self) -> list:
        """获取按收入从大到小排序的模块"""
        self.cursor.execute('''
            SELECT m.id, m.name, m.icon, m.color,
                   COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE -t.amount END), 0) as balance
            FROM modules m
            LEFT JOIN transactions t ON m.id = t.module_id
            GROUP BY m.id
            ORDER BY COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE 0 END), 0) DESC
        ''')
        return self.cursor.fetchall()

    def get_modules_sorted_by_income_asc(self) -> list:
        """获取按收入从小到大排序的模块"""
        self.cursor.execute('''
            SELECT m.id, m.name, m.icon, m.color,
                   COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE -t.amount END), 0) as balance
            FROM modules m
            LEFT JOIN transactions t ON m.id = t.module_id
            GROUP BY m.id
            ORDER BY COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE 0 END), 0) ASC
        ''')
        return self.cursor.fetchall()

    def get_modules_sorted_by_expense_desc(self) -> list:
        """获取按支出从大到小排序的模块"""
        self.cursor.execute('''
            SELECT m.id, m.name, m.icon, m.color,
                   COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE -t.amount END), 0) as balance
            FROM modules m
            LEFT JOIN transactions t ON m.id = t.module_id
            GROUP BY m.id
            ORDER BY COALESCE(SUM(CASE WHEN t.type='expense' THEN t.amount ELSE 0 END), 0) DESC
        ''')
        return self.cursor.fetchall()

    def get_modules_sorted_by_expense_asc(self) -> list:
        """获取按支出从小到大排序的模块"""
        self.cursor.execute('''
            SELECT m.id, m.name, m.icon, m.color,
                   COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE -t.amount END), 0) as balance
            FROM modules m
            LEFT JOIN transactions t ON m.id = t.module_id
            GROUP BY m.id
            ORDER BY COALESCE(SUM(CASE WHEN t.type='expense' THEN t.amount ELSE 0 END), 0) ASC
        ''')
        return self.cursor.fetchall()
    
    # ============ 交易管理 ============
    
    def add_transaction(self, amount: float, trans_type: str, source: str = "", module_id: int = 1) -> int:
        """添加交易记录"""
        self.cursor.execute(
            "INSERT INTO transactions (module_id, amount, type, source) VALUES (?, ?, ?, ?)",
            (module_id, abs(amount), trans_type, source)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_transactions_by_module(self, module_id: int) -> List[Tuple]:
        """获取指定模块的交易记录"""
        self.cursor.execute(
            """SELECT id, amount, type, source, is_selected, created_at 
               FROM transactions WHERE module_id=? ORDER BY created_at DESC""",
            (module_id,)
        )
        return self.cursor.fetchall()
    
    def get_all_transactions(self) -> List[Tuple]:
        """获取所有交易记录"""
        self.cursor.execute(
            """SELECT t.id, t.amount, t.type, t.source, t.is_selected, t.created_at, m.name, m.icon
               FROM transactions t 
               JOIN modules m ON t.module_id = m.id
               ORDER BY t.created_at DESC"""
        )
        return self.cursor.fetchall()
    
    def search_transactions(self, keyword: str, module_id: int = None) -> List[Tuple]:
        """
        搜索交易记录 - 世界顶级智能引擎
        
        支持语法:
        - 纯文本: 模糊匹配备注 (source) 和 金额字符串
        - 数字 (如 100): 精确匹配金额 100.00
        - 范围 (如 100-500): 匹配 100 <= 金额 <= 500
        - 比较 (如 >100, <500): 匹配大于或小于金额
        - 约等于 (如 ~100): 匹配 95 ~ 105 (默认 5% 容差)
        """
        keyword = keyword.strip()
        if not keyword:
            return []
            
        # 解析搜索类型
        amount_condition = None
        params = []
        
        # 匹配模式
        import re
        
        # 1. 范围模式: "100-500", "100~500", "100到500"
        range_match = re.match(r'^([\d\.]+)\s*[-~到]\s*([\d\.]+)$', keyword)
        if range_match:
            try:
                v1, v2 = float(range_match.group(1)), float(range_match.group(2))
                amount_condition = "t.amount BETWEEN ? AND ?"
                params = [min(v1, v2), max(v1, v2)]
            except: pass
            
        # 2. 比较模式: ">100", "<100", ">=100", "<=100"
        if not amount_condition:
            comp_match = re.match(r'^([><]=?)\s*([\d\.]+)$', keyword)
            if comp_match:
                try:
                    op = comp_match.group(1)
                    val = float(comp_match.group(2))
                    amount_condition = f"t.amount {op} ?"
                    params = [val]
                except: pass
                
        # 3. 约等于模式: "~100" or "≈100" (5% 容差)
        if not amount_condition:
            fuzzy_match = re.match(r'^[~≈]([\d\.]+)$', keyword)
            if fuzzy_match:
                try:
                    val = float(fuzzy_match.group(1))
                    tol = val * 0.05
                    amount_condition = "t.amount BETWEEN ? AND ?"
                    params = [val - tol, val + tol]
                except: pass

        # 4. 纯数字模式 (智能模糊匹配)
        if not amount_condition:
            exact_match = re.match(r'^([\d\.]+)$', keyword)
            if exact_match:
                try:
                    val = float(exact_match.group(1))
                    # 算法优化：
                    # 1. 备注匹配 (LIKE %12%)
                    # 2. 金额作为文本匹配 (允许 12 搜到 12.98)
                    # 3. 如果是完整输入的数字，也进行金额精确对齐
                    amount_condition = "(t.source LIKE ? OR CAST(t.amount AS TEXT) LIKE ? OR ABS(t.amount - ?) < 0.01)"
                    params = [f"%{keyword}%", f"%{keyword}%", val]
                except: pass

        # 构建最终 SQL
        if module_id:
            # 模块内部搜索
            if amount_condition:
                sql = f"""SELECT id, amount, type, source, is_selected, created_at 
                         FROM transactions t 
                         WHERE module_id = ? AND ({amount_condition})
                         ORDER BY created_at DESC"""
                query_params = [module_id] + params
            else:
                # 模糊文本搜索 (备注 + 金额文本)
                sql = """SELECT id, amount, type, source, is_selected, created_at 
                         FROM transactions t 
                         WHERE module_id = ? AND (t.source LIKE ? OR CAST(t.amount AS TEXT) LIKE ?)
                         ORDER BY created_at DESC"""
                query_params = [module_id, f"%{keyword}%", f"%{keyword}%"]
        else:
            # 全局搜索
            if amount_condition:
                sql = f"""SELECT t.id, t.amount, t.type, t.source, t.is_selected, t.created_at, m.name, m.icon
                         FROM transactions t 
                         JOIN modules m ON t.module_id = m.id
                         WHERE {amount_condition}
                         ORDER BY t.created_at DESC"""
                query_params = params
            else:
                sql = """SELECT t.id, t.amount, t.type, t.source, t.is_selected, t.created_at, m.name, m.icon
                         FROM transactions t 
                         JOIN modules m ON t.module_id = m.id
                         WHERE t.source LIKE ? OR CAST(t.amount AS TEXT) LIKE ?
                         ORDER BY t.created_at DESC"""
                query_params = [f"%{keyword}%", f"%{keyword}%"]

        self.cursor.execute(sql, query_params)
        return self.cursor.fetchall()
    
    def toggle_selection(self, trans_id: int) -> bool:
        """切换交易勾选状态"""
        self.cursor.execute(
            "UPDATE transactions SET is_selected = NOT is_selected WHERE id=?",
            (trans_id,)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def clear_all_selections(self, module_id: int = None):
        """清除勾选"""
        if module_id:
            self.cursor.execute("UPDATE transactions SET is_selected=0 WHERE module_id=?", (module_id,))
        else:
            self.cursor.execute("UPDATE transactions SET is_selected=0")
        self.conn.commit()
    
    def get_selected_stats(self, module_id: int = None) -> Tuple[int, float, float]:
        """获取勾选项统计 (数量, 收入, 支出)"""
        if module_id:
            self.cursor.execute(
                """SELECT COUNT(*), 
                   SUM(CASE WHEN type='income' THEN amount ELSE 0 END),
                   SUM(CASE WHEN type='expense' THEN amount ELSE 0 END)
                   FROM transactions WHERE module_id=? AND is_selected=1""",
                (module_id,)
            )
        else:
            self.cursor.execute(
                """SELECT COUNT(*), 
                   SUM(CASE WHEN type='income' THEN amount ELSE 0 END),
                   SUM(CASE WHEN type='expense' THEN amount ELSE 0 END)
                   FROM transactions WHERE is_selected=1"""
            )
        result = self.cursor.fetchone()
        return (result[0] or 0, result[1] or 0.0, result[2] or 0.0)
    
    def delete_transaction(self, trans_id: int) -> bool:
        """删除交易记录"""
        self.cursor.execute("DELETE FROM transactions WHERE id=?", (trans_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    # ============ 统计 ============
    
    def get_module_balance(self, module_id: int) -> float:
        """获取模块余额"""
        self.cursor.execute(
            "SELECT SUM(CASE WHEN type='income' THEN amount ELSE -amount END) FROM transactions WHERE module_id=?",
            (module_id,)
        )
        result = self.cursor.fetchone()[0]
        return result if result else 0.0
    
    def get_module_stats(self, module_id: int) -> Tuple[float, float]:
        """获取模块收支统计 (收入, 支出)"""
        self.cursor.execute(
            "SELECT SUM(CASE WHEN type='income' THEN amount ELSE 0 END), SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) FROM transactions WHERE module_id=?",
            (module_id,)
        )
        result = self.cursor.fetchone()
        return (result[0] or 0.0, result[1] or 0.0)
    
    def get_total_balance(self) -> float:
        """获取总余额"""
        self.cursor.execute(
            "SELECT SUM(CASE WHEN type='income' THEN amount ELSE -amount END) FROM transactions"
        )
        result = self.cursor.fetchone()[0]
        return result if result else 0.0
    
    def get_total_stats(self) -> Tuple[float, float]:
        """获取总收支统计"""
        self.cursor.execute(
            "SELECT SUM(CASE WHEN type='income' THEN amount ELSE 0 END), SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) FROM transactions"
        )
        result = self.cursor.fetchone()
        return (result[0] or 0.0, result[1] or 0.0)
    
    def get_modules_summary(self) -> List[Tuple]:
        """获取所有模块汇总"""
        self.cursor.execute('''
            SELECT m.id, m.name, m.icon, m.color,
                   COALESCE(SUM(CASE WHEN t.type='income' THEN t.amount ELSE 0 END), 0) as income,
                   COALESCE(SUM(CASE WHEN t.type='expense' THEN t.amount ELSE 0 END), 0) as expense
            FROM modules m
            LEFT JOIN transactions t ON m.id = t.module_id
            GROUP BY m.id
            ORDER BY m.sort_order, m.id
        ''')
        return self.cursor.fetchall()
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()
