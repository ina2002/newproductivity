import pandas as pd
import numpy as np

# 读取数据
df = pd.read_excel("ejk0.xlsx")  # 替换为你的文件路径或 pd.read_excel(...)

# 原始数据顺序（列头）
original_columns = [
    "R&D人员总量", "R&D经费投入强度", "互联网渗透度", "人均GDP", "人均专利数量", "人均收入",
    "人工智能企业数", "创业活跃度", "受教育程度", "就业理念", "工业固废物综合利用率",
    "总体能源消耗", "教育经费", "数字基础设施水平", "数字普惠金融指数", "数字经济",
    "新兴战略产业占比", "机器人安装密度", "环境保护力度", "电信业务", "电子商务企业数",
    "移动电话普及率", "绿色能源消耗", "软件业务收入", "高校在校生结构"
]

# 目标顺序
target_order = [
    "受教育程度", "高校在校生结构", "教育经费", "R&D人员总量", "R&D经费投入强度",
    "机器人安装密度", "数字基础设施水平", "就业理念", "创业活跃度", "环境保护力度",
    "工业固废物综合利用率", "人工智能企业数", "电子商务企业数", "数字普惠金融指数",
    "移动电话普及率", "人均专利数量", "人均收入", "人均GDP", "软件业务收入",
    "新兴战略产业占比", "数字经济", "电信业务", "互联网渗透度", "总体能源消耗", "绿色能源消耗"
]

# 构建列名对应字典
col_map = {col: col for col in original_columns}

# 加入 year 列
col_map["year"] = "year"

# 重新排序
reordered_df = df[["year"] + target_order]

# 去除 year 列，仅保留 11×25 数值矩阵（可选）
d_tj_matrix = reordered_df.drop(columns=["year"]).to_numpy()

# 输出
print("全国 d^t_j (11x25) 矩阵：")
print(d_tj_matrix)

# 保存为 Excel 或 npy
reordered_df.to_excel("ejk.xlsx", index=False)
np.save("national_dtj.npy", d_tj_matrix)
