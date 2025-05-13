import pandas as pd
import numpy as np

# === Step 1: 读取原始数据 ===
file_path = r"data-1-processed-normalized.xlsx"
df = pd.read_excel(file_path, header=0)

# 设置列名：前两列是 股票代码、年份，后面是指标
df.columns = ['stock_code', 'year'] + [f'indicator_{i}' for i in range(1, len(df.columns) - 1)]
indicator_cols = df.columns[2:]

# === Step 2: 熵值法函数 ===
def entropy_weight(df_indicators):
    # 极差标准化
    X = df_indicators.copy()
    min_vals = X.min()
    max_vals = X.max()
    diff = max_vals - min_vals
    X = (X - min_vals) / diff.replace(0, 1e-10)

    # 熵值计算
    P = X.div(X.sum(axis=0), axis=1).replace(0, 1e-10)
    k = 1.0 / np.log(len(P))
    E = -k * (P * np.log(P)).sum(axis=0)
    d = 1 - E
    w = d / d.sum()
    return w

# === Step 3: 按年份分组计算年度熵值权重 ===
yearly_weights = []
for year, group in df.groupby('year'):
    indicators = group[indicator_cols]
    weights = entropy_weight(indicators)
    weights['year'] = year
    yearly_weights.append(weights)

df_yearly = pd.DataFrame(yearly_weights).sort_values(by='year').reset_index(drop=True)
df_yearly = df_yearly[['year'] + list(indicator_cols)]  # 调整列顺序

# === Step 4: 计算整体熵值权重（不区分年份）===
df_overall = entropy_weight(df[indicator_cols])
df_overall = pd.DataFrame(df_overall).T
df_overall.insert(0, 'year', 'Overall')

# === Step 5: 保存结果到 Excel 文件的两个 Sheet 中 ===
output_path = r"data-2-entropy.xlsx"
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    df_yearly.to_excel(writer, sheet_name='Yearly_Entropy_Weights', index=False)
    df_overall.to_excel(writer, sheet_name='Overall_Entropy_Weight', index=False)

print("✅ 年度熵值权重与整体熵值权重计算完成，已保存至 data-2-entropy.xlsx")
