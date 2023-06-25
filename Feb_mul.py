from Bio import Entrez
Entrez.api_key = "d8aca9a4d349dbfe4e35c3dda14623ebed09"
import pandas as pd
import os
import time
from googletrans import Translator
from concurrent.futures import ThreadPoolExecutor, as_completed

Entrez.max_tries = 30
Entrez.sleep_between_tries = 5

Entrez.email = 'abc@gmail.com'  # 你的邮箱
translator = Translator()

input_folder = '/Users/yangjiarui/Downloads/GeneAnnotation/wy/'  # 输入文件夹
output_folder = os.path.join(input_folder, 'annotated')  # 输出文件夹

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def process_gene(gene_name):
    print(f"Processing {gene_name}")
    count = 0 # 错误计数
    time.sleep(0.1) # 避免超限
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
                handle.close()

                # 获取摘要和全名
                summary = gene_record[0].get('Entrezgene_summary', 'No summary found')
                entrezgene_gene = gene_record[0].get('Entrezgene_gene', {})
                gene_ref = entrezgene_gene.get('Gene-ref', {})
                full_name = gene_ref.get('Gene-ref_desc', 'No name found')

                # 翻译成中文
                full_name_cn = full_name
                summary_cn = summary
                # full_name_cn = translator.translate(full_name, dest='zh-CN').text
                # summary_cn = translator.translate(summary, dest='zh-CN').text
            else:
                # 如果没有找到基因信息，添加一个占位符
                # summary = 'Summary not found'
                # full_name = "Full name not found"
                summary_cn = '没有找到摘要'
                full_name_cn = '没有找到全名'

            # 如果成功执行，跳出循环
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"Waiting for a while before retrying...")
            time.sleep(1)
            count = count + 1
            print(f"Retrying {gene_name} for {count} times")
            continue

    return gene_name, full_name_cn, summary_cn

# 遍历输入文件夹中的所有CSV文件
for filename in os.listdir(input_folder):
    print(f"Processing {filename}")
    if filename.endswith('.csv'):
        # 读取CSV文件
        df = pd.read_csv(os.path.join(input_folder, filename))
        first_column_name = df.columns[0]
        df = df.rename(columns={first_column_name: 'Gene'})  # 如果第一列没有名称，则添加一个列名
        genes = df['Gene'].values  # 获取基因名称

        # 创建线程池
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(process_gene, gene): gene for gene in genes}

            for future in as_completed(futures):
                gene_name, full_name_cn, summary_cn = future.result()

                # 将摘要和全名添加到数据框中
                df.loc[df['Gene'] == gene_name, 'Full Name CN'] = full_name_cn
                df.loc[df['Gene'] == gene_name, 'Summary CN'] = summary_cn

                # 将数据框写入CSV文件
                output_filename = os.path.join(output_folder, filename)
                df.to_csv(output_filename, index=False)

                print(f"Finished processing gene {gene_name}. Results saved to {output_filename}.")
