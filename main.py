import os
from dotenv import load_dotenv
import modules.YaUploader as YaUploader
import json
from modules.VKClient import get_token_vk


def get_json(data):
    data_list = []
    for i in data:
        name_file = i.get('file_name')
        size_file = i.get('size')
        data_json = {'file_name': name_file, 'size_file': size_file}
        data_list.append(data_json)
    with open('file-info.json', 'w') as f:
        json.dump(data_list, f, indent=2)


if __name__ == '__main__':
    load_dotenv()
    TOKEN_YD = os.getenv('TOKEN_YD')
    TOKEN_VK = os.getenv('TOKEN_VK')
    USER_ID = os.getenv('USER_ID')

    user_one = YaUploader.YaUploader(TOKEN_VK, USER_ID, TOKEN_YD, 100)
    get_json(user_one.photo_params)
    user_one.upload_json()
    # get_token_vk()

