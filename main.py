import requests
from huepy import *
from os import system
from os import path
from sys import argv
from sys import exit
TIMEOUT_FLOAT = 10.0

def install_sublister(git_url, folder):
    try:
        system(f"git clone {git_url}")
        system(f"pip install -r {folder}/requirements.txt")
    except Exception:
        print("Could not download sublister - ensure git is installed.")


def execute_sublister(domain_scan_cmd):
    system(domain_scan_cmd.format(domain, output_file))


def web_scan_results(output_file):
    with open(output_file) as fp:
        line = fp.readlines()
    for i in line:
        url = i.strip("\n")
        try:
            r = requests.get(f"https://{url}", timeout=TIMEOUT_FLOAT)
            if r.ok:
                msg = f"{url} - found {r.status_code} "
                print(good(msg))
            else:
                msg = f"{url} - found {r.status_code}"
                print(info(msg))
        except requests.exceptions.ConnectionError:
            pass 
        except requests.exceptions.ReadTimeout:
            print(bad(f"{url} - Response took too long {TIMEOUT_FLOAT}s"))

        
   
if __name__ in "__main__":
    try:
        domain = argv[1]
    except Exception:
        print(bad(bold(red(f"USE: python {argv[0]} example.com"))))
        exit()
    git_url = "https://github.com/aboul3la/Sublist3r.git"
    folder = git_url.split('/')[-1].split('.')[0]
    output_file = f"outputs/{domain}-output.txt"
    domain_scan_cmd = f"python {folder}/sublist3r.py -n -d {domain} -o {output_file} > /dev/null "
    
    # If Sublister is already downloaded move on. 
    if path.isdir(folder):
        
        # If there is already a sub enum scan
        # ask the user if they want to re-scan...
        if path.isfile(f"{output_file}"):
            print(que(f"There is already an active output file: {output_file}"))
            question = input(que("Shall we re-scan for new domains? [y/n]"))
            
            # if no - just rescan old output
            if question.lower() == "n":
                web_scan_results(output_file)
            
            # if yes - redo the whole enum
            elif question.lower() == "y":
                execute_sublister(domain_scan_cmd)
                web_scan_results(output_file)
        
        # if there is no output files
        # go ahead and just scan like normal.
        else:
            execute_sublister(domain_scan_cmd)
            web_scan_results(output_file)
    # If sublister isn't installed use git.
    else:
        install_sublister(git_url, folder)
