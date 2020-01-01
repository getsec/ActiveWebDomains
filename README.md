# MyWebDomains
> Checks to see what web domains are associated with a DNS scan.

## Requirements
- git
- python3
- requirements.txt


## Install instructions
1. Create a venv.
```sh
python -m venv venv
source venv/bin/activate
```

2. Install requirements
```sh
pip install -r requirements.txt
```

3. Run the tool
```sh
python main.py domain.com
```

## Examples

Example basic usage
[![asciicast](https://asciinema.org/a/Brfh98CUORaPhLJvcCYCfGy5N.svg)](https://asciinema.org/a/Brfh98CUORaPhLJvcCYCfGy5N)

Example re-usage
[![asciicast](https://asciinema.org/a/eanVwvjQd4qna8oy3gQCRzAMk.svg)](https://asciinema.org/a/eanVwvjQd4qna8oy3gQCRzAMk)

Example with something a little bigger.
[![asciicast](https://asciinema.org/a/4VHm0yJ4reRgoQeqa96mDeGYb.svg)](https://asciinema.org/a/4VHm0yJ4reRgoQeqa96mDeGYb)

## Gotchas
1. If the host uses cloudflare domain protection, I've noticed that DNS resolver will resolve every single domain name you request. So, careful with that.