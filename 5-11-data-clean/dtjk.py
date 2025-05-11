#dtjk.py
import pandas as pd
import numpy as np

# ===== 文件读取 =====
df = pd.read_excel("data0.xlsx")  # 请换成你文件的真实路径

# ===== 设定固定映射 =====
# 年份映射为 t=1~11（2012~2022）
year_map = {year: t for t, year in enumerate(range(2012, 2023), start=1)}

# 固定省份顺序（k=1~30）
province_order = [
    "安徽", "北京", "福建", "甘肃", "广东", "广西", "贵州", "海南", "河北", "河南",
    "黑龙江", "湖北", "湖南", "吉林", "江苏", "江西", "辽宁", "内蒙古", "宁夏", "青海",
    "山东", "山西", "陕西", "上海", "四川", "天津", "新疆", "云南", "浙江", "重庆"
]
province_map = {name: k for k, name in enumerate(province_order, start=1)}

# 指标按列顺序映射 j=1~25（你提供顺序为准）
indicator_cols = [
    "受教育程度", "高校在校生结构", "教育经费", "R&D人员总量", "R&D经费投入强度",
    "机器人安装密度", "数字基础设施水平", "就业理念", "创业活跃度", "环境保护力度",
    "工业固废物综合利用率", "人工智能企业数", "电子商务企业数", "数字普惠金融指数",
    "移动电话普及率", "人均专利数量", "人均收入", "人均GDP", "软件业务收入",
    "新兴战略产业占比", "数字经济", "电信业务", "互联网渗透度", "总体能源消耗", "绿色能源消耗"
]
indicator_map = {name: j for j, name in enumerate(indicator_cols, start=1)}

# ===== 提取 d^t_{jk} 结构 =====
dtjk_dict = {}

for year in range(2012, 2023):
    t = year_map[year]
    df_t = df[df["年份"] == year]
    matrix = np.full((25, 30), np.nan)

    for _, row in df_t.iterrows():
        k = province_map.get(row["省份"])
        if not k:
            continue
        for col in indicator_cols:
            j = indicator_map[col]
            val = row[col]
            matrix[j-1, k-1] = val

    dtjk_dict[t] = matrix


#保存dtjk到文件dtjk.xlsx,sheet名为d1jk,d2jk,...,d11jk
with pd.ExcelWriter("dtjk.xlsx") as writer:
    for t, matrix in dtjk_dict.items():
        df_matrix = pd.DataFrame(matrix, index=indicator_cols, columns=province_order)
        df_matrix.to_excel(writer, sheet_name=f"d{t}jk", index=True)
        