from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import time
from database.dump_db import dump_database
from scrappers.auto_ria_scrapper import AutoRiaScrapper
from threading import Thread


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

def start_daily_dump(dump_time_str: str):
    while True:
        now = datetime.now()
        target_time = datetime.strptime(dump_time_str, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )

        if now >= target_time:
            dump_database()
            next_run = target_time + timedelta(days=1)
        else:
            next_run = target_time

        sleep_seconds = (next_run - datetime.now()).total_seconds()
        print(f"[{datetime.now()}] Next dump at {next_run}")
        time.sleep(max(1, sleep_seconds))


if __name__ == "__main__":
    load_dotenv(override=True)
    BASE_URL = os.getenv("BASE_URL")
    NUM_WORKERS = int(os.getenv("NUM_THREADS_WORKERS"))
    SCRAPING_TIME = os.getenv("SCRAPING_TIME")
    DB_DUMP_TIME = os.getenv("DB_DUMP_TIME")
    scrap_thread = Thread(target=start_daily_scrapper, args=(BASE_URL, NUM_WORKERS, SCRAPING_TIME))
    db_dump_thread = Thread(target=start_daily_dump, args=(DB_DUMP_TIME,))

    scrap_thread.start()
    db_dump_thread.start()

    scrap_thread.join()
    db_dump_thread.join()
