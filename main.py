import argparse
import json
from huepy import *
from os import system
from os import path
from sys import argv
from sys import exit

from webenum.help import install_sublister
from webenum.help import execute_sublister
from webenum.fast import web_scan_results

parser = argparse.ArgumentParser()
parser.add_argument("domain", help="The domain which you would like to enumerate", type=str)
parser.add_argument("--report", help="This switch creates a JSON dump of the output in the reports folder",  action="store_true")
args = parser.parse_args()

# How long do we want to wait for requests
# This is represented in seconds.
TIMEOUT_FLOAT = 10.0
SUBLISTER_DIR = "Sublist3r"


def write_output_to_file(output):
    out_path = f"reports/domain-results.json"
    with open(out_path, 'w') as outfile:
        json.dump(output, outfile)


def pretty_print_parsed_results(output):
    if report is True:
        write_output_to_file(output)

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
        domain = args.domain

        if args.report:
            report = True
        else:
            report = False

    except Exception:
        print(bad(bold(red(f"USE: python {argv[0]} example.com"))))
        exit()
    
    output_file = f"outputs/{domain}-output.txt"
    
    
    # If Sublister is already downloaded move on. 
    if path.isdir(SUBLISTER_DIR):
        
        # If there is already a sub enum scan
        # ask the user if they want to re-scan...
        if path.isfile(output_file):
            question = input(que("Old Scan Found. Should we re-scan for new domains? [y/n]: "))
            
            # if no - just rescan old output
            if question.lower() == "n":
                output = web_scan_results(output_file, TIMEOUT_FLOAT)
            
            # if yes - redo the whole enum
            elif question.lower() == "y":
                execute_sublister(domain, output_file)
                output = web_scan_results(output_file, TIMEOUT_FLOAT)
            
            else:
                print(bad("Please use [y/n]..."))
            
            # Finally print the output:
            pretty_print_parsed_results(output)

        # if there is no output files associaed with the current domain
        else:
            execute_sublister(domain, output_file)
            output = web_scan_results(output_file, TIMEOUT_FLOAT)
            pretty_print_parsed_results(output)
    
    # If sublister isn't installed use git.
    else:
        install_sublister()
