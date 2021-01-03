import sqlite3
from sqlite3 import Error

# Change to desired database
database = r"C:\sqlite\databases\stocks.db"


def init_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn


init_connection(database)


# One main table to organize seperate stocks
# sub tables for each date to record the history for previous dates
# ----------Company/Stock Table---------                    ------------Date----------------
# * Stock Ticker                                                 *Ticker
#   Company Name                            --------------->      date
#   Last Update (date)                                           open price
#                                                                high
#                                                                Low
# --------------------------------------                         Close
#                                                                Volume
#                                                            ---------------------------------
def create_table(conn, table):
    try:
        cursor = conn.cursor()
        cursor.execute(table)
    except Error as e:
        print(e)


conn = create_connection(database)


def table_init():
    stock_table = """ CREATE TABLE IF NOT EXISTS stock (
                                            stock_ticker text PRIMARY KEY,
                                            name text,
                                            last_update text NOT NULL
                                        ); """

    dates_table = """CREATE TABLE IF NOT EXISTS dates (
                                    ticker text,
                                    name text,
                                    date text NOT NULL,
                                    open_price float NOT NULL,
                                    high float NOT NULL,
                                    low float NOT NULL,
                                    close_price float NOT NULL,
                                    volume integer NOT NULL,
                                    FOREIGN KEY (ticker) REFERENCES stock (stock_ticker)
                                );"""

    if conn is not None:
        create_table(conn, stock_table)
        create_table(conn, dates_table)
    else:
        print("Error: Unable to connect to the database")


table_init()


def create_stock(conn, stock):
    insert = ''' INSERT INTO stock(stock_ticker,name,last_update) VALUES(?,?,?)'''
    cursor = conn.cursor()
    cursor.execute(insert, stock)
    conn.commit()


def create_date(conn, date):
    insert = ''' INSERT INTO dates(ticker,name,date,open_price,high,low,close_price,volume) VALUES(?,?,?,?,?,?,?,?)'''
    cursor = conn.cursor()
    cursor.execute(insert, date)
    conn.commit()


def ticker_exists(conn, symbol):
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT * FROM stock WHERE stock_ticker=?)", (symbol,))
    return cursor.fetchone()[0]
    # return bool_val


def get_last_update(conn, symbol):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock WHERE stock_ticker=?", (symbol,))
    row = cursor.fetchone()
    # print(row[2])
    return row[2]


def update_stock(conn, request):
    update = '''UPDATE stock SET last_update=? WHERE stock_ticker =?'''
    cursor = conn.cursor()
    cursor.execute(update, request)
    conn.commit()
