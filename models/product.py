class Product:
    """
    Domain model for a Car product.
    """
    def __init__(
        self,
        url: str,
        title: str,
        price_usd: int,
        odometr: int,
        username: str,
        phone_number: int,
        image_url: str,
        images_count: str,
        car_number: str,
        car_vin: str

    ):
        self.url = url
        self.title = title
        self.price_usd = price_usd
        self.odometr = odometr
        self.username = username
        self.phone_number = phone_number
        self.image_url = image_url
        self.images_count = images_count
        self.car_number = car_number
        self.car_vin = car_vin

    def __str__(self):
        return (
            f"Product:\n"
            f"  URL:            {self.url}\n"
            f"  Title:          {self.title}\n"
            f"  Price (USD):    {self.price_usd}\n"
            f"  Odometer:       {self.odometr}\n"
            f"  Seller:         {self.username}\n"
            f"  Phone:          {self.phone_number}\n"
            f"  Image URL:      {self.image_url}\n"
            f"  Images Count:   {self.images_count}\n"
            f"  Car Number:     {self.car_number}\n"
            f"  VIN:            {self.car_vin}\n"
        )
    
    # def __repr__(self):
    #     return (
    #         # f"<Product id={self.id} slug={self.slug!r} "
    #         # f"top_category={self.top_category!r} "
    #         # f"category={self.category!r}>"
    #     )
