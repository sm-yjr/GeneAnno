from Bio import Entrez
import pandas as pd
import time
#稳定版
Entrez.email = '123456789@qq.com'  # 你的邮箱

# 读取CSV文件
df = pd.read_csv('/Users/yangjiarui/Downloads/cellranger/outdir/GeneAnno/top_diff_exp_genes_cluster_Stromal.csv')  # 用你的保存了部分结果的csv文件路径替换'newfile.csv'
genes = df['Gene'].values  # 获取基因名称

# 找到你想要开始查询的基因在列表中的位置
start_position = list(genes).index('Igkc')  # 使用你想要开始查询的基因替换'H3f3a'

# 从指定位置开始遍历基因
for i in range(start_position, len(genes)):
    gene_name = genes[i]
    print(gene_name)
    while True:  # 无限循环，直到查询成功
        try:
            handle = Entrez.esearch(db="gene", term=f"{gene_name}[Gene] AND Mus musculus[Orgn]")
            record = Entrez.read(handle)
            handle.close()

            if record["Count"] != "0":
                gene_id = record["IdList"][0]  # 获取基因ID

                # 使用基因ID获取基因的具体信息
                handle = Entrez.efetch(db="gene", id=gene_id, rettype="gb", retmode="xml")
                gene_record = Entrez.read(handle)

                # 获取摘要和全名
                summary = gene_record[0].get('Entrezgene_summary', 'No summary found')
                entrezgene_gene = gene_record[0].get('Entrezgene_gene', {})
                gene_ref = entrezgene_gene.get('Gene-ref', {})
                full_name = gene_ref.get('Gene-ref_desc', 'No name found')
            else:
                # 如果没有找到基因信息，添加一个占位符
                summary = 'No summary found'
                full_name = 'No name found'

            # 如果成功执行，跳出循环
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"Waiting for 5 seconds before retrying...")
            time.sleep(5)
            continue

    # 将摘要和全名添加到数据框中
    df.loc[i, 'Full Name'] = full_name
    df.loc[i, 'Summary'] = summary

    # 将数据框写入CSV文件
    df.to_csv('/Users/yangjiarui/Downloads/cellranger/outdir/GeneAnno/annotated/stromal_annotated.csv', index=False)  # 用你想要的文件路径替换'newfile.csv'
