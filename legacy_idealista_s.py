import csv
import time
from bs4 import BeautifulSoup
import requests

print("-" * 10 + "Beggining" + "-" * 10)
# start new session to persist data between requests
session = requests.Session()

def sanitize(data):
    return data.replace('"', '""').replace('\n', ' ').replace('\r', ' ')

headers = {
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'sec-ch-device-memory': '8',
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
        print("property_number: " + str(property_number) +"/"+str(max_property_number) + "\n")
        containers = soup.find_all("div", class_="item-info-container")
        for container in containers:
            title = container.find("a", class_="item-link").text
            price = container.find("span", class_="item-price h2-simulated").text
            item_details = container.find_all("span", class_="item-detail")
            property_number += 1
            if len(item_details) >= 1:
                area = item_details[0].text
                type = "no type" if len(item_details) == 1 else item_details[1].text
                if container.find("p", class_="ellipsis") != None:
                    desc = container.find("p", class_="ellipsis").text.strip()
                else:
                    desc = "no desc"
                # write the data
                writer.writerow([sanitize(title), sanitize(price), sanitize(area), sanitize(type), sanitize(desc)])
            else:
                print(title)
        page += 1
        time.sleep(0.01)
        soup = get_page(page, headers)
