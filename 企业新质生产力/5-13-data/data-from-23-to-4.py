import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd

# 参数设定
I = 5   # 专家数量
J = 11  # 指标数量
T = 12  # 年份数量
epsilon = 0.17  # 主客观融合容差

# 决策者对专家排序
a = [1, 3, 5, 2, 4]

# 读取 b_ij 和 e^t_j
df_b = pd.read_excel("data-3-expert-rank.xlsx")
b_matrix = df_b.iloc[:, 1:].values  # 形状 (I, J)

df_e = pd.read_excel("data-2-entropy.xlsx")
e_matrix = df_e.iloc[:, 1:].values  # 形状 (T, J)

# 初始化模型
model = gp.Model("compact_fusion_model")

# 打印求解日志
model.setParam('OutputFlag', 1)

# 决策变量
x = model.addVars(I, J, lb=0.0, name="x")
z = model.addVar(lb=0.0, name="z")

# 约束 1：排序一致性约束
for i in range(I):
    for j in range(J):
        for l in range(J):
            if b_matrix[i, l] > b_matrix[i, j]:
                model.addConstr(z <= a[i] * b_matrix[i, j] * (x[i, j] - x[i, l]),
                                name=f"sort_cons_i{i}_j{j}_l{l}")

# 约束 2：年度主客观一致性约束（范数）
for t in range(T):
    expr = gp.QuadExpr()
    for j in range(J):
        expr += (gp.quicksum(x[i, j] for i in range(I)) - e_matrix[t, j]) ** 2
    model.addQConstr(expr <= epsilon ** 2, name=f"norm_cons_t{t}")

# 约束 3：总和为1
model.addConstr(gp.quicksum(x[i, j] for i in range(I) for j in range(J)) == 1, name="sum_to_1")

# 目标函数
model.setObjective(z, GRB.MAXIMIZE)

# 求解
model.optimize()

# 输出结果
if model.status == GRB.OPTIMAL:
    print(f"✅ 最优目标值 z = {z.X:.6f}")
    x_vals = np.array([[x[i, j].X for j in range(J)] for i in range(I)])
    y_fused = x_vals.sum(axis=0)
    print("📊 融合后的 y_j 权重（每个指标）:")
    for j in range(J):
        print(f"y_{j+1} = {y_fused[j]:.6f}")
else:
    print("❌ 未求得最优解，状态码:", model.status)

#保存y_fused到Excel
output_path = r"data-4-criteria-final-weight.xlsx"
# 保存 y_fused 为一列形式
df_fused = pd.DataFrame({'y_j': y_fused})
df_fused.to_excel("data-4-criteria-final-weight.xlsx", index=False)
print("✅ y_fused 已保存至 data-4-criteria-final-weight.xlsx")