import requests
import pandas as pd
from datetime import datetime

def fetch_api_data():
    print("🚀 در حال استخراج داده‌های محصولات از API سرور...")
    
    # یک API استاندارد فروشگاهی که در ایران هم کار می‌کند
    url = "https://fakestoreapi.com/products"
    
    try:
        # verify=False برای دور زدن برخی مشکلات SSL اینترنت ایران
        response = requests.get(url, timeout=15, verify=False)
        response.raise_for_status() # بررسی ارورهای HTTP
        
        # تبدیل مستقیم داده‌های JSON به دیکشنری پایتون
        products = response.json()
        results = []

        for item in products:
            results.append({
                "شناسه محصول": item['id'],
                "نام محصول": item['title'],
                "دسته بندی": item['category'],
                "قیمت (دلار)": item['price'],
                "امتیاز کاربران": item['rating']['rate'],
                "زمان استخراج": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"✅ محصول دریافت شد: {item['title'][:25]}...")

        # ساخت فایل اکسل
        if results:
            df = pd.DataFrame(results)
            file_name = "API_Products_Report.xlsx"
            df.to_excel(file_name, index=False, engine='openpyxl')
            print(f"\n✨ موفقیت! {len(results)} محصول استخراج و در فایل {file_name} ذخیره شد.")

    except Exception as e:
        print(f"❌ خطا در اجرا: {e}")

if __name__ == "__main__":
    fetch_api_data()