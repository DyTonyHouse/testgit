import datetime
colunm_data = datetime.datetime.now()

if type(colunm_data).__name__ == 'datetime':
    colunm_data = colunm_data.strftime('%Y-%m-%d %H:%M:%S')
    print(colunm_data)