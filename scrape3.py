import requests
from bs4 import BeautifulSoup
import json

url = "https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    # 🎯 抓排行榜主要書籍項目
    books = soup.select("div.mod_a li.item, div.mod_b li.item, li.top_item")
    result = []

    for idx, book in enumerate(books[:20], start=1):
        try:
            # 🟩 書名
            title_tag = book.select_one("h4 a")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"

            # 🟦 價格區塊（折扣與實際價）
            price_block = book.select_one("li.price_a")

            if price_block:
                # 折扣 (例如 "79")
                discount_tag = price_block.select_one("strong b")
                discount = discount_tag.get_text(strip=True) if discount_tag else "N/A"

                # 實際價格（最後一個 <b> 是價格）
                all_b_tags = price_block.select("b")
                if len(all_b_tags) >= 2:
                    real_price = all_b_tags[-1].get_text(strip=True)
                else:
                    real_price = "N/A"

                price = f"{discount}折 NT${real_price}"
            else:
                price = "N/A"

            result.append({
                "rank": str(idx),
                "title": title,
                "price": price
            })

        except Exception as e:
            print(f"⚠️ 第 {idx} 本書解析失敗：{e}")
            continue

    print(json.dumps(result, indent=4, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    print(f"❌ 無法取得網頁：{e}")
except Exception as e:
    print(f"❌ 發生未知錯誤：{e}")
