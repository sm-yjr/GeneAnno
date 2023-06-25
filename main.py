import pandas as pd
from Bio import Entrez
import time
# 请用你的邮箱替换这里
Entrez.email = "ghsmyjr@gmail.com"

# 读取csv文件
df = pd.read_csv('/Users/yangjiarui/Downloads/cellranger/outdir/GeneAnno/top_diff_exp_genes_cluster_Muscle.csv')
genes = df['Gene'].values  # 获取基因名称


full_names = []
summaries = []
# 遍历每个基因
for gene_name in genes:
    print(gene_name)
    handle = Entrez.esearch(db="gene", term=f"{gene_name}[Gene] AND Mus musculus[Orgn]")
    record = Entrez.read(handle)
    handle.close()

    if record["Count"] != "0":
        gene_id = record["IdList"][0]  # 获取基因ID

        # 使用基因ID获取基因的具体信息
        handle = Entrez.efetch(db="gene", id=gene_id, rettype="gb", retmode="xml")
        gene_record = Entrez.read(handle)

        # 获取摘要
        summary = gene_record[0].get('Entrezgene_summary', 'No summary found')
        summaries.append(summary)

        # 获取全名
        entrezgene_gene = gene_record[0].get('Entrezgene_gene', {})
        gene_ref = entrezgene_gene.get('Gene-ref', {})
        full_name = gene_ref.get('Gene-ref_desc', 'No name found')
        full_names.append(full_name)
    else:
        # 如果没有找到基因信息，添加一个占位符
        full_names.append('No name found')
        summaries.append('No summary found')

    # 将全名和摘要添加到数据框中
    df['Full Name'] = pd.Series(full_names)
    df['Summary'] = pd.Series(summaries)

    # 将数据框写入新的CSV文件
    df.to_csv('/Users/yangjiarui/Downloads/cellranger/outdir/GeneAnno/newfile.csv', index=False)  # 用你想要的文件路径替换'newfile.csv'
