import re
import requests
import configparser
from os import makedirs, path, walk


def set_env():
    cfg_file = "resources/bible-verse-auto-fill.cfg"
    cfg_section_name = "bible-crossway"
    sheet_name = "crossway"
    sermon_in_path = "resources/sermon_notes_in"
    sermon_out_path = "resources/sermon_notes_out"
    return cfg_file, cfg_section_name, sheet_name, sermon_in_path, sermon_out_path


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
    cfg_dict['PARAMS'].update({'q': reference})
    response = requests.get(cfg_dict['API_URL'], params=cfg_dict['PARAMS'], headers=cfg_dict['HEADERS'])
    passages = response.json()['passages']
    return re.sub(r'\s\s+', ' ', passages[0].strip() if passages else 'Error: Passage not found')


def build_gateway_url(reference):
    ref_regex_for_url = r"(\w+\s)(\d+):(\d+)(-\d+)?(\s*\w+)?"
    book, chapter, verse, ext_verse, version = re.search(ref_regex_for_url, reference).groups()
    
    if ext_verse is not None:
        verse = verse + ext_verse
    
    if version is None:
        version = "ESV"
    
    reference_url = f'{base_url}{book.strip()}+{chapter}%3A{verse}&version={version.strip()}'
    return f'[{reference}]({reference_url} "{reference}")  '


if __name__ == '__main__':
    cfg_file, cfg_section_name, sheet_name, sermon_in_path, sermon_out_path = set_env()
    cfg_dict = get_api_cfg(cfg_section_name)
    cfg_dict = set_api_params(cfg_dict)

    base_url = "https://www.biblegateway.com/passage/?search="
    ref_regex = r"\w+\s\d+:\d+(-\d+)?(\s\w+$)?"

    for dirname, directories, files in walk(sermon_in_path):
        for file_name in files:
            if dirname.endswith("/"):
                dirname = dirname[:-1]
            
            if not str(file_name).endswith(".md") and not str(file_name).endswith(".txt"):
                print(f"BadFile: {dirname}/{file_name}")
                continue

            print(f"Processing: {dirname}/{file_name}")
            ref_list = []
            with open(f"{dirname}/{file_name}", "r") as fr:
                file_content_list = fr.readlines()
                for index, line in enumerate(file_content_list):
                    if re.match(ref_regex, line):
                        reference = re.match(ref_regex, line).group().strip()
                        passage_text = get_esv_text(reference, cfg_dict)
                        gateway_url = build_gateway_url(reference)
                        ref_list.append((index, reference, gateway_url, passage_text))
            
            dirname = dirname.replace(sermon_in_path + "/", "")
            sermon_out_path = f"{sermon_out_path}/{dirname}"
            if not path.isdir(sermon_out_path):
                print("Creating New Directory: {sermon_out_path}")
                makedirs(sermon_out_path)

            with open(f"{sermon_out_path}/{file_name}", "w") as fw:
                for index, line in enumerate(file_content_list):
                    reg_index = [local_index for local_index, tup in enumerate(ref_list) if tup[0] == index]
                    if len(reg_index) > 0:
                        print(f'{ref_list[reg_index[0]][2]}', file=fw)
                        print(f'"{ref_list[reg_index[0]][3]}"', file=fw)
                    else:
                        print(line, end="", file=fw)
