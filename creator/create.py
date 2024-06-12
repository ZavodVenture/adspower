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
from selenium.webdriver.support import expected_conditions as EC
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


def worker(index):
    options = Options()
    options.add_experimental_option("debuggerAddress", ws_list[index])
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    WebDriverWait(driver, 60).until_not(EC.number_of_windows_to_be(1))
    sleep(5)
    windows = driver.window_handles
    for window in range(len(driver.window_handles) - 1):
        driver.switch_to.window(windows[window])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="critical-error"]')))
    except:
        pass
    else:
        driver.refresh()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="onboarding__terms-checkbox"]'))).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-import-wallet"]'))).click()
    WebDriverWait(driver, 1)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="metametrics-i-agree"]'))).click()

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'import-srp__srp-word-0')))

    words = int(config['Settings']['words_number'])

    if words != 12:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[2]'))).click()

        words_list = [12, 15, 18, 21, 24]
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[2]/select/option[{words_list.index(words) + 1}]'))).click()

    seed = metamask[index].split()
    for j in range(words):
        driver.find_element(By.ID, f'import-srp__srp-word-{j}').send_keys(seed[j])

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="import-srp-confirm"]'))).click()

    meta_password = ''.join(random.choice(ascii_letters + digits) for j in range(8)) if not config['Settings']['password'] else config['Settings']['password']

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@data-testid="create-password-new"]'))).send_keys(
        meta_password)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(((By.XPATH, '//input[@data-testid="create-password-confirm"]')))).send_keys(
        meta_password)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@data-testid="create-password-terms"]'))).click()

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="create-password-import"]'))).click()

    driver.implicitly_wait(5)

    while 1:
        try:
            sleep(5)
            driver.find_element(By.XPATH, '//div[@class="loading-overlay"]')
        except:
            break
        else:
            driver.refresh()
            continue

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-complete-done"]'))).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-next"]'))).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-done"]'))).click()

    if discord:
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
                WebDriverWait(driver, 7).until(EC.url_to_be("https://discord.com/channels/@me"))
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
            driver.get("https://www.google.com/")
    else:
        driver.get("https://www.google.com/")

    bar.next()


def bypass():
    for disk in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
        try:
            os.listdir(f'{disk}:\.ADSPOWER_GLOBAL')
        except FileNotFoundError:
            continue
        else:
            adspower_path = f'{disk}:\.ADSPOWER_GLOBAL'
            break
    else:
        return False

    if 'extension' in os.listdir(adspower_path):
        extension_folders = os.listdir(f'{adspower_path}\\extension')

        extension_changed = False

        for extension in extension_folders:
            current_extension_folders = os.listdir(f'{adspower_path}\\extension\\{extension}')

            for folder in current_extension_folders:
                if not os.path.isdir(f'{adspower_path}\\extension\\{extension}\\{folder}'):
                    continue

                if 'scripts' in os.listdir(
                        f'{adspower_path}\\extension\\{extension}\\{folder}') and 'runtime-lavamoat.js' in os.listdir(
                        f'{adspower_path}\\extension\\{extension}\\{folder}\\scripts'):
                    lavamoat_path = f'{adspower_path}\\extension\\{extension}\\{folder}\\scripts\\runtime-lavamoat.js'
                    with open(lavamoat_path, encoding='utf-8') as file:
                        text = file.read()
                        file.close()
                    with open(lavamoat_path, 'w', encoding='utf-8') as file:
                        replaced_text = re.sub(r'} = {"scuttleGlobalThis":\{.*}',
                                               '} = {"scuttleGlobalThis":{"enabled":false,"scuttlerName":"SCUTTLER","exceptions":[]}}',
                                               text)
                        file.write(replaced_text)
                        file.close()

                    extension_changed = True

                if 'runtime-lavamoat.js' in os.listdir(f'{adspower_path}\\extension\\{extension}\\{folder}'):
                    lavamoat_path = f'{adspower_path}\\extension\\{extension}\\{folder}\\runtime-lavamoat.js'
                    with open(lavamoat_path, encoding='utf-8') as file:
                        text = file.read()
                        file.close()
                    with open(lavamoat_path, 'w', encoding='utf-8') as file:
                        replaced_text = re.sub(r'} = {"scuttleGlobalThis":\{.*}',
                                               '} = {"scuttleGlobalThis":{"enabled":false,"scuttlerName":"SCUTTLER","exceptions":[]}}',
                                               text)
                        file.write(replaced_text)
                        file.close()

                    extension_changed = True

        if not extension_changed:
            return False

    if 'ext' in os.listdir(adspower_path):
        ext_folders = os.listdir(f'{adspower_path}\\ext')

        extension_changed = False

        for extension in ext_folders:
            if not os.path.isdir(f'{adspower_path}\\ext\\{extension}'):
                continue

            if 'scripts' in os.listdir(f'{adspower_path}\\ext\\{extension}') and 'runtime-lavamoat.js' in os.listdir(
                    f'{adspower_path}\\ext\\{extension}\\scripts'):
                lavamoat_path = f'{adspower_path}\\ext\\{extension}\\scripts\\runtime-lavamoat.js'

                with open(lavamoat_path, encoding='utf-8') as file:
                    text = file.read()
                    file.close()
                with open(lavamoat_path, 'w', encoding='utf-8') as file:
                    replaced_text = re.sub(r'} = {"scuttleGlobalThis":\{.*}',
                                           '} = {"scuttleGlobalThis":{"enabled":false,"scuttlerName":"SCUTTLER","exceptions":[]}}',
                                           text)
                    file.write(replaced_text)
                    file.close()

                extension_changed = True

            if 'runtime-lavamoat.js' in os.listdir(f'{adspower_path}\\ext\\{extension}'):
                lavamoat_path = f'{adspower_path}\\ext\\{extension}\\runtime-lavamoat.js'
                with open(lavamoat_path, encoding='utf-8') as file:
                    text = file.read()
                    file.close()
                with open(lavamoat_path, 'w', encoding='utf-8') as file:
                    replaced_text = re.sub(r'} = {"scuttleGlobalThis":\{.*}',
                                           '} = {"scuttleGlobalThis":{"enabled":false,"scuttlerName":"SCUTTLER","exceptions":[]}}',
                                           text)
                    file.write(replaced_text)
                    file.close()
                extension_changed = True

        if not extension_changed:
            return False

    return True


if __name__ == '__main__':
    print('Pre-launch verification...\n')

    try:
        status = requests.get(API_URl + 'status').json()
    except Exception:
        print('The API is unavailable. Check if AdsPower is running.')
        init_exit()

    if not bypass():
        print('MetaMask error. Check if the extension is installed in AdsPower.')
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
