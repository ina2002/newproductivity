import pandas as pd

# 读取数据
df = pd.read_excel("data-1-processed.xlsx")

# 假设第1列为ID或股票代码，第2列为年份，指标从第3列开始，共11个
id_col = df.columns[0]
year_col = df.columns[1]
indicator_cols = df.columns[2:13]  # 共11个指标

# 正向指标归一化（极差标准化）
df_normalized = df.copy()
for col in indicator_cols:
    col_min = df[col].min()
    col_max = df[col].max()
    if col_max != col_min:
        df_normalized[col] = (df[col] - col_min) / (col_max - col_min)
    else:
        df_normalized[col] = 0.0  # 所有值都相同，归一化为0

# 保存归一化结果
df_normalized.to_excel("data-1-processed-normalized.xlsx", index=False)
#print("数据归一化完成，结果已保存为 data-1-processed-normalized.xlsx")
print("✅数据归一化完成，结果已保存为 data-1-processed-normalized.xlsx")