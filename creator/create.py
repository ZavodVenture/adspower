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


def import_discord(driver, index):
    driver.get('https://discord.com/login/')

    script = """function login(token) {
            setInterval(() => {
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
            }, 50);
            setTimeout(() => {
            location.reload();
            }, 2500);
            }

            login('%s')""" % discord[index]

    attempts = 0
    while attempts != 3:
        driver.execute_script(script)
        try:
            WebDriverWait(driver, 7).until(ec.url_to_be("https://discord.com/channels/@me"))
        except Exception:
            attempts += 1
            continue
        else:
            break

    if attempts == 3:
        with open('errors.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.now()} - Не удалось войти в дискорд ({offset + index + 1} строка в файле)\n')
            file.close()
    else:
        driver.get("about:blank")


def import_keplr(driver: webdriver.Chrome, metamask_index):
    extensions = get_exts(driver)

    try:
        martin_id = [ex['id'] for ex in extensions if 'Keplr' in ex['name']][0]
    except IndexError:
        raise Exception('Keplr extension not found')

    driver.get(f'chrome-extension://{martin_id}/register.html')

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[3]/div[3]/button'))).click()
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div/div[5]/button'))).click()
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div/div/form/div[3]/div/div/div[1]//input')))

    sleep(2)

    inputs = driver.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div/div/form/div[3]/div/div/div[1]//input')

    seed = metamask[metamask_index].split()

    for j in range(12):
        inputs[j].send_keys(seed[j])

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div/div/form/div[6]/div/button'))).click()

    inp = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[1]/div[2]/div/div/input')))
    sleep(2)
    inp.send_keys('Wallet')

    meta_password = ''.join(random.choice(ascii_letters + digits) for _ in range(8)) if not config['Settings']['password'] else config['Settings']['password']

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[3]/div[2]/div/div/input'))).send_keys(meta_password)
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[5]/div[2]/div/div/input'))).send_keys(meta_password)

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[7]/button'))).click()
    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[9]/div/button'))).click()

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

    import_keplr(driver, index)

    if discord:
        import_discord(driver, index)

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
