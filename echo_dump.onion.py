import os
import sys
import time
import requests
import argparse
import random
import json

from headers.agents import Headers
from banner.banner import Banner


class Colors:
    # Console colors
    W = '\033[0m'  # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[34m'  # blue
    P = '\033[35m'  # purple
    C = '\033[36m'  # cyan
    GR = '\033[37m'  # gray
    BOLD = '\033[1m'
    END = '\033[0m'


class Configuration:
    ECHODUMP_ERROR_CODE_STANDARD = -1
    ECHODUMP_SUCCESS_CODE_STANDARD = 0

    ECHODUMP_MIN_DATA_RETRIEVE_LENGTH = 1
    ECHODUMP_RUNNING = False
    ECHODUMP_OS_UNIX_LINUX = False
    ECHODUMP_OS_WIN32_64 = False
    ECHODUMP_OS_DARWIN = False

    ECHODUMP_REQUESTS_SUCCESS_CODE = 200

    __ECHODUMP_api__ = "https://darksearch.io/api/search"


class Platform(object):
    def __init__(self, execpltf):
        self.execpltf = execpltf

    def get_operating_system_descriptor(self):
        cfg = Configuration()
        clr = Colors()

        if self.execpltf:
            if sys.platform == "linux" or sys.platform == "linux2":
                cfg.ECHODUMP_OS_UNIX_LINUX = True
                print(clr.BOLD + clr.W + "OS: " +
                      clr.G + sys.platform + clr.END)
            if sys.platform == "win64" or sys.platform == "win32":
                cfg.ECHODUMP_OS_WIN32_64 = True
                print(clr.BOLD + clr.W + "OS: " +
                      clr.G + sys.platform + clr.END)
            if sys.platform == "darwin":
                cfg.ECHODUMP_OS_DARWIN = True
                print(clr.BOLD + clr.W + "OS: " +
                      clr.G + sys.platform + clr.END)
        else:
            pass

    def clean_screen(self):
        if self.execpltf:
            if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
                os.system('clear')
            else:
                os.system('cls')
        else:
            pass


class ECHODUMP(object):
    def __init__(self, api, query):
        self.api = api
        self.query = query

    def crawl_api(self):
        hdrs = Headers()
        clr = Colors()
        cfg = Configuration()

        try:
            darksearch_url_response = requests.get(self.api, params=self.query)
            json_data = darksearch_url_response.json()
            #json_dump = json.dumps(json_data, indent=2)
            darksearch_url_response.headers["User-Agent"] = random.choice(
                hdrs.useragent)
        except requests.RequestException as re:
            print(clr.BOLD + clr.R + str(re) + clr.END)

        try:
            if json_data["total"] >= cfg.ECHODUMP_MIN_DATA_RETRIEVE_LENGTH:  # data >= 1
                for key in range(0, 18):
                    site_title = json_data['data'][key]['title']
                    site_onion_link = json_data['data'][key]['link']
                    print(
                        clr.BOLD + clr.G + f"[+] Тайтл: {site_title}\n\t> Onion Link: {clr.R}{site_onion_link}\n" + clr.END)
        except IndexError:
            print(clr.BOLD + clr.R +
                  f"[-] Результаты по запросу не найдены: {self.query}\n" + clr.END)


def ECHODUMP_main():
    cfg = Configuration()
    clr = Colors()
    bn = Banner()

    Platform(True).clean_screen()
    Platform(True).get_operating_system_descriptor()
    bn.LoadECHODUMPBanner()
    time.sleep(1.5)

    parser = argparse.ArgumentParser()
    parser.add_argument("-v",
                        "--version",
                        help="returns ECHODUMP's version",
                        action="store_true")
    parser.add_argument("-q",
                        "--query",
                        help="поиск по ключевому слову или строке",
                        type=str,
                        required=True)
    parser.add_argument("-p",
                        "--page",
                        help="номер страницы для фильтрации результатов, возвращаемых из поиска (по умолчанию=1).",
                        type=int)

    args = parser.parse_args()

    if args.version:
        print(clr.BOLD + clr.B +
              f"ECHODUMP Version: {__version__}\n" + clr.END)

    elif args.query:
        if args.page:
            query = {
                'query': args.query,
                'page': args.page
            }
            print(clr.BOLD + clr.B +
                  f"Поиск: {args.query} на странице: {args.page}...\n" + clr.END)
            ECHODUMP(cfg.__ECHODUMP_api__, query).crawl_api()
            cfg.ECHODUMP_RUNNING = True
        else:
            query = {
                'query': args.query,
                'page': 1
            }
            print(clr.BOLD + clr.B +
                  f"Поиск: {args.query} на странице: 1...\n" + clr.END)
            ECHODUMP(cfg.__ECHODUMP_api__, query).crawl_api()
            cfg.ECHODUMP_RUNNING = True


if __name__ == "__main__":
    ECHODUMP_main()
