from .connection import get_connection, get_cursor
from models.product import Product

def init_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ria_products (
        url             TEXT           UNIQUE NOT NULL,
        title           TEXT           NOT NULL,
        price_usd       INTEGER        NOT NULL,
        odometer        INTEGER        NOT NULL,
        username        TEXT           NOT NULL,
        phone_number    BIGINT         NOT NULL,
        image_url       TEXT           NOT NULL,
        images_count    INTEGER        NOT NULL,
        car_number      TEXT           NOT NULL,
        car_vin         TEXT           UNIQUE NOT NULL,
        datetime_found  TIMESTAMPTZ    NOT NULL
    );
    """
    )


def insert_product(cur, product: Product):
    """
    Вставляє product в БД.
    Якщо є car_vin ідентичний, пропускаємо.
    """
    cur.execute("""
        INSERT INTO ria_products (
            url,
            title,
            price_usd,
            odometer,
            username,
            phone_number,
            image_url,
            images_count,
            car_number,
            car_vin,
            datetime_found
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            NOW()
        )
        ON CONFLICT (car_vin) DO NOTHING
    """, (
        product.url,
        product.title,
        product.price_usd,
        product.odometr,
        product.username,
        product.phone_number,
        product.image_url,
        product.images_count,
        product.car_number,
        product.car_vin,
    ))
    cur.connection.commit()



