import re
import requests
import pandas as pd
import configparser


# Set Environment Values
def set_env():
    # file_path = "https://github.com/stephengeospy/bible-verse-auto-fill/bible_memory_verses.xls"
    cfg_file = "resources/bible-verse-auto-fill.cfg"
    cfg_section_name = "bible-crossway"
    file_path = "resources/sermon.txt"
    sheet_name = "crossway"
    return cfg_file, cfg_section_name, file_path, sheet_name


def get_api_cfg(section):
    config = configparser.SafeConfigParser()
    config.read(cfg_file)
    cfg_dict = {}
    cfg_dict.update({'API_KEY': config.get(section, 'API_KEY')})
    cfg_dict.update({'API_URL': config.get(section, 'API_URL')})
    return cfg_dict


def set_api_params(cfg_dict):
    params = {
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': False,
        'include-short-copyright': False,
        'include-passage-references': False
    }
    headers = {'Authorization': 'Token {}'.format(cfg_dict['API_KEY'])}
    cfg_dict.update({'PARAMS': params})
    cfg_dict.update({'HEADERS': headers})
    return cfg_dict


def get_esv_text(reference, cfg_dict):
    # cfg_dict['PARAMS']['q'] = reference
    cfg_dict['PARAMS'].update({'q': reference})
    response = requests.get(cfg_dict['API_URL'], params=cfg_dict['PARAMS'], headers=cfg_dict['HEADERS'])
    passages = response.json()['passages']
    return re.sub(r'\s\s+', ' ', passages[0].strip() if passages else 'Error: Passage not found')


if __name__ == '__main__':
    # Set Env Values
    cfg_file, cfg_section_name, file_path, sheet_name = set_env()

    # Get API Keys using ConfigParser
    cfg_dict = get_api_cfg(cfg_section_name)

    # Create Request String for API call
    cfg_dict = set_api_params(cfg_dict)

    # Iterate over each Reference to pull ESV Verse
    ref_regex = r"\w+\s\d+:\d+(-\d+)?(\s$)?"
    ref_list = []
    with open(file_path, "r") as file:
        file_content_list = file.readlines()
        for index, line in enumerate(file_content_list):
            if re.match(ref_regex, line):
                reference = re.match(ref_regex, line).group().strip()
                passage_text = get_esv_text(reference, cfg_dict)
                print(reference)
                print(passage_text)
                ref_list.append((index, reference, passage_text))
    
    for index, line in enumerate(file_content_list):
        reg_index = [local_index for local_index, tup in enumerate(ref_list) if tup[0] == index]
        if len(reg_index) > 0:
            print(line, end="")
            print(f'"{ref_list[reg_index[0]][2]}"')
        else:
            print(line, end="")
