import pandas as pd

# 文件路径
main_path = "data-0.xlsx"
score_path = "data-6-final-score.xlsx"
output_path = "data-7-primal-plus-final-score-trimmed.xlsx"

# 读取数据
df_main = pd.read_excel(main_path)
df_score = pd.read_excel(score_path)

# 截取主表前 N 行，使其与得分数据对齐
df_main_trimmed = df_main.iloc[:len(df_score)]

# 提取得分列（最后一列）
final_score_col = df_score.iloc[:, -1]
final_score_col.name = "final_score"

# 合并
df_combined = pd.concat([df_main_trimmed, final_score_col], axis=1)

# 保存结果
df_combined.to_excel(output_path, index=False)

print(f"✅ 合并完成，已保存为：{output_path}")

