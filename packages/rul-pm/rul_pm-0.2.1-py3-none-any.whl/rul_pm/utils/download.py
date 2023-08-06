from tqdm import tqdm
import requests
from pathlib import Path

def download_file(URL:str, output_path:Path):
    with requests.get(URL, stream=True) as r:
        r.raise_for_status()
        with open(output_path, 'wb') as f:
            pbar = tqdm(total=int(r.headers['Content-Length']))
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    pbar.update(len(chunk))