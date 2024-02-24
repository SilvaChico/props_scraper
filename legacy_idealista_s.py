import csv
import time
from bs4 import BeautifulSoup
import requests

print("-" * 10 + "Beggining" + "-" * 10)
# start new session to persist data between requests
session = requests.Session()

headers = {
    'authority': 'www.idealista.pt',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-ch-device-memory': '8',
    'sec-ch-ua': '"Chromium";v="121", "Not A(Brand";v="99"',
    'sec-ch-ua-arch': '"arm"',
    'sec-ch-ua-full-version-list': '"Chromium";v="121.0.6167.160", "Not A(Brand";v="99.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}


def get_page(page, headers):
    req = session.get(
        "https://www.idealista.pt/comprar-casas/lisboa/pagina-"
        + str(page),
        headers=headers,
    )
    print(req)
    html_text = req.text
    return BeautifulSoup(html_text, "html.parser")


page = 1
soup = get_page(page, headers)

print(soup.prettify())

h1_container = soup.find("h1", id="h1-container")
print("h1_container: " + str(h1_container))
if h1_container is not None:
    max_property_number = int(h1_container.text.split()[0].replace(".", ""))
else:
    print("No h1 element with id 'h1-container' found")
    max_property_number = 0  # or some other default value

print("max_property_number: " + str(max_property_number))
property_number = 1

header = ["title", "price", "area", "type", "desc"]

with open("lisboa.csv", "w", encoding="UTF8") as f:
    writer = csv.writer(f)
    writer.writerow(["number of props:", max_property_number])
    # write the header
    writer.writerow(header)

    while property_number <= max_property_number:
        print("\n\n page num" + str(page) + "\n")
        containers = soup.find_all("div", class_="item-info-container")
        for container in containers:
            title = container.find("a", class_="item-link").text
            price = container.find("span", class_="item-price h2-simulated").text
            item_details = container.find_all("span", class_="item-detail")
            print(str(property_number))
            property_number += 1
            if len(item_details) >= 1:
                area = item_details[0].text
                type = "no type" if len(item_details) == 1 else item_details[1].text
                if container.find("p", class_="ellipsis") != None:
                    desc = container.find("p", class_="ellipsis").text.strip()
                else:
                    desc = "no desc"
                # write the data
                writer.writerow([title, price, area, type, desc])
            else:
                print(title)
        page += 1
        time.sleep(1.0)
        soup = get_page(page, headers)
