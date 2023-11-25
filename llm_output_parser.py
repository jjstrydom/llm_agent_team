import json
import re
from response_components import ResponseComponent, project_plan_components
import markdown_to_json
import markdown 
from bs4 import BeautifulSoup
from pprint import pprint

def find_headings(soup, project_plan_components):
    project_plan_component_names = [c.name for c in project_plan_components]
    headings = soup.find_all(re.compile("^h[1-6]$"))
    headings = [h for h in headings if any([p.lower() in h.text.lower() for p in project_plan_component_names])]
    return headings
        
def find_contents(headings):
    content = {}
    for h in headings:
        content[h.text] = []
        for c in drop_from_list(list(h.next_siblings),"\n"):
            if c in headings:
                break
            content[h.text].append(c)
    return content

def flatten_list(the_list: list, nr_prefix=''):
    if not isinstance(the_list, list):
        return [the_list]
    new_list = []
    n = 0
    for list_item in the_list:  
        if type(list_item) == list:
            number_str = f"{nr_prefix}{str(n)}."
            new_list.extend(flatten_list(list_item, nr_prefix=number_str))
        else:
            n += 1
            number_str = f"{nr_prefix}{str(n)}."
            new_list.append(f"{number_str} {str(list_item)}")
    return new_list

def extract_hidden_list(text:str):
    hidden_list_strs = re.findall(r'\[[\"|\'](.*?)[\"|\']\]', text)
    hidden_list = []
    for n, hl in enumerate(hidden_list_strs):
        loading_str = f'["{hl}"]'.replace('\n','').replace("',","\",").replace(", '",", \"")
        loaded = json.loads(loading_str)
        hidden_list.extend(loaded)
    return hidden_list

def drop_from_list(the_list:list, item_to_drop):
    return list(filter(lambda item: item != item_to_drop, the_list))

def add_hash(match):
    return '#' + match.group(1)

def clean_plain_text(text: str):
    pattern = re.compile(r'(?<=\n\n)([^#\n]+:)(?=\n\n)')
    text = pattern.sub(add_hash, text)
    return text

def extract_tasks_content(text: str, response_components: list):
    clean = clean_plain_text(text)
    html = markdown.markdown(clean)
    soup = BeautifulSoup(html, 'lxml')
    headings = find_headings(soup, response_components)
    content = find_contents(headings)
    pprint(content)


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_parquet('data/project_plan.parquet')
    data = df.loc[2].iloc[0]
    extracted = extract_tasks_content(data, project_plan_components)
