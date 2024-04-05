import requests
from configparser import ConfigParser
from sys import exit
import re
from time import sleep
from progress.bar import Bar
from threading import Thread
from helpers import adspower, readers, metamask_bypass, workers

config = ConfigParser()
config.read('restore.ini')

CURRENT_THREADS = 0
MAX_THREADS = int(config['Settings']['profile_setup_number'])
ERRORS = []

API_URl = 'http://localhost:50325/'


def init_exit():
    input("\nPress Enter to close program...")
    exit()


def worker(bar: Bar, serial_number, seed, ws, driver_path, password):
    global CURRENT_THREADS

    try:
        workers.old_metamask(seed, ws, driver_path, password)
    except:
        ERRORS.append(str(serial_number))
    finally:
        CURRENT_THREADS -= 1
        bar.next()


def main():
    global CURRENT_THREADS

    print('Pre-launch verification...\n')

    try:
        adspower.check_adspower()
    except:
        print('The API is unavailable. Check if AdsPower is running.')
        init_exit()

    try:
        r = metamask_bypass.bypass()
    except:
        print('MetaMask critical error')
        init_exit()
    else:
        if not r:
            print('MetaMask error. Check if the extension is installed in AdsPower.')

    try:
        seeds = readers.read_file(config['Settings']['metamask_file'])
    except FileNotFoundError:
        print(f'File {config["Settings"]["metamask_file"]} not found')
        init_exit()

    print('Verification is complete, search for rows associated with profiles...\n')

    first_profile = int(config['Settings']['first_profile'])
    profile_number = int(config['Settings']['profile_number'])

    profiles = list(range(first_profile, profile_number + first_profile))
    lines = []

    bar = Bar('Searching rows', max=len(profiles))
    bar.start()

    for profile in profiles:
        try:
            profile_data = adspower.get_profile(profile)
        except Exception as e:
            print(f'Profile searching error: {e}')
            init_exit()

        group_id = profile_data['group_id']
        group_name = profile_data['group_name']

        try:
            offset = int(re.findall(r'Profiles(\d*)-\d*_.*', group_name)[0]) - 1
        except:
            print('Could not determine the number of the first profile in the group (the group has a non-standard name)')
            init_exit()

        try:
            profiles_in_group = adspower.get_profiles_by_group_id(group_id)
        except Exception as e:
            print(f'Searching profiles in selected group error: {e}')
            init_exit()

        profiles_in_group.reverse()

        for i in range(len(profiles_in_group)):
            if profiles_in_group[i]['serial_number'] == str(profile):
                lines.append(offset + i)
                break
        else:
            print(f'Could not find the line number for the profile {profile}')
            init_exit()

        bar.next()

    bar.finish()

    print('\nThe rows were found successfully. Launching profiles...\n')

    bar = Bar('Launching profiles...', max=len(profiles))
    bar.start()
    ws_list = []
    driver_path = ''

    for serial_number in profiles:
        try:
            ws, dp = adspower.run_profile(serial_number)
        except Exception as e:
            print(f'\nFailed to launch profile: {e}')
            init_exit()
        else:
            ws_list.append(ws)
            driver_path = dp

        bar.next()

    bar.finish()

    print('\nProfiles are running. Restoring profiles...\n')

    bar = Bar("Restoring profiles...", max=len(profiles))
    bar.start()

    for i in range(profile_number):
        while CURRENT_THREADS >= MAX_THREADS:
            continue

        CURRENT_THREADS += 1

        thread = Thread(target=worker, args=(bar, profiles[i], seeds[lines[i]], ws_list[i], driver_path, config['Settings']['password']))
        thread.start()

    while CURRENT_THREADS != 0:
        continue

    bar.finish()

    print('\nThe program has been successfully completed.')

    if ERRORS:
        print(f'\nErrors on profiles: {", ".join(ERRORS)}')

    init_exit()


if __name__ == '__main__':
    main()
