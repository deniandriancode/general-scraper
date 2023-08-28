import requests
from bs4 import BeautifulSoup
import json
import sys

az_animals = list()

def make_request(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "en-US,en", 
        "Host": "www.a-z-animals.com", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    session = requests.Session()
    response = session.get(url, headers=headers).content

    soup = BeautifulSoup(response, "html.parser")

    style_raw = soup.find("div", class_="entry-content").find("style").get_text()
    style_raw = style_raw.split("background-image: ")[-1].replace("\n", "").replace("\t", "").replace("\");}}", "").strip()

    image_url = style_raw.split("url(\"")[1]
    common_name = soup.find("h1").get_text().strip()
    latin_name = soup.find("p", class_="has-text-align-center text-white font-weight-bolder font-size-lg").get_text().strip()
    print(f"GET {common_name}")

    return {
        "image_url": image_url,
        "common_name": common_name,
        "latin_name": latin_name
    }


count = 0
with open("az_animals.json", "r") as fp:
    urls = json.load(fp)
    for url in urls:
        sys.stdout.write('\033[2K\033[1G')
        result = make_request(url)
        az_animals.append(result)
        count += 1

with open("az_animals_result.json", "w") as fp:
    json.dump(az_animals, fp)
    print(f"Finished scraped {count} animals!")
