# JASA_spider

#### 1. 爬虫的程序和中间文件（可忽略它们）

- JASA_spider.py
- issue_list.json
- vol_list.json

#### 2. 原始数据

- **文件夹 Abstracts**：每个文件是一个年份的论文标题+论文摘要

#### 3. 数据处理程序与数据

- Gather_abs.py：将文件夹 Abstracts中的数据汇总成一个数据文件abstracts.json
- AbsToWords.py：分词，并生成摘要数据文件abs_word.json
- abstracts.json：汇总的所有年份论文标题+摘要
- abs_word.json：分词后的摘要数据

#### 4. 组会上报告的描述性统计

- Description.ipynb：jupyter notebook原始文件
- Description.html：Description.ipynb导出来的html文件，可直接看这个

