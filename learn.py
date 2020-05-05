import pandas as pd
import os
import time
from pathlib import Path
from datetime import datetime

path = 'data/'

def Key_Stats(gather='Total Debt/Equity (mrq)'):

    # 1// get data path
    statspath = path + '_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)] # notice: it lists the root dir (first element)

    # 2// create panda data frame
    df = pd.DataFrame(columns = ['Date', 'Unix', 'Ticker', 'DE Ratio'])

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split('/')[2]
        if len(each_file) > 0:
            for file_name in each_file:
                date_stamp = datetime.strptime(file_name, '%Y%m%d%H%M%S.html') # strip date from file name
                unix_time = time.mktime(date_stamp.timetuple()) # convert to unix format
                source = open(f'{each_dir}/{file_name}', 'r').read() # opening the html file for read
                try:
                    # convert to float to avoid error
                    value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]) # hack to not use bs
                    df = df.append({'Date':date_stamp,'Unix':unix_time,'Ticker':ticker,'DE Ratio':value,}, ignore_index = True)
                except Exception as _e:
                    pass

    save = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
    Path('output').mkdir(parents=True, exist_ok=True) # create folder output if not exists
    df.to_csv(f'output/{save}')

Key_Stats()
