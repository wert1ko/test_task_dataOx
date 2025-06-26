import queue
import cloudscraper
import re
from bs4 import BeautifulSoup
import requests
import threading

from models.product import Product
from database.connection import get_connection
from database.product_repository import init_db, insert_product


class AutoRiaScrapper:
    def __init__(self, base_url: str, num_threads: int = 5):
        self.base_url = base_url

        self.scraper = cloudscraper.create_scraper()
        self.db_queue = queue.Queue()
        self.conn = get_connection()
        self.cur = self.conn.cursor()
        self.num_threads = num_threads
        init_db(self.cur)

    def _insert_db(self) -> None:
        """
        Зберігає Product у базу через ProductRepository.
        Якщо вже існує ідентичний car_vin коміту не буде.
        """
        while True:
            product = self.db_queue.get()       # блокує, поки не з’явиться елемент
            if product is None:
                self.db_queue.task_done()
                break
            insert_product(self.cur, product)
            self.db_queue.task_done()


    def _scrape_urls_frompage(self):
        resp = requests.get(self.base_url)
        html = resp.text

        soup = BeautifulSoup(html, 'html.parser')
        urls = [a['href'] for a in soup.select('a.m-link-ticket[href]')]
        return urls

    def _get_phone_number(self, autoId, userId, phoneId):
        url = "https://auto.ria.com/bff/final-page/public/auto/popUp/"
        payload = {
            "blockId": "autoPhone",
            "autoId": autoId,
            "data": [
                ["userId", userId],
                ["phoneId", phoneId],
            ]
        }
        resp = requests.post(url,json=payload)
        try:
            s = "38" + str(resp.json()["additionalParams"]["phoneStr"])
            return int(''.join(filter(str.isdigit, s)))
        except Exception as e:
            return "-"
        
    def run(self):
        urls = self._scrape_urls_frompage()
        chunks = [urls[i::self.num_threads] for i in range(self.num_threads)]

        db_thread = threading.Thread(target=self._insert_db, daemon=True)
        db_thread.start()

        producers = []
        for chunk in chunks:
            t = threading.Thread(target=self._start_scrape_product, args=(chunk,))
            t.start()
            producers.append(t)

        for t in producers:
            t.join()

        self.db_queue.put(None)
        db_thread.join()

    def _start_scrape_product(self, urls):
        for url in urls:
            self._scrape_product(url)
           
    def _scrape_product(self, url):
        resp = requests.get(url)
        text = resp.text
        # with open('text.html', 'w', encoding='utf-8') as f:
        #     f.write(text)




        try:
            soup = BeautifulSoup(text, 'html.parser')
            vin_span = soup.find('span', class_='label-vin')
            car_vin = vin_span.get_text(strip=True)
        except Exception as e:
            m = re.search(r'"vehicleIdentificationNumber"\s*:\s*"([^"]+)"', text)
            car_vin = m.group(1) if m else "-"


        m = re.search(r'data-owner-id="(\d+)"', text)
        userId = m.group(1) if m else "-"

        m = re.search(r'data-phone-id="(\d+)"', text)
        phoneId = m.group(1) if m else "-"

        m = re.search(r'<h1 class="head"\s+title="([^"]+)"', text)
        title = m.group(1) if m else "-"

        m = re.search(r'href="https?://auto\.ria\.com/uk/dealers/([^/]+)/\d+/', text)
        userName = m.group(1) if m else 0 
        if not userName:
            m = re.search(r'window\.ria\.userName\s*=\s*"([^"]+)"', text)
            userName = m.group(1) if m else "-"

        m = re.search(r'_(\d+)\.html$', url)
        autoId = m.group(1) if m else "-"

        phone_number = self._get_phone_number(autoId, userId, phoneId)

        m = re.search(r'<source\s+srcset="([^"]+)"\s+type="image/webp">\s*<img\s+class="outline m-auto"',text)
        image_url = m.group(1) if m else "-"

        # images_count — беремо цифру після "з "
        m = re.search(r'<span class="mhide">з\s*(\d+)', text)
        images_count = int(m.group(1))-1 if m else 0
        # images_count = int(images_count)-1



        m = re.search(r'"price"\s*:\s*"(\d+)"', text)
        price_usd = int(m.group(1)) if m else 0

        m = re.search(r'"value"\s*:\s*(\d+)', text)
        odometer = int(m.group(1)) if m else 0

        m = re.search(r'<span class="state-num ua">([^<]+)<', text)
        car_number = m.group(1) if m else "-"
        
        product = Product(url = url, title = title, price_usd = price_usd, 
        odometr = odometer,username = userName,phone_number = phone_number, 
        image_url = image_url, images_count = images_count,car_number = car_number, car_vin = car_vin)
        self.db_queue.put(product)
        print(product)
