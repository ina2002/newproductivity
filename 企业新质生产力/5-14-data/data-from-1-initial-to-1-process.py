import pandas as pd

# 读取原始数据
df = pd.read_excel('data-1-initial.xlsx')

# 创建 stock_code 映射表
unique_codes = df['stock_code'].unique()
code_mapping = {code: idx + 1 for idx, code in enumerate(unique_codes)}

# 替换 stock_code 为映射值
df_mapped = df.copy()
df_mapped['stock_code'] = df_mapped['stock_code'].map(code_mapping)

# 构建映射表 DataFrame
mapping_df = pd.DataFrame(list(code_mapping.items()), columns=['original_stock_code', 'mapped_id'])

# 保存为一个 Excel 文件，两个 sheet
with pd.ExcelWriter('data-1-processed.xlsx', engine='openpyxl') as writer:
    df_mapped.to_excel(writer, sheet_name='mapped_data', index=False)
    mapping_df.to_excel(writer, sheet_name='code_mapping', index=False)

print("✅ 完成：两个 Sheet 已写入 data-1-processed.xlsx")
