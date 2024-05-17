import os
import re
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
from sys import exit
from configparser import ConfigParser
from progress.bar import Bar
from time import sleep
from threading import Thread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from string import digits, ascii_letters
from datetime import datetime

config = ConfigParser()
config.read('config.ini')
profile_numbers = int(config['Settings']['profiles_number'])

API_URl = 'http://localhost:50325/'


def init_exit():
    input("\nPress Enter to close program...")
    exit()


def chunks(lst, n):
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])

    return result


def get_exts(driver):
    driver.get('chrome://extensions/')

    sleep(5)

    script = '''ext_manager = document.getElementsByTagName('extensions-manager')[0].shadowRoot;
    item_list = ext_manager.getElementById('items-list').shadowRoot;
    container = item_list.getElementById('container');
    extension_list = container.getElementsByClassName('items-container')[1].getElementsByTagName('extensions-item');

    var extensions = [];

    for (i = 0; i < extension_list.length; i++) {
        console.log(extension_list[i]);
        name = extension_list[i].shadowRoot.getElementById('name').textContent;
        id = extension_list[i].id;
        extensions.push({'id': id, 'name': name});
    }

    return extensions;'''

    return driver.execute_script(script)


def import_phantom(driver: webdriver.Chrome, metamask_index):
    extensions = get_exts(driver)

    try:
        ext_id = [ex['id'] for ex in extensions if 'Phantom' in ex['name']][0]
    except IndexError:
        raise Exception('Phantom extension not found')

    driver.get(f'chrome-extension://{ext_id}/onboarding.html')

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/div/div[2]/button[2]'))).click()
    sleep(0.5)
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/div/div[2]'))).click()

    WebDriverWait(driver, 15).until(ec.presence_of_element_located((By.XPATH, '//input[@data-testid="secret-recovery-phrase-word-input-0"]')))

    seed = metamask[metamask_index].split()

    for i in range(12):
        driver.find_element(By.XPATH, f'//input[@data-testid="secret-recovery-phrase-word-input-{i}"]').send_keys(seed[i])

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/form/button'))).click()
    WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/form/button[2]'))).click()

    # dismiss whip wet immense mechanic point guilt canyon clever detect unhappy find

    meta_password = ''.join(random.choice(ascii_letters + digits) for _ in range(8)) if not config['Settings']['password'] else config['Settings']['password']

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/form/div[1]/div[2]/input'))).send_keys(meta_password)
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/form/div[1]/div[2]/div/div/input'))).send_keys(meta_password)
    sleep(0.5)
    WebDriverWait(driver, 15).until(ec.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div[2]/form/div[2]/span/input'))).click()
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/form/button'))).click()

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/form/button')))

    driver.get(f'chrome-extension://{ext_id}/popup.html')
    sleep(0.5)

    while 1:
        try:
            WebDriverWait(driver, 2).until(ec.element_to_be_clickable((By.XPATH, '//div[@data-testid="settings-menu-open-button"]'))).click()
        except:
            driver.refresh()
        else:
            break
    sleep(0.5)
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//div[@data-testid="sidebar_menu-button-settings"]'))).click()
    sleep(0.5)
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//div[@data-testid="settings-item-security-and-privacy"]'))).click()
    sleep(0.5)
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//div[@class="sc-cidDSM jFTnWc"]/div[2]'))).click()
    sleep(0.5)
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//div[@class="sc-icMgfS dcgSON"]/div[9]'))).click()
    sleep(0.5)

    driver.get('about:blank')


def worker(index):
    options = Options()
    options.add_experimental_option("debuggerAddress", ws_list[index])
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    sleep(3)

    try:
        driver.maximize_window()
    except:
        pass

    WebDriverWait(driver, 60).until_not(ec.number_of_windows_to_be(1))
    sleep(5)
    windows = driver.window_handles
    for window in range(len(driver.window_handles) - 1):
        driver.switch_to.window(windows[window])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])

    import_phantom(driver, index)

    bar.next()


if __name__ == '__main__':
    print('Pre-launch verification...\n')

    try:
        status = requests.get(API_URl + 'status').json()
    except Exception:
        print('The API is unavailable. Check if AdsPower is running.')
        init_exit()

    metamask = None
    proxy = None
    discord = None
    try:
        metamask = open(config['Settings']['metamask_file'])
        metamask = metamask.read().split('\n')
        if not metamask[-1]:
            metamask = metamask[:-1]
    except FileNotFoundError:
        print(f'File {config["Settings"]["metamask_file"]} not found')
        init_exit()

    try:
        proxy = open(config['Settings']['proxy_file'])
        proxy = proxy.read().split('\n')
    except FileNotFoundError:
        print(f'File {config["Settings"]["proxy_file"]} not found. Proxies will not be used.\n')

    try:
        discord = open(config['Settings']['discord_file'])
        discord = discord.read().split('\n')
    except FileNotFoundError:
        print(f'File {config["Settings"]["discord_file"]} not found. Discords will not be used.\n')

    offset = int(config['Settings']['offset'])

    metamask = metamask[offset:]
    metamask_len = len(metamask)
    if proxy:
        proxy = proxy[offset:]
        proxy_len = len(proxy)
    else:
        proxy_len = metamask_len

    if discord:
        discord = discord[offset:]
        discord_len = len(discord)
    else:
        discord_len = metamask_len

    if profile_numbers > proxy_len or\
       profile_numbers > discord_len or\
       profile_numbers > metamask_len:
        print('The number of lines in files, taking into account the offset, is less than the number of profiles specified in the settings.\n'
              f'Will be created {min(proxy_len, discord_len, metamask_len)} profiles except {profile_numbers}\n')
        profile_numbers = min(proxy_len, discord_len, metamask_len)

    print('Verification is complete. Creating AdsPower profiles...\n')

    group_name = f'Profiles{offset+1}-{offset+profile_numbers}_{config["Settings"]["group_name"]}'
    group_id = 0

    try:
        r = requests.get(API_URl + 'api/v1/group/list').json()
    except Exception as e:
        pass
    else:
        if r['code'] == 0:
            for i in r['data']['list']:
                if i['group_name'] == group_name:
                    group_id = i['group_id']
                    break

    if not group_id:
        try:
            r = requests.post(API_URl + 'api/v1/group/create', json={'group_name': group_name}).json()
        except Exception as e:
            print('Failed to create AdsPower profile group: ' + str(e))
            init_exit()
        else:
            if r['code'] != 0:
                print('Failed to create AdsPower profile group: ' + r['msg'])
                init_exit()
            else:
                group_id = r['data']['group_id']

    profile_ids = []
    bar = Bar('Creating profiles', max=profile_numbers)
    for i in range(profile_numbers):
        if proxy:
            host, port, user, password = proxy[i].split(':')
            account_data = {
                'group_id': group_id,
                'user_proxy_config': {
                    'proxy_soft': 'other',
                    'proxy_type': config['Settings']['proxy_type'],
                    'proxy_host': host,
                    'proxy_port': port,
                    'proxy_user': user,
                    'proxy_password': password
                }
            }
        else:
            account_data = {
                'group_id': group_id,
                'user_proxy_config': {
                    'proxy_soft': 'no_proxy'
                }
            }

        try:
            r = requests.post(API_URl + 'api/v1/user/create', json=account_data).json()
        except Exception as e:
            bar.finish()
            print('\nCouldn\'t create profile: ' + str(e))
            init_exit()
        else:
            if r['code'] != 0:
                bar.finish()
                print('\nCouldn\'t create profile: ' + r['msg'])
                init_exit()
            else:
                profile_ids.append(r['data']['id'])
                bar.next()

        sleep(1)

    bar.finish()

    print('\nProfiles have been created successfully. Launching profiles...\n')

    bar = Bar("Launching profiles", max=profile_numbers)
    ws_list = []
    driver_path = ''
    for i in profile_ids:
        args = {
            'user_id': i,
            'ip_tab': 0
        }
        try:
            r = requests.get(API_URl + 'api/v1/browser/start', params=args).json()
        except Exception as e:
            bar.finish()
            print('\nFailed to launch profile: ' + str(e))
            init_exit()
        else:
            if r['code'] != 0:
                bar.finish()
                print('\nFailed to launch profile: ' + r['msg'])
                init_exit()
            else:
                ws_list.append(r["data"]["ws"]["selenium"])
                if not driver_path:
                    driver_path = r["data"]["webdriver"]
                bar.next()
        sleep(1)

    bar.finish()

    print('\nProfiles are running. Configuring profiles...\n')

    bar = Bar("Configuring profiles", max=profile_numbers)

    threads = chunks([Thread(target=worker, args=(i,)) for i in range(profile_numbers)], int(config['Settings']['profile_setup_numbers']))
    for group in threads:
        for thread in group:
            thread.start()
        for thread in group:
            thread.join()

    bar.finish()

    print('\nThe program has been successfully completed.')
    init_exit()
