import pandas as pd
import os
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
path = 'data/'

def Key_Stats(gather='Total Debt/Equity (mrq)'):

    # 1// get data path
    statspath = path + '_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)] # notice: it lists the root dir (first element)
    save_filename = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')

    # 2// create panda data frame for ratios
    df = pd.DataFrame(columns = ['Date',
                                'Unix',
                                'Ticker',
                                'DE Ratio',
                                'Price',
                                'stock_p_change',
                                'SP500',
                                'sp500_p_change'])

    # 3// create panda data frame for s&p500
    sp500_df = pd.read_csv(f'{path}GSPC.csv')

    # 4// keep track of tickers already parsed for % changes
    ticker_list = []

    for each_dir in stock_list[1:5]: # NOTICE: remove upper limit
        each_file = os.listdir(each_dir)
        
        # extract tiker from dir name
        ticker = each_dir.split('/')[2]

        # temporary list containing all stocks
        stocks_ticker_list = []

        if len(each_file) > 0:
            for file_name in each_file:
                date_stamp = datetime.strptime(file_name, '%Y%m%d%H%M%S.html') # strip date from file name
                unix_time = time.mktime(date_stamp.timetuple()) # convert to unix format
                source = open(f'{each_dir}/{file_name}', 'r').read() # opening the html file for read
                try:
                    # convert to float to avoid error
                    value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]) # hack to not use bs

                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.Date == sp500_date)]
                        sp500_value = float(row["Adj Close"])
                    except:
                        cheat = 259200 # to be changed into complexer wk identifier 
                        sp500_date = datetime.fromtimestamp(unix_time-cheat).strftime('%Y-%m-%d') # date format we have in our csv
                        row = sp500_df[(sp500_df.Date == sp500_date)]
                        sp500_value = float(row['Adj Close'])
                    
                    stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    stocks_ticker_list.append({
                        'Date':date_stamp,
                        'Unix':unix_time,
                        'Ticker':ticker,
                        'DE Ratio':value,
                        'Price':stock_price,
                        'SP500':sp500_value})
                    
                except Exception as _e:
                    pass
            
            # save list to dataframe
            tmp = sorted(stocks_ticker_list, key=lambda r: r['Date'])
            print(tmp)
            df.append([], ignore_index = True)

    Path('output').mkdir(parents=True, exist_ok=True) # create folder output if not exists
    df.to_csv(f'output/{save_filename}')


# if os.path.isfile(f'output/{save_filename}'):
#     pass
# else:
Key_Stats()
