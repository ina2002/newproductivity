import pandas as pd
import numpy as np

# === 参数设置 ===
input_data_path = "data-1-processed-normalized.xlsx"
input_weight_path = "data-4-criteria-final-weight.xlsx"
output_path = "data-6-final-score.xlsx"
output_path_test = "data-test-6-final-score+liuxiong.xlsx"
# === 读取融合权重 y_j ===
df_weight = pd.read_excel(input_weight_path)
y_fused = df_weight.iloc[:, 0].values  # shape: (J,)
y_of_liuixong=[0.07817,0.07432,0.13901,0.14558,0.10473,0.07433,0.07585,0.07758,0.07863,0.0759,0.07588]

# === 读取原始指标数据 ===
df_data = pd.read_excel(input_data_path, sheet_name="mapped_data")
meta_cols = df_data.iloc[:, :2]  # stock_code, year
data_matrix = df_data.iloc[:, 2:]  # 指标数据 (J列)

# === 校验维度 ===
assert data_matrix.shape[1] == len(y_fused), "指标数量与权重维度不一致！"

# === 计算得分 ===
scores = data_matrix.values @ y_fused  # 每行 dot product
scores_liuxiong = data_matrix.values @ y_of_liuixong  # 每行 dot product
#保存scores和scores_liuxiong到data-6-final-score+liuxiong.xlsx
df_scores = pd.DataFrame(scores, columns=["Final_Score"])
df_scores_liuxiong = pd.DataFrame(scores_liuxiong, columns=["Final_Score_LiuXiong"])
df_final = pd.concat([meta_cols, df_scores, df_scores_liuxiong], axis=1)
df_final = df_final.sort_values(by=["year", "Final_Score"], ascending=[True, False])
df_final.reset_index(drop=True, inplace=True)
# === 保存结果 ===
df_final.to_excel(output_path_test, index=False)
print(f"✅ 最终得分计算完成，结果已保存至 {output_path_test}。")

#计算scores 和scores_liuxiong的pearson相关系数
correlation = df_final["Final_Score"].corr(df_final["Final_Score_LiuXiong"])
print(f"✅ scores 和 scores_liuxiong 的 Pearson 相关系数为: {correlation:.4f}")
# 计算scores 和scores_liuxiong的Spearman相关系数
spearman_correlation = df_final["Final_Score"].corr(df_final["Final_Score_LiuXiong"], method='spearman')
print(f"✅ scores 和 scores_liuxiong 的 Spearman 相关系数为: {spearman_correlation:.4f}")
# 计算scores 和scores_liuxiong的Kendall相关系数
kendall_correlation = df_final["Final_Score"].corr(df_final["Final_Score_LiuXiong"], method='kendall')
print(f"✅ scores 和 scores_liuxiong 的 Kendall 相关系数为: {kendall_correlation:.4f}")