import requests
import re

# 1. 目標網址 (Travel 分類頁面)
url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

# 2. 發送 GET 請求並取得 HTML 原始碼
response = requests.get(url)
html = response.text

# 3. 撰寫正則表達式匹配價格 (£xx.xx)
pattern = r"£\d+\.\d{2}"

# 4. 使用 re.findall 找出所有符合價格格式的字串
prices = re.findall(pattern, html)

# 5. 印出結果 (Python List 格式)
print(prices)
