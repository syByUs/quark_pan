import pandas as pd
import numpy as np
import os

class ExcelManager:
    def __init__(self, file_path, columns=None):
        """
        初始化 Excel 管理类
        :param file_path: Excel 文件路径
        :param columns: 数据列名（可选），默认使用标准列
        """
        self.file_path = file_path
        self.default_columns = ['title', 'des', 'img', 'quark', 'baidu', 'category', 'count']
        self.columns = columns if columns else self.default_columns
        
        # 确保文件存在
        if not os.path.exists(file_path):
            self._create_empty_excel()
    
    def _create_empty_excel(self):
        """创建空的 Excel 文件"""
        df = pd.DataFrame(columns=self.columns)
        df['count'] = df['count'].fillna(0).astype(int)  # 初始化count为整数
        df.to_excel(self.file_path, index=False)
        print(f"📁 创建新文件: {self.file_path}")
    
    def read_data(self):
        """读取 Excel 数据到 DataFrame"""
        try:
            df = pd.read_excel(self.file_path)
            
            # 确保所有列都存在
            for col in self.columns:
                if col not in df.columns:
                    df[col] = np.nan if col != 'count' else 0
            
            # 确保count是整数类型
            df['count'] = df['count'].fillna(0).astype(int)
            return df
        
        except Exception as e:
            print(f"❌ 读取失败: {str(e)}")
            return pd.DataFrame(columns=self.columns)
    
    def save_data(self, df):
        """保存 DataFrame 到 Excel 文件"""
        try:
            # 确保列顺序正确
            df = df[self.columns] if all(col in df.columns for col in self.columns) else df
            df.to_excel(self.file_path, index=False)
            return True
        except Exception as e:
            print(f"❌ 保存失败: {str(e)}")
            return False
    
    # +++ 新增方法: 检查标题是否存在 +++
    def exists_by_title(self, title):
        """
        检查指定标题的记录是否存在
        :param title: 要检查的标题
        :return: 存在返回 True，否则返回 False
        """
        df = self.read_data()
        return not df[df['title'] == title].empty
    
    def update_or_insert(self, data_list):
        """
        更新或插入数据
        :param data_list: 字典列表，每个字典代表一行数据
        :return: 成功更新的记录数
        """
        df = self.read_data()
        update_count = 0
        
        for data in data_list:
            title = data.get('title')
            if not title:
                print("⚠️ 警告: 缺少标题字段，跳过记录")
                continue
            
            # 检查标题是否存在
            title_exists = self.exists_by_title(title)
            
            if title_exists:
                # 更新现有记录
                matches = df[df['title'] == title]
                idx = matches.index[0]
                updated = False
                
                # 只更新内容为空的字段
                for col in data:
                    if col in df.columns and col != 'count' and col != 'title':
                        # 检查原值是否为空或NaN
                        original_val = df.at[idx, col]
                        if pd.isna(original_val) or original_val == '':
                            new_val = data[col]
                            if pd.notna(new_val) and new_val != '':
                                df.at[idx, col] = new_val
                                print(f"🔄 更新字段 [{col}]: {title}")
                                updated = True
                
                # 增加计数
                df.at[idx, 'count'] += 1
                print(f"🔢 更新计数: {title} (count={df.at[idx, 'count']})")
                update_count += 1
            else:
                # 创建新记录
                new_row = {col: data.get(col, '') for col in self.columns if col != 'count'}
                new_row['count'] = 1  # 新记录计数初始化为1
                
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                print(f"✨ 新增记录: {title} (count=1)")
                update_count += 1
        
        if self.save_data(df):
            print(f"✅ 成功更新 {update_count} 条记录")
        return update_count
    
    def get_record_by_title(self, title):
        """根据标题获取记录"""
        df = self.read_data()
        matches = df[df['title'] == title]
        return matches.iloc[0].to_dict() if not matches.empty else None
    
    def get_records_by_category(self, category):
        """根据分类获取记录"""
        df = self.read_data()
        return df[df['category'] == category].to_dict('records')
    
    def increment_count(self, title):
        """仅增加指定标题的计数"""
        df = self.read_data()
        matches = df[df['title'] == title]
        
        if not matches.empty:
            idx = matches.index[0]
            df.at[idx, 'count'] += 1
            self.save_data(df)
            print(f"🔢 增加计数: {title} (新count={df.at[idx, 'count']})")
            return True
        return False
    
    def delete_record(self, title):
        """删除指定标题的记录"""
        df = self.read_data()
        initial_count = len(df)
        df = df[df['title'] != title]
        
        if len(df) < initial_count:
            self.save_data(df)
            print(f"🗑️ 删除记录: {title}")
            return True
        return False
    
    def get_category_stats(self):
        """获取分类统计"""
        df = self.read_data()
        return df['category'].value_counts().to_dict()
    
    def find_missing_fields(self, required_fields=None):
        """
        查找缺失字段的记录
        :param required_fields: 必填字段列表，默认为所有非计数字段
        :return: 缺失字段的标题列表
        """
        df = self.read_data()
        if not required_fields:
            required_fields = [col for col in self.columns if col not in ['count', 'title']]
        
        missing_records = []
        for _, row in df.iterrows():
            missing = [field for field in required_fields if pd.isna(row[field]) or row[field] == '']
            if missing:
                missing_records.append({
                    'title': row['title'],
                    'missing_fields': missing
                })
        
        return missing_records


# ====== 使用示例 ======
if __name__ == "__main__":
    # 初始化管理器
    excel_file = "data.xlsx"
    manager = ExcelManager(excel_file)
    
    # 1. 检查标题是否存在（新文件应不存在）
    title_to_check = "Python高级教程"
    exists = manager.exists_by_title(title_to_check)
    print(f"\n记录 '{title_to_check}' 是否存在? {'是' if exists else '否'}")
    
    # 2. 插入新记录
    print("\n=== 插入新记录 ===")
    manager.update_or_insert([
        {
            'title': 'Python高级教程',
            'des': '深入理解Python高级特性',
            'category': '编程'
        }
    ])
    
    # 3. 再次检查标题是否存在
    exists = manager.exists_by_title(title_to_check)
    print(f"\n记录 '{title_to_check}' 是否存在? {'是' if exists else '否'}")
    
    # 4. 使用存在检查进行条件操作
    if manager.exists_by_title("Python高级教程"):
        print("\n=== 更新记录 ===")
        manager.update_or_insert([
            {
                'title': 'Python高级教程',
                'img': 'python_advanced.jpg'
            }
        ])
    else:
        print("\n记录不存在，跳过更新")
    
    # 5. 检查不存在的标题
    non_existent_title = "不存在的标题"
    exists = manager.exists_by_title(non_existent_title)
    print(f"\n记录 '{non_existent_title}' 是否存在? {'是' if exists else '否'}")