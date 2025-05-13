import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import math
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 文件路径
input_path = "data-7-primal-plus-final-score-trimmed.xlsx"
output_fig_path = "data-8-figure-of-compare.png"

# 读取数据
df = pd.read_excel(input_path)
col1 = df.columns[-2]
col2 = df.columns[-1]

# 设置分段大小
segment_size = 5000
N = len(df)
num_segments = math.ceil(N / segment_size)

# 创建画布
plt.figure(figsize=(15, num_segments * 3))

for i in range(num_segments):
    start = i * segment_size
    end = min((i + 1) * segment_size, N)
    x_vals = range(start, end)
    y1 = df[col1].iloc[start:end].values
    y2 = df[col2].iloc[start:end].values
    
    corr, _ = pearsonr(y1, y2)
    
    plt.subplot(num_segments, 1, i + 1)
    plt.plot(x_vals, y1, label=col1, linewidth=1)
    plt.plot(x_vals, y2, label=col2, linestyle='--', linewidth=1.5)
    plt.title(f"Segment {i+1}: Sample {start}–{end} | Pearson r = {corr:.5f}")
    plt.xlabel("Sample Index")
    plt.ylabel("Score")
    plt.legend()
    plt.grid(True)

plt.tight_layout()
plt.savefig(output_fig_path, dpi=300)
print(f"✅ 图像保存为：{output_fig_path}")
