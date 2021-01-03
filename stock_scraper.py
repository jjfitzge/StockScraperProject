from datetime import datetime

import requests
from bs4 import BeautifulSoup

import sql_db
price_data = []
url = ""
page = ""
soup = ""
# url = "https://finance.yahoo.com/quote/AMZN?p=AMZN"
def get_url(symbol):
    # Append requested ticker symbol at the end of our url "https://finance.yahoo.com/quote/
    global url
    url = "https://finance.yahoo.com/quote/" + symbol + "/history?p=" + symbol
    global price_data
    global page
    global soup
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    price_data = soup.find(class_="D(ib) Mend(20px)").find_all("span")


def get_price():
    # print("Current Price: ", price)
    return price_data[0].text
def get_perc_change():
    # print("Current Price: ", price)
    return price_data[1].text
# get_url("AAPL")
# print(get_price())
# print(get_perc_change())

# Scrape History page to get data for requested stock ticker

def get_history(symbol, name):
    # First check if we already have history for symbol
    if sql_db.ticker_exists(sql_db.conn, symbol):
        # Todo: add standardization for timezone
        date_now = datetime.today().strftime("%b %d, %Y")
        # print(date_now)
        last_update_time = sql_db.get_last_update(sql_db.conn, symbol)
        # print(last_update_time)
        if last_update_time != date_now:
            print("Dates don't match: Updating history....")
            # update tables
            historical_table = soup.find("section", class_="smartphone_Px(20px)")
            # get all data from data
            table_data = historical_table.find('tbody')
            # print(table_data)
            data_row = table_data.find_all(class_="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)")[0]
            # fill in values for stock table
            new_update = data_row.find(class_="Py(10px) Ta(start) Pend(10px)").text

            with sql_db.conn:
                sql_db.update_stock(sql_db.conn, (new_update, symbol))
            vert_data = data_row.find_all(class_="Py(10px) Pstart(10px)")
            # Insert new row into DATES table
            open_price = vert_data[0].text
            high = vert_data[1].text
            low = vert_data[2].text
            close = vert_data[3].text
            volume = vert_data[5].text
            # print("Inserting new row Symbol = ",symbol, "New date = ",new_update, "open_price = ",open_price, "......")
            date_insert = (symbol, name, new_update, open_price, high, low, close, volume)
            sql_db.create_date(sql_db.conn, date_insert)
            return
        # TODO: UPDATE current day continuously if market is upon
        # TODO: ADD LOGIC TO CONTROL FLOW FOR WHEN MARKET IS OPEN (I.E NOT Holidays and weekends)
        else:
            print("Stock History is up to date")
            return
    else:
        # Then check if current access date is last_update if not insert new row in dates and update last update
        # otherwise return immediately

        historical_table = soup.find("section", class_="smartphone_Px(20px)")
        # get all data from data
        table_data = historical_table.find('tbody')
        # print(table_data)
        data_list = table_data.find_all(class_="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)")
        # fill in values for stock table
        last_update = data_list[0].find(class_="Py(10px) Ta(start) Pend(10px)").text
        stock = (symbol, name, last_update)
        sql_db.create_stock(sql_db.conn, stock)
        for data in data_list:
            date = data.find(class_="Py(10px) Ta(start) Pend(10px)").text
            # temp to store all other fields of data for specific data
            vert_data = data.find_all(class_="Py(10px) Pstart(10px)")
            # Dividen rows only have a length of 1
            if len(vert_data) > 1:
                open_price = vert_data[0].text
                high = vert_data[1].text
                low = vert_data[2].text
                close = vert_data[3].text
                volume = vert_data[5].text
                date_insert = (symbol, name, date, open_price, high, low, close, volume)
                sql_db.create_date(sql_db.conn, date_insert)

    #
# get_history("DIS")

