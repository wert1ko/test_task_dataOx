from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import time

from scrappers.auto_ria_scrapper import AutoRiaScrapper

def parse_target_time(scraping_time: str) -> datetime:
    now = datetime.now()
    target_time = datetime.strptime(scraping_time, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )
    return target_time

def start_daily_scrapper(url, num_threads, scraping_time):

    while True:
        now = datetime.now()
        target_time = parse_target_time(scraping_time)

        if now >= target_time:
            # Якщо вже пройшов час запуску запускаємо одразу
            print(f"[{now}] Запуск скрапінгу")
            scraper = AutoRiaScrapper(url, num_threads)
            scraper.run()
            next_run = target_time + timedelta(days=1)
        else:
            # Якщо ще не прийшов час — очікуємо
            next_run = target_time

        sleep_seconds = (next_run - datetime.now()).total_seconds()
        print(f"[{datetime.now()}] Очікування до {next_run}")
        time.sleep(max(1, sleep_seconds))

if __name__ == "__main__":
    load_dotenv(override=True)
    BASE_URL = os.getenv("BASE_URL")
    NUM_WORKERS = int(os.getenv("NUM_THREADS_WORKERS"))
    SCRAPING_TIME = os.getenv("SCRAPING_TIME")
    start_daily_scrapper(BASE_URL, NUM_WORKERS, SCRAPING_TIME)
