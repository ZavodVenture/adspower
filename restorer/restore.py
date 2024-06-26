from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configparser import ConfigParser
from sys import exit
import re
from time import sleep
from progress.bar import Bar
from threading import Thread
import random
from string import ascii_letters, digits
import os
from shutil import rmtree


def init_exit():
    input("\nPress Enter to close program...")
    exit()


def chunks(lst, n):
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])

    return result


def worker(ws_index, metamask_index):
    options = Options()
    options.add_experimental_option("debuggerAddress", ws_list[ws_index])
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    if int(config['settings']['close_tabs']):
        tabs = driver.window_handles
        curr = driver.current_window_handle
        for tab in tabs:
            if tab == curr:
                continue
            driver.switch_to.window(tab)
            driver.close()
        driver.switch_to.window(curr)
    driver.get('about:blank')


    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="critical-error"]')))
    except:
        pass
    else:
        driver.refresh()

    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/button'))).click()
    except:
        pass
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onboarding__terms-checkbox"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-import-wallet"]'))).click()
    WebDriverWait(driver, 1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="metametrics-i-agree"]'))).click()

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'import-srp__srp-word-0')))

    words = int(config['settings']['words_number'])

    if words != 12:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[2]'))).click()

        words_list = [12, 15, 18, 21, 24]
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,f'//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[2]/select/option[{words_list.index(words) + 1}]'))).click()

    seed = metamask[metamask_index].split()
    for j in range(words):
        driver.find_element(By.ID, f'import-srp__srp-word-{j}').send_keys(seed[j])

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="import-srp-confirm"]'))).click()

    meta_password = ''.join(random.choice(ascii_letters + digits) for j in range(8)) if not config['settings']['password'] else config['settings']['password']

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@data-testid="create-password-new"]'))).send_keys(meta_password)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(((By.XPATH, '//input[@data-testid="create-password-confirm"]')))).send_keys(meta_password)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@data-testid="create-password-terms"]'))).click()

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="create-password-import"]'))).click()

    while 1:
        try:
            sleep(5)
            driver.find_element(By.XPATH, '//div[@class="loading-overlay"]')
        except:
            break
        else:
            driver.refresh()
            continue

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-complete-done"]'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-next"]'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-done"]'))).click()

    driver.get('about:blank')
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

                if 'scripts' in os.listdir(f'{adspower_path}\\extension\\{extension}\\{folder}') and 'runtime-lavamoat.js' in os.listdir(f'{adspower_path}\\extension\\{extension}\\{folder}\\scripts'):
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

            if 'scripts' in os.listdir(f'{adspower_path}\\ext\\{extension}') and 'runtime-lavamoat.js' in os.listdir(f'{adspower_path}\\ext\\{extension}\\scripts'):
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

    profiles_folders = os.listdir(f'{adspower_path}\\cache')

    for profile_dir in profiles_folders:
        profile_path = f'{adspower_path}\\cache\\{profile_dir}'

        if 'extensionCenter' in os.listdir(profile_path) and '07de772c049203839ed54e4156de1a89' in os.listdir(f'{profile_path}\\extensionCenter'):
            extension_path = f'{profile_path}\\extensionCenter\\07de772c049203839ed54e4156de1a89'
            rmtree(extension_path)

        if 'Default' in os.listdir(profile_path) and 'nkbihfbeogaeaoehlefnkodbefgpgknn' in os.listdir(f'{profile_path}\\Default\\Local Extension Settings'):
            extension_path = f'{profile_path}\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn'
            rmtree(extension_path)

    return True


config = ConfigParser()
config.read('restore.ini')

API_URl = 'http://localhost:50325/'

if __name__ == '__main__':
    print('Pre-launch verification...\n')

    try:
        status = requests.get(API_URl + 'status').json()
    except Exception:
        print('The API is unavailable. Check if AdsPower is running.')
        init_exit()
    if int(config['settings']['do_bypass']):
        if not bypass():
            print('MetaMask error. Check if the extension is installed in AdsPower.')
            init_exit()

    sleep(1)

    metamask = None
    try:
        metamask = open(config['settings']['metamask_file'])
        metamask = metamask.read().split('\n')
        if not metamask[-1]:
            metamask = metamask[:-1]
    except FileNotFoundError:
        print(f'File {config["settings"]["metamask_file"]} not found')
        init_exit()

    print('Verification is complete, search for rows associated with profiles...\n')

    first_profile = int(config['settings']['first_profile'])
    profile_number = int(config['settings']['profile_number'])

    profiles = list(range(first_profile, profile_number + first_profile))
    lines = []

    bar = Bar('Searching rows', max=len(profiles))

    for profile in profiles:
        try:
            r = requests.get(API_URl + 'api/v1/user/list', params={'serial_number': profile}).json()
        except Exception as e:
            bar.finish()
            print(f'Couldn\'t find a profile with a number {profile}: {e}')
            init_exit()
        else:
            sleep(1)
            if r['code'] != 0:
                bar.finish()
                print(f'Couldn\'t find a profile with a number {profile}: {r["msg"]}')
                init_exit()
            else:
                if not r['data']['list']:
                    bar.finish()
                    print(f'Couldn\'t find a profile with a number {profile}')
                    init_exit()

                group_id = r['data']['list'][0]['group_id']
                group_name = r['data']['list'][0]['group_name']

                offset = 0
                try:
                    offset = int(re.findall(r'Profiles(\d*)-\d*_.*', group_name)[0]) - 1
                except Exception as e:
                    bar.finish()
                    print('Could not determine the number of the first profile in the group (the group has a non-standard name)')
                    init_exit()

                try:
                    r = requests.get(API_URl + 'api/v1/user/list', params={'group_id': group_id, 'page_size': 100}).json()
                except Exception as e:
                    bar.finish()
                    print(f'Could not find profiles in the group: {e}')
                    init_exit()
                else:
                    sleep(1)
                    if r['code'] != 0:
                        bar.finish()
                        print(f'Could not find profiles in the group: {r["msg"]}')
                        init_exit()
                    else:
                        group = r['data']['list']
                        group.reverse()

                        flag = False
                        for i in range(len(group)):
                            if group[i]['serial_number'] == str(profile):
                                lines.append(offset + i)
                                flag = True
                                break
                        if not flag:
                            bar.finish()
                            print(f'Could not find the line number for the profile {profile}')
                            init_exit()
                        bar.next()

    bar.finish()

    print('\nThe rows were found successfully. Launching profiles...\n')

    bar = Bar('Launching profiles...', max=len(profiles))
    ws_list = []
    driver_path = ''

    for i in profiles:
        args = {
            'serial_number': i,
            'ip_tab': 0,
            'open_tabs': 0
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

    print('\nProfiles are running. Restoring profiles...\n')

    bar = Bar("Restoring profiles...", max=len(profiles))
    threads = chunks([Thread(target=worker, args=(i, lines[i])) for i in range(len(profiles))], 2)
    for group in threads:
        for thread in group:
            thread.start()
        for thread in group:
            thread.join()
    bar.finish()

    print('\nThe program has been successfully completed.')
    init_exit()
