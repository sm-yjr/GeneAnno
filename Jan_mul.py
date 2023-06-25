# 单文件多线程版本
from Bio import Entrez
import pandas as pd
import os
import time
from googletrans import Translator
from concurrent.futures import ThreadPoolExecutor

Entrez.email = '123456789@qq.com'  # 你的邮箱
translator = Translator()

input_folder = 'GeneAnno'  # 输入文件夹
output_folder = os.path.join(input_folder, 'annotated')  # 输出文件夹

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def process_gene(gene_name):
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

                # 翻译成中文
                full_name_cn = translator.translate(full_name, dest='zh-CN').text
                summary_cn = translator.translate(summary, dest='zh-CN').text
            else:
                # 如果没有找到基因信息，添加一个占位符
                summary_cn = '没有找到摘要'
                full_name_cn = '没有找到全名'

            # 如果成功执行，跳出循环
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"Waiting for 5 seconds before retrying...")
            time.sleep(5)
            continue

    return gene_name, full_name_cn, summary_cn

# 遍历输入文件夹中的所有CSV文件
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        # 读取CSV文件
        df = pd.read_csv(os.path.join(input_folder, filename))
        genes = df['Gene'].values  # 获取基因名称

        # 创建线程池
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(process_gene, genes))

        for gene_name, full_name_cn, summary_cn in results:
            # 将摘要和全名添加到数据框中
            df.loc[df['Gene'] == gene_name, 'Full Name CN'] = full_name_cn
            df.loc[df['Gene'] == gene_name, 'Summary CN'] = summary_cn

        # 将数据框写入CSV文件
        output_filename = os.path.join(output_folder, filename)
        df.to_csv(output_filename, index=False)

        print(f"Finished processing {filename}. Results saved to {output_filename}.")
