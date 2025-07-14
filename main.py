import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from tqdm import tqdm

EMAIL = "test@email.com"  # ایمیل تستی
DOWNLOAD_DIR = os.path.abspath("downloads")

# اطمینان از وجود پوشه ذخیره
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# فایل‌هایی که قبلا دانلود شدند
downloaded_file = "downloaded.txt"
if os.path.exists(downloaded_file):
    with open(downloaded_file, "r", encoding="utf-8") as f:
        downloaded_links = set(line.strip() for line in f if line.strip())
else:
    downloaded_links = set()

# راه‌اندازی مرورگر با تنظیمات دانلود
options = uc.ChromeOptions()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
}
options.add_experimental_option("prefs", prefs)
driver = uc.Chrome(options=options)
driver.get("https://poweren.ir/electricity-books/")
time.sleep(5)

# استخراج همه لینک مقالات
article_elements = driver.find_elements(By.CSS_SELECTOR, "h2.entry-title > a")
article_links = [a.get_attribute("href") for a in article_elements]
print(f"🔗 {len(article_links)} مقاله یافت شد.")

# اجرای دانلود مقاله به مقاله
for idx, url in enumerate(tqdm(article_links, desc="دانلود مقالات")):
    if url in downloaded_links:
        continue  # رد شدن از مقاله‌های قبلاً دانلود شده

    try:
        print(f"\n📝 مقاله {idx+1}: {url}")
        driver.get(url)
        time.sleep(5)

        # کلیک روی دکمه دانلود
        download_btn = driver.find_element(By.PARTIAL_LINK_TEXT, "دانلود کتاب")
        download_btn.click()
        time.sleep(3)

        # پر کردن ایمیل
        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        email_input.clear()
        email_input.send_keys(EMAIL)
        time.sleep(1)

        # کلیک روی دکمه دریافت لینک
        submit_btn = driver.find_element(By.XPATH, "//button[contains(text(),'دریافت لینک دانلود')]")
        submit_btn.click()
        time.sleep(5)

        # یافتن و کلیک روی لینک نهایی
        final_link = driver.find_element(By.PARTIAL_LINK_TEXT, "اینجا کلیک کنید")
        final_link.click()
        print("✅ دانلود آغاز شد.")

        # افزودن به لیست دانلودشده
        with open(downloaded_file, "a", encoding="utf-8") as f:
            f.write(url + "\n")

        # صبر ۲ دقیقه
        print("⏳ صبر برای مقاله بعدی (۲ دقیقه)...")
        time.sleep(120)

    except Exception as e:
        print(f"⚠️ خطا در {url}: {e}")
        continue

driver.quit()
print("\n🎉 همه مقالات پردازش شدند.")
