import pandas as pd
import numpy as np

# === 参数设置 ===
input_data_path = "data-1-processed-normalized.xlsx"
input_weight_path = "data-4-criteria-final-weight.xlsx"
output_path = "data-6-final-score.xlsx"

# === 读取融合权重 y_j ===
df_weight = pd.read_excel(input_weight_path)
y_fused = df_weight.iloc[:, 0].values  # shape: (J,)

# === 读取原始指标数据 ===
df_data = pd.read_excel(input_data_path, sheet_name="mapped_data")
meta_cols = df_data.iloc[:, :2]  # stock_code, year
data_matrix = df_data.iloc[:, 2:]  # 指标数据 (J列)

# === 校验维度 ===
assert data_matrix.shape[1] == len(y_fused), "指标数量与权重维度不一致！"

# === 计算得分 ===
scores = data_matrix.values @ y_fused  # 每行 dot product
df_result = pd.concat([meta_cols, pd.Series(scores, name="final_score")], axis=1)

# === 保存为 Excel 文件 ===
df_result.to_excel(output_path, index=False)
print(f"✅ 结果已保存至：{output_path}")
