#!/usr/bin/env python
# coding: utf-8
# By Fox Waynne credito a Temp-Number.xyz

import os
import subprocess
import random
import sys
try:
    import requests
    import colorama
    import pyfiglet
    import pyperclip
except ModuleNotFoundError:
    if os.name == 'nt':
        _ = 'python'
    else:
        _ = 'python' + '.'.join(str(i) for i in sys.version_info[:2])
    if subprocess.run([_, '-m', 'pip', 'install', '-r', 'requirements.txt'], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        exit('\x1b[1m\x1b[92m' + '[+] Dependencias instaladas\nExecute o pograma novamente'.title().center(os.get_terminal_size().columns))
    elif subprocess.run(['pip3', 'install', '-r', 'requirements.txt'], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        exit('\x1b[1m\x1b[92m' + '[+] Depedencias instaladas\nExecute o pograma  novamente'.title().center(os.get_terminal_size().columns))
    else:
        exit('\x1b[1m\x1b[31m' + '[!] something error occured while installing dependencies\n maybe pip isn\'t installed or requirements.txt file not available?'.title().center(os.get_terminal_size().columns))
BLU = colorama.Style.BRIGHT + colorama.Fore.BLUE
CYA = colorama.Style.BRIGHT + colorama.Fore.CYAN
GRE = colorama.Style.BRIGHT + colorama.Fore.GREEN
YEL = colorama.Style.BRIGHT + colorama.Fore.YELLOW
RED = colorama.Style.BRIGHT + colorama.Fore.RED
MAG = colorama.Style.BRIGHT + colorama.Fore.MAGENTA
LIYEL = colorama.Style.BRIGHT + colorama.Fore.LIGHTYELLOW_EX
LIRED = colorama.Style.BRIGHT + colorama.Fore.LIGHTRED_EX
LIMAG = colorama.Style.BRIGHT + colorama.Fore.LIGHTMAGENTA_EX
LIBLU = colorama.Style.BRIGHT + colorama.Fore.LIGHTBLUE_EX
LICYA = colorama.Style.BRIGHT + colorama.Fore.LIGHTCYAN_EX
LIGRE = colorama.Style.BRIGHT + colorama.Fore.LIGHTGREEN_EX
BOLD = colorama.Style.BRIGHT
LIMPAR = 'cls' if os.name == 'nt' else 'clear'
CORES = BLU, CYA, GRE, YEL, RED, MAG, LIYEL, LIRED, LIMAG, LIBLU, LICYA, LIGRE
FONTES = 'basic', 'o8', 'cosmic', 'graffiti', 'chunky', 'epic', 'doom', 'avatar', #'poison'
global font
font = random.choice(FONTES)
colorama.init(autoreset=True)

def logo() -> None:
    os.system(LIMPAR)
    cor1 = random.choice(CORES)
    cor2 = random.choice(CORES)
    while cor1 == cor2:
        cor2 = random.choice(CORES)
    print(cor1 + '_' * os.get_terminal_size().columns, end='\n'*2)
    print(cor2 + pyfiglet.figlet_format('FOXS\nBLINTERS', font=font, justify='center', width=os.get_terminal_size().columns), end='')
    msg = '[+] By Fox Waynne'
    _ = int(os.get_terminal_size().columns/2)
    _ -= int(len(msg)/2)
    print(cor1 + '_' * _ + LIYEL + msg + cor1 + '_' * _ + '\n')

def fetch_countries() -> dict:
    url = 'https://temp-numbers.xyz/admin/API/country_catagory.php'
    headers = {
        'Host': 'temp-numbers.xyz',
        'accept-encoding': 'gzip',
        'user-agent': 'okhttp/4.9.0'
    }
    return requests.get(url, headers=headers).json()

def list_numbers(country:str) -> dict:
    url = 'https://temp-numbers.xyz/admin/API/get_lsit.php'
    params = {
        'no': country
    }
    headers = {
        'Host': 'temp-numbers.xyz',
        'accept-encoding': 'gzip',
        'user-agent': 'okhttp/4.9.0'
    }
    return requests.post(url, params=params, headers=headers).json()

def copy_clipboard(text:str) -> tuple:
    '''Error codes
        1: termux api pelo apt não installada
        2: termux api app não instalado
        3: Não tem o termux'''
    try:
        pyperclip.copy(text)
    except Exception:
        try:
            if subprocess.check_output(['uname', '-o']).strip() == b'Android':
                try:
                    if subprocess.call(['termux-clipboard-set', text],
                    stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, timeout=4) == 0:
                        return True, None
                except FileNotFoundError:
                    return False, 'Falha ao copiar para a área de transferência! Instale o pacote termux-API "apt install termux-api"'
                except subprocess.TimeoutExpired:
                    return False, 'Falha ao copiar para a área de transferência! Instale o aplicativo termux-API "https://www.mediafire.com/file/vlgkmdqodyoxla6/Termux.API.ver.0.49.build.49.apk/file"'
        except FileNotFoundError:
            return False, 'Falha ao copiar para a área de transferência! Você está em um ambiente desconhecido'
    else:
        return True, None
def fetch_sms(number:str) -> dict:
    url = 'https://temp-numbers.xyz/API/getAllMessages.php'
    params = {
        'no': number
    }
    headers = {
        'Host': 'temp-numbers.xyz',
        'accept-encoding': 'gzip',
        'user-agent': 'okhttp/4.9.0'
    }
    return requests.post(url, headers=headers, params=params).json()

def print_sms(number:str) -> None:
    sms_list = fetch_sms(number)
    perc = int(len(sms_list)*20/100)
    # random.choice(color_list) + 'press <enter> to go to main menu'.title().center(os.get_terminal_size().columns)
    for i in sms_list[:perc]:
        print('{}{} {} {}'.format(random.choice(CORES),
        i['FromNumber'], repr(i['Messagebody']), i['message_time']
        ))
        print('_' * os.get_terminal_size().columns)

def check_update() -> tuple:
    latest = requests.get(
        'https://raw.githubusercontent.com/Sl-Sanda-Ru/Temp-SMS-Receive/main/.version'
        ).text.strip()
    with open('.version') as version:
        if version.read().strip() != latest:
            return True, latest
        else:
            return False, '0'

def update():
    if '.git' in os.listdir():
        _ = subprocess.run(['git', 'stash'], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _ = subprocess.run(['git', 'pull'], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        for i in os.listdir():
            if i == '.git':
                continue
            latest_source = requests.get(
                f'https://raw.githubusercontent.com/Foxys0007/update/F0x-SMS/{i}'
                ).content
            with open(i, 'wb') as file:
                file.write(latest_source)

def main():
    try:
        logo()
        tmp_countries = fetch_countries()
        for i in enumerate(tmp_countries, start=1):
            print(f'{random.choice(CORES)}{i[0]}. {i[1]["country_code"]} {i[1]["Country_Name"]}'.center(os.get_terminal_size().columns))
        while True:
            try:
                choice = int(input(BOLD + 'Digite o numero da regiao: '))
                if choice <= 0 or choice > len(tmp_countries):
                    print(f'{RED}[!] Opção Incorreta'.center(os.get_terminal_size().columns))
                else:
                    break
            except ValueError:
                print(f'{RED}[!] Opção icorreta'.center(os.get_terminal_size().columns))
            except KeyboardInterrupt:
                exit(0)
        number_list = list_numbers(tmp_countries[choice-1]['Country_Name'])
        for i in enumerate(number_list, start=1):
            print('{}{}. {} {}'.format(random.choice(CORES), i[0], i[1]['ToNumber'], i[1]['realtime']).center(os.get_terminal_size().columns))
        while True:
            try:
                choice = input(BOLD + 'Digite o número necessário "R" para aleatório: ')
                if int(choice) <= 0 or int(choice) > len(number_list):
                    print(f'{RED}[!] Opção Incorreta'.center(os.get_terminal_size().columns))
                else:
                    break
            except ValueError:
                if choice.isalpha() and choice.upper() == 'R':
                    break
                else:
                    print(f'{RED}[!] Opção Incorreta'.center(os.get_terminal_size().columns))
        if choice.upper() == 'R':
            per = int(len(number_list)*20/100)
            weight = [2 for i in range(per)] + [1 for i in range(len(number_list)-per)]
            rnd = random.choices(number_list,weights=weight,k=1)[0]['ToNumber']
        while True:
            try:
                print(f'{random.choice(CORES)}Numero Selecionado: {rnd}'.center(os.get_terminal_size().columns))
                _ = copy_clipboard(rnd)
                if not _[0] == True:
                    print(RED + _[1].center(os.get_terminal_size().columns))
                else:
                    print(GRE + 'Numero copiado para a area de transferencia'.center(os.get_terminal_size().columns))
                print_sms(rnd)
            except NameError:
                print(f'{random.choice(CORES)}Numero Selecionado: {number_list[int(choice)-1]["ToNumber"]}'.center(os.get_terminal_size().columns))
                _ = copy_clipboard(number_list[int(choice)-1]['ToNumber'])
                if not _[0] == True:
                    print(RED + _[1].center(os.get_terminal_size().columns))
                else:
                    print(GRE + 'Numero copiado para a area de trabalho'.center(os.get_terminal_size().columns))
                print_sms(number_list[int(choice)-1]['ToNumber'])
            print(BOLD + 'Pressione <Enter> Para Recarreagar as msg'.center(os.get_terminal_size().columns))
            input(BOLD + 'Ou ctrl+c Para o Menu Iniciar'.center(os.get_terminal_size().columns))
            logo()
    except KeyboardInterrupt:
        main()
if __name__ == '__main__':
    if check_update()[0]:
        print(RED + '\t[!] Atualização Econtrada'.title().center(os.get_terminal_size().columns))
        print(LIGRE + '\t[+] Atualizando...'.title().center(os.get_terminal_size().columns))
        update()
        exit(LIGRE + '\t[+] Atualização Completa...\n\t rode o pograma novamente'.title().center(os.get_terminal_size().columns))
    main()