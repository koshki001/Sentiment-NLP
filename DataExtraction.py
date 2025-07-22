import os
from goose3 import Goose
from tqdm import tqdm
import pandas as pd
from process_analysis import analysis
dfs = pd.read_excel('Input.xlsx', sheet_name='Sheet1')
extracted_path = 'text_extracted/'
dir_list = os.listdir(extracted_path)
output_file = 'utility_files/Output Data Structure.xlsx'
df = pd.read_excel(output_file)


def get_title_and_content(url):
    try:
        g = Goose()
        article = g.extract(url=url)
        title = article.title
        # print(article.infos)
        content = article.cleaned_text
        return {"title": title, "content": content}
    except:
        return {"title": 'None', "content": 'None'}


def app():
    print('Extracting texts..')
    for i in tqdm(range(0, len(dfs))):
        file_name = dfs['URL_ID'][i]
        url = dfs['URL'][i]
        res = get_title_and_content(url)
        with open(f"text_extracted/{file_name}.txt", "w", encoding='utf-8') as file:
            file.write(res['title'])
            file.write('\n')
            file.write(res['content'])

    modified_df = analysis(dir_list, df, extracted_path)
    modified_df.to_excel('Output Data Structure modified.xlsx')

app()