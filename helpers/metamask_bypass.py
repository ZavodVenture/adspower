import os
import re
from shutil import rmtree


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
