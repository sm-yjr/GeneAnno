import pandas as pd

# 打开 Excel 文件
xlsx = pd.ExcelFile('/Users/yangjiarui/Downloads/GeneAnnotation/wy/副本基因变化注释(1).xlsx')

# 遍历所有的工作表
for sheet_name in xlsx.sheet_names:
    # 读取每个工作表为一个 DataFrame
    df = xlsx.parse(sheet_name)

    # 将 DataFrame 保存为 CSV 文件
    df.to_csv(f'/Users/yangjiarui/Downloads/GeneAnnotation/wy/{sheet_name}.csv', index=False)
