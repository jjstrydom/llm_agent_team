import json
import re
from response_components import ResponseComponent, project_plan_components
import markdown_to_json

def find_headings(response_components: ResponseComponent, text: str):
    if type(text) != str:
        return None
    text_to_test = text.lower()
    for component in response_components:
        if component.name.lower() in text_to_test:
            return component.name

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

def extract_tasks_content(text: str, response_components: list):
    input_dict = markdown_to_json.dictify(text)
    result_dict = {}
    for l in input_dict:
        result = find_headings(response_components, l)
        if result is not None:
            result_dict[result] = input_dict[l]

    for k, v in result_dict.items():
        hidden_list = []
        if isinstance(v, str):
            hidden_list = extract_hidden_list(v)
        if hidden_list:
            v = hidden_list
        result_dict[k] = flatten_list(v)
    return result_dict

if __name__ == "__main__":
    import pandas as pd
    df = pd.read_parquet('data/project_plan.parquet')
    data = df.loc[0].iloc[0]
    extracted = extract_tasks_content(data, project_plan_components)
    