import requests
from huepy import *
from os import system
from os import path
from sys import argv
from sys import exit

from webenum.help import install_sublister
from webenum.help import execute_sublister
from webenum.help import web_scan_results

# How long do we want to wait for requests
# This is represented in seconds.
TIMEOUT_FLOAT = 10.0


def parse_results(http):
    for i in http:
        print(good(f"{i['status_code']} @ {i['url']} \"{i['soup']}\""))



if __name__ in "__main__":
    try:
        domain = argv[1]
    except Exception:
        print(bad(bold(red(f"USE: python {argv[0]} example.com"))))
        exit()
    git_url = "https://github.com/aboul3la/Sublist3r.git"
    sublister_folder = git_url.split('/')[-1].split('.')[0]
    output_file = f"outputs/{domain}-output.txt"
    domain_scan_cmd = f"python {sublister_folder}/sublist3r.py -n -d {domain} -o {output_file} > /dev/null "
    
    # If Sublister is already downloaded move on. 
    if path.isdir(sublister_folder):
        
        # If there is already a sub enum scan
        # ask the user if they want to re-scan...
        if path.isfile(f"{output_file}"):
            print(que(f"There is already an active output file: {output_file}"))
            question = input(que("Shall we re-scan for new domains? [y/n]"))
            
            # if no - just rescan old output
            if question.lower() == "n":
                http = web_scan_results(output_file, TIMEOUT_FLOAT)
                parse_results(http)
            # if yes - redo the whole enum
            elif question.lower() == "y":
                print(info("Currently Looking for domains - This may take some time"))
                execute_sublister(domain_scan_cmd)
                http = web_scan_results(output_file, TIMEOUT_FLOAT)
                parse_results(http)
        
        # if there is no output files
        # go ahead and just scan like normal.
        else:
            print(info("Currently Looking for domains - This may take some time"))
            execute_sublister(domain_scan_cmd)
            http = web_scan_results(output_file, TIMEOUT_FLOAT)
            parse_results(http)
    
    # If sublister isn't installed use git.
    else:
        install_sublister(git_url, sublister_folder)
