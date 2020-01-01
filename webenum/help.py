from os import system
from requests import exceptions
from requests import exceptions 
from requests import get
from tqdm import tqdm

import asyncio
from aiohttp import ClientSession

def install_sublister(git_url, sublister_folder):
    system(f"git clone {git_url}")
    system(f"pip install -r {sublister_folder}/requirements.txt")


def execute_sublister(domain_scan_cmd):
    system(domain_scan_cmd)


def web_scan_results(output_file, TIMEOUT_FLOAT):
    http_200 = []
    http_non200 = []
    http_timeout = []
    http_err = []
    with open(output_file) as fp:
        line = fp.readlines()
    for i in tqdm(line):
        url = i.strip("\n")
        try:
            r = get(f"https://{url}", timeout=TIMEOUT_FLOAT)
            if r.ok:
                http_200.append({'url':url, 'status_code':r.status_code})
            else:
                http_non200.append({'url':url, 'status_code':r.status_code})
        except exceptions.ReadTimeout:
            http_timeout.append({'url':url, 'status_code':'na'})
        except exceptions.ConnectionError:
            http_err.append(url)
            pass

    return http_200, http_non200, http_timeout, http_err


def fetch(session, csv):
    base_url = "https://people.sc.fsu.edu/~jburkardt/data/csv/"
    with session.get(base_url + csv) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(url))
        # Return .csv data for future consumption
        return data