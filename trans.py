import pandas as pd
from googletrans import Translator
import time
# 翻译已有的文件

df = pd.read_csv("/Users/yangjiarui/Downloads/cellranger/outdir/GeneAnno/annotated/transm.csv")
full_name = df['Full Name'].values
summary = df['Summary'].values

full_names = []
summaries = []
for txt in full_name:
    while True:
        try:
            tr = Translator()
            txt_cn = tr.translate(text=txt, dest='zh-CN', src='en').text
            full_names.append(txt_cn)
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"Waiting for 1 seconds before retrying...")
            time.sleep(1)
            continue

    df['Full Name'] = pd.Series(full_names)
    df.to_csv("/Users/yangjiarui/Downloads/cellranger/outdir/GeneAnno/annotated/transm.csv")

for txt in summary:
    while True:
        try:
            tr = Translator()
            txt_cn = tr.translate(text=txt, dest='zh-CN', src='en').text
            summaries.append(txt_cn)
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"Waiting for 1 seconds before retrying...")
            time.sleep(1)
            continue

    df['Summary'] = pd.Series(summaries)
    df.to_csv("/Users/yangjiarui/Downloads/cellranger/outdir/GeneAnno/annotated/transm.csv")