import matplotlib.pyplot as plt
import pandas as pd
#支持中文图例
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 读取数据
df_e = pd.read_excel("data-2-entropy.xlsx")
e_matrix = df_e.iloc[:, 1:].values
t_labels = df_e['year'].tolist()

df_y = pd.read_excel("data-4-criteria-final-weight.xlsx")
y_fused = df_y.iloc[:, 0].values

T = e_matrix.shape[0]
J = e_matrix.shape[1]

# 横轴指标标签
indicator_labels = [
    "高学历人员占比", "研发人员占比", "研发人员薪资占比", "研发经费直接投入占比", "研发租赁费占比",
    "固定资产占比", "无形资产占比", "企业创新水平", "数字资产占比", "工业机器人渗透度",
    "华证ESG中E得分"
]

# 开始绘图
plt.figure(figsize=(12, 6))

# 绘制 e^t_j 的曲线
for t in range(T):
    plt.plot(range(1, J + 1), e_matrix[t], linewidth=1, label=f"{t_labels[t]}指标熵权")

# 绘制 y_j 融合权重曲线
plt.plot(range(1, J + 1), y_fused, linewidth=3, linestyle='--', color='black', label="主客观融合指标权重")

# 设置横轴标签
plt.xticks(ticks=range(1, J + 1), labels=indicator_labels, rotation=45, ha='right')

# 图例和其他美化

plt.ylabel("权重")
plt.title("各年度熵权 vs 融合权重 ")
plt.legend(loc="upper right", fontsize="small")
plt.grid(True)
plt.tight_layout()
plt.savefig("data-5-criteria-final-weight-vs-entropy-weight", dpi=300)
print("✅ 图像保存为：data-5-criteria-final-weight-vs-entropy-weight.png")
# 显示图像
plt.show()
