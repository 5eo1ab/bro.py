## How to user DB connetion

### Install package @ Anaconda environment
`conda install mysql-connector-python`

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
query = (YOUR_QUERY)
cursor.execute(query)
table_rows = cursor.fetchall()
cursor.close()
```

### Transform pandas.DataFrame
```
from pandas import DataFrame as df
table_df = df(table_rows)
df_offers.columns = [ ... ]
```
