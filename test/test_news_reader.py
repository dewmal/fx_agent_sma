from bs4 import BeautifulSoup
from requests_html import HTMLSession

session = HTMLSession()
home = "https://www.bloomberg.com"
r = session.get(home)
soup = BeautifulSoup(r.content)

links = soup.find_all('a')

for link in links:
    print(link.text)

    link_href = link.get("href")
    if link_href.startswith("/"):
        link_href = f"{home}{link_href}"
    print(link_href)


import torch
x = torch.rand(5, 3)
print(x)