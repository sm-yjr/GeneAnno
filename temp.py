from Bio import Entrez
import pandas as pd

Entrez.email = '123456789@qq.com'

# 选择一个基因进行查询
gene_name = 'Igkc'  # 使用你的基因名称替换这里

handle = Entrez.esearch(db="gene", term=f"{gene_name}[Gene] AND Mus musculus[Orgn]")
record = Entrez.read(handle)
handle.close()

if record["Count"] != "0":
    gene_id = record["IdList"][0]  # 获取基因ID

    # 使用基因ID获取基因的具体信息
    handle = Entrez.efetch(db="gene", id=gene_id, rettype="gb", retmode="xml")
    gene_record = Entrez.read(handle)
    handle.close()
    summary = gene_record[0].get('Entrezgene_summary', 'No summary found')

    entrezgene_gene = gene_record[0].get('Entrezgene_gene', {})
    gene_ref = entrezgene_gene.get('Gene-ref', {})
    full_name = gene_ref.get('Gene-ref_desc', 'No name found')
    print(full_name)

    # print(summary)
    # 打印出基因的所有信息
    # print(gene_record[0])
