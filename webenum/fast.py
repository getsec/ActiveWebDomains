
import requests
import tqdm
from concurrent.futures import ThreadPoolExecutor

def web_scan_results(output_files, TIMEOUT_FLOAT):
    
    with open(output_files) as f:
        urls = [line.rstrip() for line in f]

    def get_url(url):
        try:    
            full_address = f"https://{url}"
            r = requests.get(full_address, timeout=TIMEOUT_FLOAT)
            return {"url": url, "status_code": r.status_code}
        except requests.exceptions.ConnectionError:
            pass


    with ThreadPoolExecutor(max_workers=50) as pool:
        output = list(pool.map(get_url,urls))
        return output
        
    
