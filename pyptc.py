#!/bin/python
# coding: utf-8
# Author: https://twitter.com/27Sawyer
# Version: beta 1.0
# Licence: GPLv2
# +-----------------------------------------------------------------------
# pip install selenium
# pip install beautifulsoup4
# pip install requests
# +-----------------------------------------------------------------------
__author__ = '@27Sawyer'
__version__ = 'beta 1.0'

import argparse,time,sys,requests,random,re,signal
from selenium import webdriver
from bs4 import BeautifulSoup

_ptc = '';_user = '';_pass = ''
neobux = 'https://www.neobux.com/m/l/'

# +-----------------------------------------------------------------------

def detect_popup(driver):
    "Funcion que detecta ventanas emergentes"
    try:
        alert = driver.switch_to_alert()
        alert.accept()
        print('[*] alert accept!')
    except:
        None

def detect_ads(_cookies):
    driver = webdriver.Firefox()
    driver.get('http://www.neobux.com/m/v/')
    for cookie in _cookies:
        driver.add_cookie(cookie)
    driver.refresh()

    sourcepage = BeautifulSoup(driver.page_source)                  # Source Code

    # +-------------------------------------------------------------------
    def search_advertising():
        ads = re.findall(r'id="l0l(.*?)</td></tr></tbody></table></td></tr></tbody></table>', str(sourcepage))
        i = 0; ads_number = []
        for x in ads:
            l = re.findall(r'http://cache1.neodevlda.netdna-cdn.com/imagens/estrela_16.gif"', ads[i])
            i += 1
            if len(l) > 0:
                ads_number.append(re.findall(r'(.*?)" onclick="ggz\(', x))

        for x in ads_number:
            value = str(x).replace('\'','').replace('[','').replace(']','')
            driver.find_element_by_id('l0l' + value).click()                        # abrir
            driver.find_element_by_id('i' + value).click()                          # abrir, punto rojo
            time.sleep(25)

            win = driver.window_handles                                             # Lista de ventanas abiertas
            driver.switch_to_window(win[1])                                         # Cambiamos ventana
            sourcepage_text = BeautifulSoup(driver.page_source).get_text()

            if sourcepage_text.find('Ya ha visto este anuncio') >= 0 or sourcepage_text.find('El anuncio seleccionado no esta disponible.') >= 0:
                print('[*] Ads seen - window closed ... ')
                driver.close()
                detect_popup(driver)                                                # En caso de ventana emergente
                driver.switch_to_window(win[0])                                     # Cambiamos ventana Main
            else:
                print('[-] Ads in process ...')
                try:
                    driver.find_element_by_link_text('Cerrar').click()
                    print('[-] Ads Complete =)')
                except:
                    print('[!] Failed to find ads, recharging ...')
                    driver.close()
                detect_popup(driver)
                driver.switch_to_window(win[0])                                     # Cambiamos ventana (ventana main)
        driver.close()
    # +-------------------------------------------------------------------
    search_advertising()

def request(_cookies):
    headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98)'}
    payload = {'t': 'F' + str(int(time.time() * 1000))}
    cookies = {}
    for s_cookie in _cookies:
        cookies[s_cookie['name']] = s_cookie['value']

    response = requests.get('http://www.neobux.com/adalert/g/', headers=headers, params=payload, cookies=cookies)
    #print(response.content)
    part = response.content.replace('\'', '').replace('[',' ').replace(']',' ').replace(',',' ')
    list_var = part.split()
    return list_var

def run(_ptc, _user, _pass):
    driver = webdriver.Firefox()
    driver.get(neobux)                                              # Entra a la pagina
    textbox_user = driver.find_element_by_id('Kf1')                 # Nombre de Usuario, completamos datos
    textbox_user.send_keys(_user)
    textbox_password = driver.find_element_by_id('Kf2')             # Password
    textbox_password.send_keys(_pass)
    driver.find_element_by_link_text('enviar').click()
    time.sleep(1)                                                   # Esperamos x segundos

    _cookies = driver.get_cookies()                                 # Cookies =)
    driver.close()

    # +-------------------------------------------------------------------
    print('[-] start!')
    while True:
        list_var = request(_cookies)                                # Peticion get
        if list_var[0] == '1':

            print('[-] $ ' + list_var[8])
            print('[-] Fixed Advertisements: ' + list_var[1])
            print('[-] Micro Exposure: ' + list_var[5])
            print('[-] Fixed Advertisements: ' + list_var[2])
            print('[-] Total Ads: ' + list_var[18])

            if int(list_var[1]) > 0 or int(list_var[5]) > 0 or int(list_var[2]) > 0:
                print('[-] ---')
                detect_ads(_cookies)
            else:
                seconds = random.randrange(start=20, stop=60)
                print('[!] no ads, recheck in ' + str(seconds) + ' seconds')
                time.sleep(seconds)
        else:
            print('[!] error sesion')
            time.sleep(random.randrange(start=300, stop=600))
            run(_ptc,_user,_pass)

# +-----------------------------------------------------------------------

def banner():
    print ('''
               __  .__                 __________  __
______ ___.___/  |_|  |__   ____   ____\______   _/  |_  ____
\____ <   |  \   __|  |  \ /  _ \ /    \|     ___\   ___/ ___\.
|  |_> \___  ||  | |   Y  (  <_> |   |  |    |    |  | \  \___
|   __// ____||__| |___|  /\____/|___|  |____|    |__|  \___  >
|__|   \/               \/            \/        bot for ptc \/

Version     :   %s
Author      :   %s ''' %(__version__,__author__))
    print('')
    return

def main(argv):
    parser = argparse.ArgumentParser(description=banner())
    parser.add_argument('-ptc', '--ptc', dest='ptc', metavar='ptc', required=True,
                        help='[required] ' + 'ptc name ' + '(neobux)')
    parser.add_argument("-u", '--user', dest='user', metavar='user', required=True,
                        help='[required] ' + 'user')
    parser.add_argument("-p", '--password', dest='password', metavar='pass', required=True,
                        help='[required] ' + 'password')

    args = parser.parse_args()
    _ptc = args.ptc
    _user = args.user
    _pass = args.password

    run(_ptc, _user, _pass)

def _exit(signum, frame):
    sys.exit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, _exit)
    main(sys.argv)
