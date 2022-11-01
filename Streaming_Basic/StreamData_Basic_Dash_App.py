import dash_core_components as dcc
import dash_html_components as html

from dash import Dash
from dash.dependencies import Input, Output
from dash_extensions import WebSocket

import json
import datetime

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


#%%

symbol = "btcusdt"
interval = "5m"
endpoint = f"wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}"

#%%


# Create example app.
app = Dash(prevent_initial_callbacks=True)
app.layout = html.Div([
    html.Div(id="MessageFromWebSocket"),
    WebSocket(url= endpoint, id="ws")
])



# Read from websocket.
@app.callback(Output("MessageFromWebSocket", "children"),
              [Input("ws", "message")])
def message(message):
        
    # json_message = json.loads(message)
    json_message = json.loads(message['data']) 
    candle = json_message['k']

    is_candle_close = candle['x']

    close = float(candle['c'])
    high =  float(candle['h'])
    low =  float(candle['l'])
    volume =  float(candle['v'])
    CloseTimeRawUTC = datetime.datetime.fromtimestamp(candle['T']/1000, tz=datetime.timezone.utc)
    CloseTimeUTC = round_time( CloseTimeRawUTC, 60 ).replace(tzinfo=None)
    
    # if is_candle_close:
    
    # it print current Bitcoin Price Becouse, Close Time' shows when candle will close
    return f"Current Bitcoin price: {round(close, 1)} USD"  # read from websocket

if __name__ == '__main__':
    app.run_server()