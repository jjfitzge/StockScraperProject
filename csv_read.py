import csv
import main
import stock_scraper
import timeit

nasdaq_csv = "nasdaq_company_list.csv"
amex_csv = "stocks_csv/amex_company_list.csv"

def read_csv(filename):
    # start
    start = timeit.default_timer()
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        line = 0
        count = 0
        for row in reader:
            # main.sample_present_data(row[0])
            # print(row[0])

            # print(row[0])
            if line > 0:
                # main.sample_present_data(row[0])
                if row[2] != 'n/a':
                    # main.sample_present_data(row[0])
                    # stock = row[0]
                    # print(stock)
                    # stock_scraper.get_url(stock)
                    # stock_scraper.get_history(stock)
                    # print("Stock: ", stock, " price = ", stock_scraper.get_price())
                    if (row[3] != 'n/a') or (row[4] != 'n/a') or (row[5] != 'n/a') or (row[6] != 'n/a'):
                        # print(row)
                        count += 1
                        main.sample_present_data(row[0], row[1])


            line += 1
    # print(count)
    stop = timeit.default_timer()

    print('Time: ', stop - start)
read_csv(amex_csv)