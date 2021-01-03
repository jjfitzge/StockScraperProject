import stock_scraper
from datetime import datetime
def sample_present_data(symbol, name):
    stock_scraper.get_url(symbol)
    price = stock_scraper.get_price()
    price_change = stock_scraper.get_perc_change()
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #Update history of requested stock
    stock_scraper.get_history(symbol, name)
    print("As of ", date_time, "the stock ", symbol, "has:\n"
          "Price = ", price, "\nPrice change = ", price_change)
sample_present_data("NFLX","Netflix")


