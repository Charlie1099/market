import config
import sqlite3
import alpaca_trade_api as tradeapi

connection = sqlite3.connect('app.db')
# This will tell the SQLite connection to return sqlite Row objects.
connection.row_factory = sqlite3.Row


cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, name FROM stock
""")

rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows] # list comprehension



api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("INSERT INTO stock (symbol, name) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()