## How to use DB connetion

### Install [package](https://pypi.python.org/pypi/mysql-connector-python) 
`conda install mysql-connector-python`  
@ Anaconda environment  

### Create connection
```
import mysql.connector
cnx = mysql.connector.connect(
        user = USER_NAME,
        password = PASSWORD,
        host = IP_ADDRESS, 
        database = 'bropy'
        )
```
bro.py IP address: '192.168.0.4'  

### Create cursor
```
cursor = cnx.cursor()
query = YOUR_QUERY
cursor.execute(query)
table_rows = cursor.fetchall()
cursor.close()
```
`query = "SELECT * FROM G_IDX_CLOSE"`

### Transform pandas.DataFrame
```
from pandas import DataFrame as df
table_df = df(table_rows)
df_offers.columns = [ ... ]
```
USE **column names dictionary** (Read `colnames.json`)



## How to column names dictionary
```
import json
fpath = './colnames.json'
colnames = json.load(open(fpath))
```

column descriptions : `META_DATA.xlsx`

