from sys import exit
from configparser import ConfigParser
from progress.bar import Bar
from threading import Thread
from helpers import adspower, metamask_bypass, readers, workers

config = ConfigParser()
config.read('config.ini')
profile_number = int(config['Settings']['profiles_number'])

CURRENT_THREADS = 0
MAX_THREADS = int(config['Settings']['profile_setup_numbers'])
ERRORS = []

API_URl = 'http://localhost:50325/'


def init_exit():
    input("\nPress Enter to close program...")
    exit()


def worker(bar: Bar, serial_number, seed, ws, driver_path, password):
    global CURRENT_THREADS

    try:
        workers.new_metamask(seed, ws, driver_path, password)
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

    try:
        proxy = readers.read_file(config['Settings']['proxy_file'])
    except FileNotFoundError:
        print(f'File {config["Settings"]["proxy_file"]} not found. Proxies will not be used.\n')
        proxy = None

    offset = int(config['Settings']['offset'])
    seeds = seeds[offset:]
    if proxy:
        proxy = proxy[offset:]

    if profile_number > len(seeds) or proxy and profile_number > len(proxy):
        print('The number of lines in files, taking into account the offset, is less than the number of profiles specified in the settings.')
        init_exit()

    print('Verification is complete. Creating AdsPower profiles...\n')

    group_name = f'Profiles{offset + 1}-{offset + profile_number}_{config["Settings"]["group_name"]}'

    group_id = None

    try:
        group_id = adspower.get_group_id(group_name)
    except:
        pass

    if not group_id:
        try:
            group_id = adspower.create_group(group_name)
        except Exception as e:
            print(f'Failed to create AdsPower profile group: {e}')
            init_exit()

    profile_ids = []
    bar = Bar('Creating profiles', max=profile_number)
    bar.start()

    for i in range(profile_number):
        try:
            profile_ids.append(adspower.create_profile(proxy[i] if proxy else None, group_id))
        except Exception as e:
            print(f'\nCouldn\'t create profile: {e}')
            init_exit()
        bar.next()

    bar.finish()

    print('\nProfiles have been created successfully. Launching profiles...\n')

    bar = Bar("Launching profiles", max=profile_number)
    bar.start()
    ws_list = []

    for serial_number in profile_ids:
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

    print('\nProfiles are running. Configuring profiles...\n')

    bar = Bar("Configuring profiles", max=profile_number)
    bar.start()

    for i in range(profile_number):
        while CURRENT_THREADS >= MAX_THREADS:
            continue

        CURRENT_THREADS += 1
        thread = Thread(target=worker, args=(bar, profile_ids[i], seeds[i], ws_list[i], driver_path, config['Settings']['password']))
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
