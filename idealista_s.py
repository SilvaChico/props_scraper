import csv
import time
from bs4 import BeautifulSoup
import requests

print("-" * 10 + "Beggining" + "-" * 10)
# start new session to persist data between requests
session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-GPC": "1",
    "Cache-Control": "max-age=0",
    "Cookie": "userUUID=d5aad8e3-9f05-4034-92d7-1dd16e0d5e3e; xtvrn=$410875$; xtan410875=1-444370859; xtant410875=1; xtide=%5B%5D; cookieDirectiveClosed=true; uc=\"OTflZbpgQBH/UrTL+SP6KTeHvbHoAD/Oi74cFIg+4L+z7RPxB2jL2OmzqvZc2K2infhuJhjErtaE4ANxlk652ntB9OD8E2oYxy0kwq1uGV5tO+RAlfcbXZWdPsD+dhiKxOO7Q5Cbyak = \"; nl=AlL2z/KnYroc8+Cgmmimr4WyPQdFR1IzNV54DARZsjtpceuGLJOhL8L40RnHUov80rkOul41Q3Pb0GRRfsVzAAyKyfdRwfNXEjVBxzsAOzvs06iKiw+6OyXk1QgDaK5D; cc=eyJhbGciOiJIUzI1NiJ9.eyJjdCI6NDM1OTI2LCJleHAiOjE2NDMzOTMwOTN9.MnQac0kGGBmtmwaFuFQFd_5NLKFcElJOnm9cng-gtdo; IQ_userIdCookie=PT00444370859; datadome=YuW2LOLngYvWt7imO301kcAhAVcnJdCwfnmxcD5asJ~a3.YZ5fe6RlxR0YqXcI~s2-pHeBvt0UanpA4Z3iyS9.iIb_MR0K~G06IY3-pn4aFFBV1_W6dix9PE8MmyrFW; didomi_token=eyJ1c2VyX2lkIjoiMTc5ZTVkMjgtNmE2NS02YjFkLTkyZWMtZjQ5MzA2MjQ1Yjk3IiwiY3JlYXRlZCI6IjIwMjEtMDYtMDdUMDk6MzQ6MTUuMDgxWiIsInVwZGF0ZWQiOiIyMDIxLTA2LTA3VDA5OjM0OjE1LjA4MVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiZmFjZWJvb2siLCJjOm1peHBhbmVsIiwiYzphYnRhc3R5LUxMa0VDQ2o4IiwiYzpob3RqYXIiLCJjOmJlYW1lci1IN3RyN0hpeCIsImM6dGVhbGl1bWNvLURWRENkOFpQIiwiYzpjaGFyYmVhdC1aNFFrOENhaCIsImM6aWRlYWxpc3RhLTdHbnQ2NHpGIiwiYzppZGVhbGlzdGEtV1UzQ0duNEMiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiYW5hbHl0aWNzLUhwQkpycks3IiwiZ2VvbG9jYXRpb25fZGF0YSJdfSwidmVyc2lvbiI6Mn0=; euconsent-v2=CPHaxDnPHaxDnAHABBENBcCoAP_AAAAAAB6YF5wAwAWgBbAXmAAAAgNApACsAFwAQwAyABlgDUAGyAOwAfgBAACCgEYAKWAU8Aq8BaAFpANYAbwA6oB8gENgIdARUAi8BIgCbAE7AKRAXIAwIBhIDDwGMAMnAZyAzwBnwDkgHKAOsAfgSgegAIAAWABQADIAHAARQAwADEAHgARAAmABVAC4AF8AMQAZgA2gCEAENAIgAiQBHACjAFKALcAYQAygBqgDZAHeAPwAjABHACngFXgLQAtIBdQDFAG4AOoAfIBDoCKgEXgJEATYAsUBbAC7QF5gMPAZEAycBlgDOQGeAM-AaQA1gBwADrAHagPwKQVAAFwAUABUADIAHIAPgBAACKAGAAZQA0ADUAHkAQwBFACYAE8AKQAVQAsABcAC-AGIAMwAcwBCACGgEQARIAowBSgCxAFuAMIAZQA0QBqgDZAHfAPsA_QCLAEYAI4ASkAoIBQwCrgFbALmAXkAxQBtADcAHoAQ6Ai8BIgCTgE2AJ2AUOArYBYoC0AFsALgAXIAu0BeYDDQGHgMYAZEAyQBk4DLgGcgM8AZ9A0gDSYGsAayA2MBusDkwOUAcuA6wB2oDxwHygPwIQRAAFgAUAAyACIAFwAMQAhgBMACqAFwAL4AYgAzABvAD0AI4AWIAwgBlADUAG-AO-AfYB-AD_AIwARwAlIBQQChgFPAKvAWgBaQC5gF-AMUAbQA6gB6AEggJEAScAlQBNgCmgFigLRgWwBbQC4AFyALtAYeAxIBkQDJwGcgM8AZ8A0QBpIDSwGqgOAAckA6MB1gDtQHjgPwHQdgAFwAUABUADIAHIAPgBAACIAF0AMAAygBoAGoAPAAfQBDAEUAJgAT4AqgCsAFiALgAugBfADEAGYAN4AcwA9ACEAENAIgAiQBHQCWAJgATQAowBSgCxAFvAMIAwwBkADKAGiANQAbIA3wB3gD2gH2AfoA_wCBwEWARgAjkBKQEqAKCAU8Aq4BYoC0ALSAXMAuoBeQC_AGKANoAbgA4kB0wHUAPQAhsBDoCIgEVAIvASCAkQBKgCZAE2AJ2AUOApoBVgCxQFoQLYAtkBcAC5AF2gLvAXmAwYBhIDDQGHgMSAYwAx4BkgDJwGVAMsAZcAzkBnwDRIGkAaSA0sBpwDVQGsANjAbqA4uByQHKgOXAdGA6wB44D0gHqgPlAfWA_AJBfAAQAAuACgAKgAZAA5AB4AIAARAAwABlADQANQAeQBDAEUAJgAT4AqgCsAFgALgAbwA5gB6AEIAIaARABEgCOgEsAS4AmgBSgC3AGGAMgAZcA1ADVAGyAO8AewA-IB9gH6AQAAgcBFwEYAI0ARwAlIBQQClgFPAKuAXMAvwBigDWAG0ANwAbwA4gB6AD5AIbAQ6Ai8BIgCYgEygJsATsAocBSICmgFigLQAWwAuQBd4C8wGBAMGAYSAw0Bh4DIgGSAMnAZcAzkBnwDSAGnQNYA1kBusDkQOVAcuA6MB1gDxwHyjID4AFAAhgBMAC4AI4AZYA1AB2QD7APwAjABHAClgFXAK2AbwBJwCYgE2ALRAWwAvMBgQDDwGRAM5AZ4Az4ByQDlAHxAPwFQIAAKABDACYAFwARwAywBqADsAH4ARgAjgBSwCrwFoAWkA3gCQQExAJsAU2AtgBcgC8wGBAMPAZEAzkBngDPgG5AOSAcoA_AAAA.f_gAAAAAAAAA; smc=\"{}\"; utag_main=v_id:017e9bc4ad57001b8b39621fe6b600052001900f00ac2; SESSION=15a353ca7aab3446~fd39cb5b-fe5c-40a9-9472-49b02aa171a3; cookieSearch-1=\"/comprar-terrenos/lisboa/azambuja/azambuja/: 1643298252103\"; contactf6f995b1-1464-47a0-892c-e99c43052a27=\"{'email': 'Bp7OXUFVgKLw00vABVEcjNIDpb7jl6+8MR4dzC+rmMw=', 'phone': '916698439', 'phonePrefix': null, 'friendEmails': null, 'name': 'Bp7OXUFVgKLw00vABVEcjPcZq0WXbInn', 'message': null, 'message2Friends': null, 'maxNumberContactsAllow': 10, 'defaultMessage': true}",
}


def get_page(page, headers):
    req = session.get(
        "https://www.idealista.pt/comprar-terrenos/lisboa/azambuja/azambuja/pagina-"
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
    max_property_number = int(h1_container.text.split()[0])
else:
    print("No h1 element with id 'h1-container' found")
    max_property_number = 0  # or some other default value

print("max_property_number: " + str(max_property_number))
property_number = 1

header = ["title", "price", "area", "type", "desc"]

with open("buja.csv", "w", encoding="UTF8") as f:
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
