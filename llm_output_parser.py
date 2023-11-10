import json
import re
from response_components import ResponseComponent

def find_headings(response_components: ResponseComponent, text: str):
    if type(text) != str:
        return None
    text_to_test = text.lower()
    for component in response_components:
        if component.name.lower() in text_to_test and len(text_to_test) <= len(component.name)*2:
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
    # print('='*90)
    # print(text)
    # print('-'*10)
    # print(hidden_list_strs)
    # print('='*90)
    hidden_list = []
    for n, hl in enumerate(hidden_list_strs):
        loading_str = f'["{hl}"]'.replace('\n','').replace("',","\",").replace(", '",", \"")
        # print(loading_str)
        loaded = json.loads(loading_str)
        # print(type(loaded), loaded)
        hidden_list.extend(loaded)
    return hidden_list

def extract_content(input_dict: dict, response_components: list):
    result_dict = {}
    for l in input_dict:
        result = find_headings(response_components, l)
        if result is not None:
            result_dict[result] = input_dict[l]

    for k, v in result_dict.items():
        hidden_list = []
        # print(k, type(v))
        if isinstance(v, str):
            hidden_list = extract_hidden_list(v)
            # print(hidden_list)
        if hidden_list:
            v = hidden_list
        # if k == 'team':
        #     print(type(result_dict[k]))
        #     print(result_dict[k])
        result_dict[k] = flatten_list(v)
    return result_dict