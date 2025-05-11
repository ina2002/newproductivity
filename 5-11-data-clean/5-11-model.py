#last edit: 2025-5-11



import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np

# ===== 参数设置 =====
I, J, K, T = 5, 25, 30, 11
ai = np.array([1, 2, 3, 4, 5])
bij = np.array([
    [8,6,7,3,2,5,9,13,14,23,21,10,19,24,20,11,15,16,1,4,12,17,22,18,25],
    [9,5,7,4,3,6,8,12,13,24,22,10,20,25,19,11,14,15,1,2,16,18,21,17,23],
    [7,8,6,3,2,4,9,11,12,25,23,10,21,24,20,12,14,15,1,5,16,18,22,17,19],
    [10,6,8,4,3,5,9,13,14,22,20,11,19,24,21,12,15,16,2,1,17,18,23,15,25],
    [9,7,8,4,2,5,10,12,13,23,21,11,20,25,22,14,16,16,1,3,17,18,19,24,22]
])

# ===== 数据读取 =====
d = np.zeros((T, J, K))
for t in range(1, T + 1):
    df = pd.read_excel("dtjk.xlsx", sheet_name=f"d{t}jk", header=0, index_col=0)
    d[t - 1] = df.values

e = pd.read_excel("ejk.xlsx", header=0, index_col=0).values

# ===== 模型建立 =====
model = gp.Model("NewProductivityOptimization")

x = model.addVars(I, J, K, T, lb=0, ub=1, name="x")
y = model.addVars(J, T, lb=0, ub=1, name="y")
z = model.addVar(lb=0, name="z")

# ===== 约束设置 =====

# 排序一致性：\sum_{l > k} z <= ai * bij * x
for t in range(T):
    for j in range(J):
        for k in range(K):
            count = sum(d[t, j, l] > d[t, j, k] for l in range(K))
            for i in range(I):
                model.addConstr(
                    count * z <= ai[i] * bij[i, j] * x[i, j, k, t],
                    name=f"ranking_{i}_{j}_{k}_{t}"
                )

# y[j,t] = sum_{i,k} x[i,j,k,t]
for t in range(T):
    for j in range(J):
        model.addConstr(
            gp.quicksum(x[i, j, k, t] for i in range(I) for k in range(K)) == y[j, t],
            name=f"y_def_{j}_{t}"
        )

# 年度间y保持一致
for j in range(J):
    for t in range(1, T):
        model.addConstr(y[j, t] == y[j, t - 1], name=f"y_equal_{j}_{t}")

# 熵权欧氏距离约束
epsilon = 0.07
for t in range(T):
    model.addQConstr(
        gp.quicksum((y[j, t] - e[t, j]) * (y[j, t] - e[t, j]) for j in range(J)) <= epsilon ** 2,
        name=f"entropy_cons_{t}"
    )

# 每个地区得分总和 ≤ 1
for t in range(T):
    for k in range(K):
        model.addConstr(
            gp.quicksum(x[i, j, k, t] for i in range(I) for j in range(J)) <= 1,
            name=f"region_score_{k}_{t}"
        )

# 所有x的总和 = 1（归一化约束）
for t in range(T):
    model.addConstr(
        gp.quicksum(x[i, j, k, t] for i in range(I) for j in range(J) for k in range(K)) == 1,
        name=f"norm_total_{t}"
    )

# ===== 目标函数 =====
model.setObjective(z, GRB.MAXIMIZE)
model.setParam("OutputFlag", 1)
model.optimize()

# ===== 解读输出 =====
f = np.zeros((T, K))
for t in range(T):
    for k in range(K):
        f[t, k] = sum(y[j, t].X * d[t, j, k] for j in range(J))

# 保存结果
pd.DataFrame(f, columns=[f"f_{k+1}" for k in range(K)],
             index=[f"t_{t+1}" for t in range(T)]).to_excel("ftk.xlsx")


