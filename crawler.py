import requests
import time
import csv
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com/"
r = requests.get(url)

print(r.status_code)
#print(r.encoding)
#print(r.text[:500])

#把格言變成一個list of dictionary
def parse_quotes(soup):
    #soup = BeautifulSoup(html, "html.parser")
    results = []

    #selected = soup.select("div.quote")
    #print(selected)

    for q in soup.select("div.quote"):
        text = q.select_one("span.text").get_text(strip=True)
        author = q.select_one("small.author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in q.select("a.tag")]
        results.append({"text": text, "author": author, "tags": tags})

    return results

quotes = parse_quotes(r.text)
#print(len(quotes))
#print(quotes[0])

all_quotes = []
#for page in range(1, 4):
#    url = f"https://quotes.toscrape.com/page/{page}/"
#    try:
#        r = requests.get(url)
#       r.raise_for_status()
#  except requests.RequestException as e:
#     print(f"第{page}頁失敗: {e}")
#        continue
#    all_quotes.extend(parse_quotes(r.text))
#    time.sleep(1)  # 增加延遲以避免過於頻繁的請求

#print(len(all_quotes))

BASE = "https://quotes.toscrape.com/"
url = BASE +"/"

while True:
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"抓取失敗: {e}")
        continue

    soup = BeautifulSoup(r.text, "html.parser")
    all_quotes.extend(parse_quotes(soup))
    print(f"已抓取 {len(all_quotes)} 則")

    next_btn = soup.select_one("li.text a")
    if next_btn is None:
        break
    url = BASE + next_btn["href"]
    time.sleep(1)  # 增加延遲以避免過於頻繁的請求


with open("quote.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
    writer.writeheader()
    writer.writerows(all_quotes)

#print(f"完成!! {len(all_quotes)} 則!")