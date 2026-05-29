import random
import string
from pathlib import Path

import requests

desktop = Path.home() / 'Desktop' / 'Pictures_From_IMGUR'
desktop.mkdir(parents=True, exist_ok=True)

session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0'
}

while True:
    image_id = ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(random.choice([5, 6]))
    )

    url = f'https://i.imgur.com/{image_id}.jpg'

    try:
        response = session.get(
            url,
            headers=headers,
            timeout=10,
            stream=True
        )

        if response.status_code != 200:
            print(f'[-] Invalid: {image_id}')
            continue

        content_type = response.headers.get('Content-Type', '')

        if 'image' not in content_type:
            print(f'[-] Not image: {image_id}')
            continue

        file_path = desktop / f'{image_id}.jpg'

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)

        print(f'[+] Valid: {url}')

    except requests.RequestException as error:
        print(f'[!] Error: {error}')