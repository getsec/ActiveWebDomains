import requests
from huepy import *
from os import system
from os import path
from sys import argv
from sys import exit

from webenum.help import install_sublister
from webenum.help import execute_sublister
from webenum.fast import web_scan_results

# How long do we want to wait for requests
# This is represented in seconds.
TIMEOUT_FLOAT = 10.0


def pretty_print_parsed_results(output):
    for i in output:
        if i is not None:
            if i['status_code'] in range(0,399):
                print(good(f"{i['status_code']} @ {i['url']}"))
            elif i['status_code'] in range(400,499):
                print(info(f"{i['status_code']} @ {i['url']}"))
            elif i['status_code'] in range(500,599):
                print(bad(f"{i['status_code']} @ {i['url']}"))


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
            question = input(que("Shall we re-scan for new domains? [y/n]: "))
            
            # if no - just rescan old output
            if question.lower() == "n":
                output = web_scan_results(output_file, TIMEOUT_FLOAT)
                pretty_print_parsed_results(output)
            # if yes - redo the whole enum
            elif question.lower() == "y":
                print(info("Currently Looking for domains - This may take some time"))
                execute_sublister(domain_scan_cmd)
                output = web_scan_results(output_file, TIMEOUT_FLOAT)
                pretty_print_parsed_results(output)
        # if there is no output files
        # go ahead and just scan like normal.
        else:
            print(info("Currently Looking for domains - This may take some time"))
            execute_sublister(domain_scan_cmd)
            output = web_scan_results(output_file, TIMEOUT_FLOAT)
            pretty_print_parsed_results(output)
    # If sublister isn't installed use git.
    else:
        install_sublister(git_url, sublister_folder)
