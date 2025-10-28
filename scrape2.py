import requests
from bs4 import BeautifulSoup
import json

# 1. 目標網址 (Travel 分類)
url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

# 2. 發送請求並解析 HTML
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

# 3. 找出所有書籍區塊
books = soup.find_all("article", class_="product_pod")

data = []  # 用來存放每本書的資料

# 4. 逐一擷取書名、價格、評分
for book in books:
    # 書名 title 屬性在 <h3><a title=...>
    title = book.h3.a.get("title")

    # 價格位於 <p class="price_color">
    price = book.find("p", class_="price_color").text.strip()

    # 評分在 <p class="star-rating"> 的 class 屬性中
    rating_tag = book.find("p", class_="star-rating")
    rating = rating_tag.get("class")[1] if rating_tag and len(rating_tag.get("class")) > 1 else "None"

    # 整理成字典
    book_info = {
        "title": title,
        "price": price,
        "rating": rating
    }

    data.append(book_info)

# 5. 印出整個清單 (JSON 格式)
print(json.dumps(data, indent=4))
