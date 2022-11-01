import websocket
import json
import datetime
# pip intall websocket-client==1.2.0
#%%


def round_time(dt, round_to_seconds=60):
    """Round a datetime object to any number of seconds
    dt: datetime.datetime object
    round_to_seconds: closest number of seconds for rounding, Default 1 minute.
    """
    rounded_epoch = round(dt.timestamp() / round_to_seconds) * round_to_seconds
    #rounded_dt = datetime.datetime.fromtimestamp(rounded_epoch).astimezone(dt.tzinfo)

    rounded_dt = datetime.datetime.fromtimestamp(rounded_epoch).astimezone(dt.tzinfo)
    return rounded_dt

def on_message(ws, message):
    
    #print(message) 
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_close = candle['x']

    if is_candle_close:
        
        close = float(candle['c'])
        high =  float(candle['h'])
        low =  float(candle['l'])
        volume =  float(candle['v'])
        CloseTimeRawUTC = datetime.datetime.fromtimestamp(candle['T']/1000, tz=datetime.timezone.utc)
        CloseTimeUTC = round_time( CloseTimeRawUTC, 60 ).replace(tzinfo=None)
        
        print(f"DtateTimeUTC: {CloseTimeUTC}, Price: {round(close, 1)} USD")


    

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")


   
    
symbol = "btcusdt"
interval = "1m"
endpoint = f"wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}"   
# endpoint = f"wss://stream.binance.com:9443/ws/@kline_1m"   
 
if __name__ == "__main__":
    
    ws = websocket.WebSocketApp(endpoint,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)


    ws.run_forever()
