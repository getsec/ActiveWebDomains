from os import system
from requests import exceptions
from requests import exceptions 
from requests import get
from tqdm import tqdm
from bs4 import BeautifulSoup  # NOQA

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15"  # NOQA

def install_sublister(git_url, sublister_folder):
    system(f"git clone {git_url}")
    system(f"pip install -r {sublister_folder}/requirements.txt")


def execute_sublister(domain_scan_cmd):
    system(domain_scan_cmd)


def web_scan_results(output_file, TIMEOUT_FLOAT):
    http = []
    soup = []
    with open(output_file) as fp:
        line = fp.readlines()
    for i in tqdm(line):
        url = i.strip("\n")
        try:
            address = f"https://{url}"
            r = get(address, timeout=TIMEOUT_FLOAT, headers={'User-Agent': UA})
            soup = BeautifulSoup(r.text, features="html.parser")
            try:
                http.append({
                        'url': url, 
                        'status_code': r.status_code, 
                        'soup': soup.title.string
                    })
            except AttributeError:
                http.append({
                        'url': url, 
                        'status_code': r.status_code, 
                        'soup': None
                    })


        except exceptions.ReadTimeout:
            pass
        except exceptions.ConnectionError:
            pass

    return http


