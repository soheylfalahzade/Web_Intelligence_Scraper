import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_ecommerce():
    print("🛒 در حال استخراج داده‌های محصولات فروشگاهی...")
    
    # سایت مرجع برای تست اسکرپینگ فروشگاهی
    url = "http://books.toscrape.com/"
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # پیدا کردن تمام کارت‌های محصولات
        products = soup.find_all("article", class_="product_pod")
        results = []

        for item in products:
            # استخراج نام محصول (از تگ a داخل h3)
            title = item.h3.a["title"]
            
            # استخراج قیمت
            price = item.find("p", class_="price_color").text
            
            # استخراج وضعیت موجودی
            stock = item.find("p", class_="instock availability").text.strip()
            
            results.append({
                "نام محصول": title,
                "قیمت": price,
                "وضعیت موجودی": stock,
                "زمان استخراج": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"✅ استخراج شد: {title[:30]}...")

        if results:
            df = pd.DataFrame(results)
            file_name = "Ecommerce_Products_Report.xlsx"
            df.to_excel(file_name, index=False, engine='openpyxl')
            print(f"\n✨ ماموریت موفق! اطلاعات {len(results)} محصول استخراج و در فایل {file_name} ذخیره شد.")
        else:
            print("\n⚠️ هیچ داده‌ای پیدا نشد.")

    except Exception as e:
        print(f"خطا در ارتباط با سرور: {e}")

if __name__ == "__main__":
    scrape_ecommerce()