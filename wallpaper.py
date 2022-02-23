#!/usr/bin/env python3
import requests
import shutil
import sys
import os

image_folder_path = '/Users/{}/Pictures/bing-wallpapers'.format(os.environ['USER'])
daily_image_api_url = 'https://bingwallpaper.microsoft.com/api/BWC/getHPImages?screenWidth=3840&screenHeight=2160&env=live'


def get_image_config():
    r = requests.get(daily_image_api_url)
    if r.status_code == 200:
        result = r.json()
        return result['images']
    return None


def download_today_image():
    if not os.path.exists(image_folder_path):
        print('bing-wallpapers folder does not exist, creating one', file=sys.stderr)
        os.makedirs(image_folder_path)
    print('downloading config...', end='', file=sys.stderr)
    image_list = get_image_config()
    print('done', file=sys.stderr)
    if image_list and len(image_list) > 0:
        for image_config in image_list:
            date = image_config['startdate']
            file_name = '{}/wallpaper_{}.jpg'.format(image_folder_path, date)
            if os.path.exists(file_name):
                print('wallpaper_{}.jpg exists, skipping'.format(date), file=sys.stderr)
                continue
            base_url = image_config['urlbase']
            idx = base_url.find('&w=')
            base_url = base_url[:idx]
            print('downloading image for {}...'.format(date), end='', file=sys.stderr)
            r = requests.get(base_url, stream=True)
            if r.status_code == 200:
                with open(file_name, 'wb') as out_file:
                    shutil.copyfileobj(r.raw, out_file)
                print('done', file=sys.stderr)
        

if __name__ == '__main__':
    download_today_image()
