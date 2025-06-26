# Опис

Основний клас зі всім функціонал знаходиться в scrappers/auto_ria_scrapper.py, 
_insert_db
Приватний метод який в окремому потоці записує в дб продукт класу Product.

_scrape_urls_frompage
Приватний метод, парсить урли на машини з першої сторінки.

_get_phone_number
Приватний метод, дістає номер телефону оголошення.

_scrape_product
Приватний метод який скрапить всі дані які потрібно з оголошення та записує в бд викликаючи _insert_db.
В нас є оголошення де може не бути Номеру автомобілю, Юзернейму, Вінкоду. Для таких оголошень замість поля якого нема записується "-". 

run
Метод входу, створює NUM_THREADS потоків + 1 для запису в бд(_insert_db).

main.py:

start_daily_scrapper:
Приймає час, та запускає скрапер кожного дня в час який зазначений в env.

start_daily_dump:
Приймає час, та запускає дамп бази кожного дня в час який зазначений в env.

Адже в обох функціях є time.sleep(), запуск цих обох функцій відбувається з використанням двох потоків щоб уникнути того що одна функція буде чекати іншу і через це дамп бази або скрапер спрацює пізніше за зазначений в енв час.
```
    scrap_thread = Thread(target=start_daily_scrapper, args=(BASE_URL, NUM_WORKERS, SCRAPING_TIME))
    db_dump_thread = Thread(target=start_daily_dump, args=(DB_DUMP_TIME,))

    scrap_thread.start()
    db_dump_thread.start()

    scrap_thread.join()
    db_dump_thread.join()
```





# Guidance to SETUP:
Clone repository

```
git clone https://github.com/wert1ko/test_task_dataOx.git
```

```
cd test_task_dataOx
```

```
python -m venv env
```

MAC OS/Linux
``` 
source env/bin/activate
```
WINDOWS
```
env\Scripts\activate
```

```
pip install requirments.txt
```

Create .env
ENV EXAMPLE:
```
BASE_URL = "https://auto.ria.com/uk/car/used/"
SCRAPING_TIME = 12:00
NUM_THREADS_WORKERS = 8

DB_DUMP_TIME = 15:00
DB_HOST = 127.0.0.1
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres

```

```python main.py```

