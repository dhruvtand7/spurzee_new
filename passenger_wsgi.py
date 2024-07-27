import os
import sys
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, render_template
import requests
import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
import pandas_ta as ta
import plotly.io as pio
from sklearn.cluster import DBSCAN
import json
from fyers_apiv3 import fyersModel
import datetime as dt
import plotly
import pyotp
import mysql.connector
from urllib.parse import parse_qs, urlparse
import base64
import warnings
import pytz
import math
import requests
from time import sleep
from datetime import datetime, timedelta, date
import webbrowser
import os
import sys
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
# from flask_mail import Mail, Message
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
import pandas_ta as ta
import plotly.io as pio
from sklearn.linear_model import LinearRegression
import json
from fyers_apiv3 import fyersModel
import os
import datetime as dt
import plotly
import pyotp
import mysql.connector

sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
users = {'admin': {'password': 'user98440', 'role': 'admin'},
    'user2': {'password': 'user98840', 'role': 'limited'},
    'user1': {'password': 'user@123', 'role': 'admin'}
}

from fyers_apiv3 import fyersModel
import webbrowser

# redirect_uri= "http://127.0.0.1"  ## redircet_uri you entered while creating APP.
# client_id = "DZO41L3M36-100"                       ## Client_id here refers to APP_ID of the created app
# secret_key = "FDGH8EAMHW"                          ## app_secret key which you got after creating the app 
# grant_type = "authorization_code"                  ## The grant_type always has to be "authorization_code"
# response_type = "code"                             ## The response_type always has to be "code"
# state = "sample"                                   ##  The state field here acts as a session manager. you will be sent with the state field after successfull generation of auth_code 
# FY_ID="YL00137"
# TOTP_KEY="EWQ3JH35FTQA6IQLYNZEGNB7WACXTRSG"
# PIN="8844"

# ### Connect to the sessionModel object here with the required input parameters
# appSession = fyersModel.SessionModel(client_id = client_id, redirect_uri = redirect_uri,response_type=response_type,state=state,secret_key=secret_key,grant_type=grant_type)

# # ## Make  a request to generate_authcode object this will return a login url which you need to open in your browser from where you can get the generated auth_code 
# generateTokenUrl = appSession.generate_authcode()
# generateTokenUrl
from datetime import datetime, timedelta, date
from  time import sleep
import os
import pyotp
import requests
import json
import math
import pytz
from urllib.parse import parse_qs,urlparse
import warnings
import pandas as pd
# pd.set_option('display.max_columns', None)
# warnings.filterwarnings('ignore')

# import base64
# def getEncodedString(string):
#     string = str(string)
#     base64_bytes = base64.b64encode(string.encode("ascii"))
#     return base64_bytes.decode("ascii")
  



# URL_SEND_LOGIN_OTP="https://api-t2.fyers.in/vagator/v2/send_login_otp_v2"
# res = requests.post(url=URL_SEND_LOGIN_OTP, json={
#                     "fy_id": getEncodedString(FY_ID), "app_id": "2"}).json()  
# print(res) 

# if datetime.now().second % 30 > 27 : sleep(5)
# URL_VERIFY_OTP="https://api-t2.fyers.in/vagator/v2/verify_otp"
# res2 = requests.post(url=URL_VERIFY_OTP, json= {"request_key":res["request_key"],"otp":pyotp.TOTP(TOTP_KEY).now()}).json()  
# print(res2) 


# ses = requests.Session()
# URL_VERIFY_OTP2="https://api-t2.fyers.in/vagator/v2/verify_pin_v2"
# payload2 = {"request_key": res2["request_key"],"identity_type":"pin","identifier":getEncodedString(PIN)}
# res3 = ses.post(url=URL_VERIFY_OTP2, json= payload2).json()  
# print(res3) 


# ses.headers.update({
#     'authorization': f"Bearer {res3['data']['access_token']}"
# })


# TOKENURL="https://api-t1.fyers.in/api/v3/token"
# payload3 = {"fyers_id":FY_ID,
#           "app_id":client_id[:-4],
#           "redirect_uri":redirect_uri,
#           "appType":"100","code_challenge":"",
#           "state":"None","scope":"","nonce":"","response_type":"code","create_cookie":True}

# res3 = ses.post(url=TOKENURL, json= payload3).json()  
# print(res3)


# url = res3['Url']
# print(url)
# parsed = urlparse(url)
# auth_code = parse_qs(parsed.query)['auth_code'][0]
# auth_code


# grant_type = "authorization_code" 

# response_type = "code"  

# sess = fyersModel.SessionModel(
#     client_id=client_id,
#     secret_key=secret_key, 
#     redirect_uri=redirect_uri, 
#     response_type=response_type, 
#     grant_type=grant_type
# )

# # Set the authorization code in the session object
# sess.set_token(auth_code)

# # Generate the access token using the authorization code
# response = sess.generate_token()

# # Print the response, which should contain the access token and other details
# #print(response)


# access_token = response['access_token']

with open("abcd.txt", 'r') as r:
    access_token = r.read()

client_id = "DZO41L3M36-100"
fyers = fyersModel.FyersModel(
    client_id=client_id, is_async=False, token=access_token, log_path=os.getcwd())
    
def read_stocks_from_file():
    with open('50stocks.txt', "r") as f:
        lines = f.readlines()
        stocks = [{'label': line.strip(), 'value': line.strip()} for line in lines]
    return stocks

time_intervals = [
    {'label': '1', 'value': '1'},
    {'label': '3', 'value': '3'},
    {'label': '5', 'value': '5'},
    {'label': '15', 'value': '15'},
    {'label': '1H', 'value': '60'},
    {'label': '1D', 'value': '1440'}
]

db_config = {
    'host': 'localhost',
    'user': 'sqluser1',
    'password': 'TGDp0U&[1Y4S',
    'database': 'stocks'
}
db_config2 = {
    'host': '118.139.182.3',
    'user': 'sqluser1',
    'password': 'TGDp0U&[1Y4S',
    'database': 'user_registration'
}

db_config3 = {
    'host': '118.139.182.3',
    'user': 'sqluser1',
    'password': 'TGDp0U&[1Y4S',
    'database': 'stocks'
}
db_config4 = {
    'host': '118.139.182.3',
    'user': 'sqluser1',
    'password': 'TGDp0U&[1Y4S',
    'database': 'news'
}


def generate_graph(symbol, start_date, end_date, interval, ema_visible,emaval, sr_visible, nsr, trline, dtop, dbottom, ttop, tbottom, srcands, th, ibars, ema5,box, bth, nbc, hsind, vshape, mestar):
    
    con = mysql.connector.connect(**db_config3)
    cur = con.cursor()
    sym = symbol
    parts = sym.split(':')[-1].replace('-', '_').replace('&', '_')
    sym = parts.lower()
    
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'stocks'")
    tables = cur.fetchall()
    tables = [table[0] for table in tables]
    if sym in tables and interval != '1' and interval != '3':
        
        query = f"SELECT t.INTERVAL_START AS `Interval`, t.`Open`, t.`High`, t.`Low`, ae.`Close`, t.`Volume` " \
                    f"FROM (SELECT (UNIX_TIMESTAMP(`date`) - (UNIX_TIMESTAMP(DATE_FORMAT(`date`, '%Y-%m-%d 09:15:00'))))  DIV ({interval} * 60) + UNIX_TIMESTAMP(DATE_FORMAT(`date`, '%Y-%m-%d 09:15:00')) AS interval_id, " \
                    f"MIN(`date`) AS INTERVAL_START, " \
                    f"`open` AS `Open`, " \
                    f"MAX(`high`) AS `High`, " \
                    f"MIN(`low`) AS `Low`, " \
                    f"MAX(`date`) AS max_date,    " \
                    f"SUM(`volume`) AS `Volume` " \
                    f"FROM {sym} " \
                    f"WHERE " \
                    f"`date` BETWEEN '{start_date}' AND  '{end_date} 16:00:00'" \
                    f"GROUP BY interval_id) AS t "\
                    f"INNER JOIN {sym} ae ON ae.`date` = t.max_date "\
                    f"LIMIT 5000"
        cur.execute(query)
        results = cur.fetchall()
        columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        df = pd.DataFrame(results, columns=columns)
       
        dtime_datetime = dt.datetime.now()
        dtime_datetime += timedelta(hours=12, minutes=30)
        dtime = dtime_datetime.strftime("%Y-%m-%d")
        if end_date >= dtime :
            data = {
            "symbol": symbol,
            "resolution": interval,
            "date_format": "1",
            "range_from": dtime,
            "range_to": dtime,
            "cont_flag": "1"
            }
            df2 = pd.DataFrame(fyers.history(data=data)['candles'])
            df2.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            df2['date'] = pd.to_datetime(df2['date'], unit='s')
            df2.date = (df2.date.dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata'))
            df2['date'] = df2['date'].dt.tz_localize(None)
            df = pd.concat([df,df2],ignore_index=True)
        
    else :
        data = {
            "symbol": symbol,
            "resolution": interval,
            "date_format": "1",
            "range_from": start_date,
            "range_to": end_date,
            "cont_flag": "1"
        }
        df = pd.DataFrame(fyers.history(data=data)['candles'])
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    
        df['date'] = pd.to_datetime(df['date'], unit='s')
        df.date = (df.date.dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata'))
        df['date'] = df['date'].dt.tz_localize(None)
        
    df_sorted = df.sort_values(by=['date'], ascending=True)
    df = df_sorted.drop_duplicates(subset='date', keep='first')
    df.reset_index(drop=True, inplace=True)
    df["EMA"] = ta.ema(df["close"], length=emaval)
    
    
    
    if len(df) > 2000 :
        if nsr==0:
            nsr = 8
        prd = int(len(df)/75)
    elif len(df) > 1500 :
        if nsr==0:
            nsr = 8
        prd = int(len(df)/50)
    elif len(df) > 1000 :
        if nsr==0:
            nsr = 7
        prd = int(len(df)/50)
    elif len(df) > 500 :
        if nsr==0:
            nsr = 6
        prd = int(len(df)/25)
    elif len(df) > 100 :
        if nsr==0:
            nsr = 5
        prd = int(len(df)/25)
    else :
        if nsr==0:
            nsr = 4
        prd = int(len(df)/10)
    
    sup = df[df.low == df.low.rolling(prd, center=True).min()].low
    res = df[df.high == df.high.rolling(prd, center=True).max()].high
    lev = sup.tolist() + res.tolist()
    lev.sort()
    
    kmeans = KMeans(n_clusters=min(int(nsr), len(lev)),random_state=42).fit(
        np.array(lev).reshape(-1, 1))
    lset = []
    for cluster_center in kmeans.cluster_centers_:
        closest_index = np.argmin(np.abs(lev - cluster_center))
        lset.append(lev[closest_index])

    # fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
    #                     vertical_spacing=0.1, row_heights=[0.8, 0.2])
    # fig.add_trace(go.Candlestick(x=df['date'], open=df['open'], high=df['high'],
    #               low=df['low'], close=df['close'], name='Candlestick'), row=1, col=1)
    # if ema_visible == 'true':
    #     ema_trace = go.Scatter(
    #         x=df['date'], y=df['EMA'], mode='lines', name='EMA')
    #     fig.add_trace(ema_trace, row=1, col=1)
    # fig.add_trace(go.Bar(x=df['date'], y=df['volume'],
    #               name='Volume', marker_color='black', marker_opacity=0.9), row=2, col=1)
    # fig.update_layout(
    #     title=symbol, xaxis_rangeslider_visible=False, showlegend=False
    # )
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True,
                        specs=[[{"secondary_y": True}]])

    # Add the candlestick trace
    fig.add_trace(go.Candlestick(
        x=df['date'], 
        open=df['open'], 
        high=df['high'],
        low=df['low'], 
        close=df['close'], 
        name='Candlestick'), 
        row=1, col=1, secondary_y=False)

    # Add the EMA trace if visible
    if ema_visible == 'true':
        fig.add_trace(go.Scatter(
            x=df['date'], 
            y=df['EMA'], 
            mode='lines', 
            name='EMA'), 
            row=1, col=1, secondary_y=False)

    # Add the volume trace on the secondary y-axis
    fig.add_trace(go.Bar(
        x=df['date'], 
        y=df['volume'],
        name='Volume', 
        marker_color='black', 
        marker_opacity=0.2), 
        row=1, col=1, secondary_y=True)

    # Define the light and dark mode layouts
    light_mode_layout = dict(
        plot_bgcolor='#e6ecf5',
        paper_bgcolor='white',
        font=dict(color='#000')
    )

    dark_mode_layout = dict(
        plot_bgcolor='black',
        paper_bgcolor='white',
        font=dict(color='#000')
    )
    # Update the layout
    fig.update_layout(
        title=symbol,
        xaxis_rangeslider_visible=False,
        showlegend=False,
        yaxis_fixedrange=True,
        yaxis2_fixedrange=True,
        dragmode='pan'
    )
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=[
                    dict(
                        label="Light",
                        method="relayout",
                        args=[light_mode_layout]
                    ),
                    dict(
                        label="Dark",
                        method="relayout",
                        args=[dark_mode_layout]
                    )
                ],
                pad={"r": 10, "t": 10},
                showactive=True,
                x=1.15,  # Positioning the menu to the right
                xanchor="right",  # Anchoring to the right
                y=1.15,  # Positioning above the plot
                yanchor="top"  # Anchoring to the top
            ),
        ]
    )

    # Update y-axes titles
    fig.update_yaxes(title_text="Price", secondary_y=False, showgrid = False)
    fig.update_yaxes(title_text="Volume", secondary_y=True, showgrid = False)


    # fig.update_yaxes(side='right')


    if symbol[:3] == 'MCX' :
        bounds = [24,9]
    elif interval == '1440':
        bounds = [12,18]
    elif interval == '5':
        bounds = [15.5,9.25]
    elif interval == '15':
        bounds = [15.5,9.25]
    elif interval == '30':
        bounds = [15.75,9.25]
    else :
        bounds = [16,9.25]
    alldays =set(df.date[0]+timedelta(x) for x in range((df.date[len(df.date)-1]- df.date[0]).days))
    missing=sorted(set(alldays)-set(df.date))
    fig.update_xaxes(
        rangeslider_visible=False,
        rangebreaks=[
            dict(bounds=bounds, pattern="hour"),
            dict(values=missing)
        ]
    )
    # fig.update_yaxes(side='right')
    fig.update_layout(yaxis=dict(tickformat='.f'))
    fig.update_layout(margin=dict(l=20, r=50, t=30, b=50))
    if sr_visible == 'true':
        for l in lset:
            fig.add_shape(type='line', x0=df['date'][0], y0=l, x1=df['date'][len(df)-1], y1=l)
    if trline == 'true':
        if interval == '60':
            climit = 3
            dlimit = 2
            prd = 6
        elif interval == '15':
            climit = 5
            dlimit = 2
            prd = 10
        elif interval == '5':
            climit = 7
            dlimit = 3
            prd = 15
        elif interval == '3':
            climit = 4
            dlimit = 2
            prd = 8
        elif interval == '1':
            climit = 7
            dlimit = 1
            prd = 6
        else:
            climit = 2
            dlimit = 2
            prd = 6
        sup=df[df.low==df.low.rolling(prd*2,center=True).min()].low
        res=df[df.high==df.high.rolling(prd*2,center=True).max()].high
        pl = list(zip(sup.index, sup))
        ph = list(zip(res.index, res))
        valid = False
        uv1 = uv2 = up1 = up2 = 0
        ilimit = len(df)
        uplines = []
        for i in range(len(pl)-1,0,-1):
            if pl[i][0] > ilimit :
                continue
            for j in range(0,i-1):
                val1=pl[i][1]
                val2=pl[j][1]
                pos1=pl[i][0]
                pos2=pl[j][0]
                if val1>val2:
                    diff = (val1 - val2) / (pos1 - pos2)
                    hline = val2 
                    lloc = pos1
                    lval = val1
                    valid = True
                    c=d=0
                    for x in range(j+1,i):
                        hline = val2 + (pl[x][0] - pos2) * diff
                        if df['close'][pl[x][0]] < hline :
                            valid = False
                            break
                        elif df['low'][pl[x][0]] < hline * (1.005):
                            c+=1
                            d = 0
                        else:
                            d+=1
                            if d > dlimit :
                                valid = False
                                break
                    if valid and i-j > 2 and c > climit:
                        # while (lval < df['close'][lloc]) and (lloc < len(df)-1):
                        #     lloc+=1
                        #     lval+=diff
                        uv1 = lval 
                        uv2 = val2
                        up1 = lloc
                        up2 = pos2
                        uplines.append((uv1,uv2,up1,up2))
                        uv1 = uv2 = up1 = up2 = 0
                        ilimit = pl[j][0]

                        break
        valid = False
        dv1 = dv2 = dp1 = dp2 = 0
        ilimit = len(df)
        dnlines = []
        for i in range(len(ph)-1,0,-1):
            if ph[i][0] > ilimit :
                continue
            for j in range(0,i-1):
                val1=ph[i][1]
                val2=ph[j][1]
                pos1=ph[i][0]
                pos2=ph[j][0]
                if val1<val2:  
                    diff = (val2 - val1) / (pos1 - pos2)
                    hline = val2 
                    lloc = pos1
                    lval = val1
                    valid = True
                    c=d=0
                    for x in range(j+1,i):
                        hline = val2 - (ph[x][0] - pos2) * diff
                        if df['close'][ph[x][0]] > hline :
                            valid = False
                            break
                        elif df['high'][ph[x][0]] > hline * 0.995:
                            c+=1
                            d = 0
                        else:
                            d+=1
                            if d > dlimit :
                                valid = False
                                break
                    if valid and i-j > 2 and c > climit:
                        # while (lval > df['close'][lloc]) and (lloc < len(df)-1):
                        #     lloc+=1
                        #     lval-=diff
                        dv1 = lval
                        dv2 = val2
                        dp1 = lloc
                        dp2 = pos2
                        dnlines.append((dv1,dv2,dp1,dp2))
                        dv1 = dv2 = dp1 = dp2 = 0
                        ilimit = ph[j][0]                
                        break
        valid = False
        uv1 = uv2 = up1 = up2 = 0
        ilimit = len(df)
        for i in range(len(ph)-1,0,-1):
            if ph[i][0] > ilimit :
                continue
            for j in range(0,i-1):
                val1=ph[i][1]
                val2=ph[j][1]
                pos1=ph[i][0]
                pos2=ph[j][0]
                if val1>val2:
                    diff = (val1 - val2) / (pos1 - pos2)
                    hline = val2 
                    lloc = pos2
                    lval = hline
                    valid = True
                    c=d=0
                    for x in range(j+1,i):
                        hline = val2 + (ph[x][0] - pos2) * diff
                        if df['close'][ph[x][0]] > hline :
                            valid = False
                            break
                        elif df['high'][ph[x][0]] > hline * 0.995:
                            c+=1
                            d = 0
                        else:
                            d+=1
                            if d > dlimit :
                                valid = False
                                break
                    if valid and i-j > 2 and c > climit:
                        # while (lval > df['close'][lloc]) and (lloc > 0):
                        #     lloc-=1
                        #     lval-=diff
                        uv1 = lval 
                        uv2 = val1
                        up1 = lloc
                        up2 = pos1
                        uplines.append((uv1,uv2,up1,up2))
                        uv1 = uv2 = up1 = up2 = 0
                        ilimit = ph[j][0]

                        break
        valid = False
        dv1 = dv2 = dp1 = dp2 = 0
        ilimit = len(df)
        for i in range(len(pl)-1,0,-1):
            if pl[i][0] > ilimit :
                continue
            for j in range(0,i-1):
                val1=pl[i][1]
                val2=pl[j][1]
                pos1=pl[i][0]
                pos2=pl[j][0]
                if val1<val2:  
                    diff = (val2 - val1) / (pos1 - pos2)
                    hline = val2 
                    lloc = pos2
                    lval = hline
                    valid = True
                    c=d=0
                    for x in range(j+1,i):
                        hline = val2 - (pl[x][0] - pos2) * diff
                        if df['close'][pl[x][0]] < hline :
                            valid = False
                            break
                        elif df['low'][pl[x][0]] < hline * 1.005:
                            c+=1
                            d = 0
                        else:
                            d+=1
                            if d > dlimit :
                                valid = False
                                break
                    if valid and i-j > 2 and c > climit:
                        # while (lval < df['close'][lloc]) and (lloc > 0):
                        #     lloc-=1
                        #     lval+=diff
                        dv1 = lval
                        dv2 = val1
                        dp1 = lloc
                        dp2 = pos1
                        dnlines.append((dv1,dv2,dp1,dp2))
                        dv1 = dv2 = dp1 = dp2 = 0
                        ilimit = pl[j][0]            
                        break
        def angle_with_x_axis( y1, y2, x1, x2):
            diff = max(df['high']) - min(df['low'])
            dx = x2 - x1
            dy = (y2 - y1) * (len(df)/diff)
            angle_rad = math.atan2(dy, dx)
            
            angle_deg = math.degrees(angle_rad)
            angle_deg = abs(angle_deg)
            if angle_deg > 90:
                angle_deg = 180 - angle_deg
            return angle_deg
        for up in uplines :
            angle = angle_with_x_axis(up[0], up[1], up[2], up[3])
            fig.add_shape(type="line",
                x0=df['date'][up[3]], y0=up[1], x1=df['date'][up[2]], y1=up[0],
                line=dict(color="Green",width=1)
            )
            mid_x = (up[3] + up[2]) // 2
            mid_y = (up[1] + up[0]) / 2
        
            # Add a text annotation just above the line
            fig.add_annotation(x=df['date'][mid_x], y=mid_y, text=int(angle), showarrow=False, 
                font=dict(
                    size=10,
                    color="Green"
                ),
                #textangle=angle 
            )
        for dn in dnlines:
            angle = angle_with_x_axis(dn[0], dn[1], dn[2], dn[3])
            fig.add_shape(type="line",
                x0=df['date'][dn[3]], y0=dn[1], x1=df['date'][dn[2]], y1=dn[0],
                line=dict(color="Red",width=1)
            )
            mid_x = (dn[3] + dn[2]) // 2
            mid_y = (dn[1] + dn[0]) / 2
        
            # Add a text annotation just above the line
            fig.add_annotation(x=df['date'][mid_x], y=mid_y, text=int(angle), showarrow=False, 
                font=dict(
                    size=10,  
                    color="Red"
                ),
                #textangle=angle 
            )
    if dtop == 'true':
        def calculate_slope_angle(x, y):
            # Fit a linear regression model
            model = LinearRegression().fit(x.reshape(-1, 1), y)
            
            # Get the slope from the linear regression model
            slope = model.coef_[0]
            
            # Calculate the difference in high and low for scaling
            diff = max(df['high']) - min(df['low'])
            
            # Calculate the scaled dy and dx
            dx = max(x) - min(x)
            dy = slope * dx * (len(df) / diff)
            
            # Calculate the angle using arctangent
            angle_rad = math.atan2(dy, dx)
            
            # Convert radians to degrees
            angle_deg = math.degrees(angle_rad)
            #angle_deg = abs(angle_deg)
            
            if angle_deg > 90:
                angle_deg = 180-angle_deg
                
            return slope, angle_deg
        srcands=10
        sup = df[df.low == df.low.rolling(srcands, center=True).min()].low
        res = df[df.high == df.high.rolling(srcands, center=True).max()].high
        print(sup,res)
        price_diff = np.mean(df['high'] - df['low']) / 2
        pat = []
        max_bar_diff = 50
        min_bar_diff = 0
        i = 1
        j = 0
        flag = 1

        while i < sup.size and j < res.size:
            if flag == 0 and i < sup.size:
                if sup.index[i] > pat[0]:
                    pat.append(sup.index[i])
                    flag = 1
                i += 1
            else:
                if len(pat) == 0 or res.index[j] > pat[len(pat) - 1]:
                    pat.append(res.index[j])
                    flag = 0
                else:
                    pat.pop(0)
                    pat.insert(0, res.index[j])
                j += 1

            if len(pat) == 3 and pat[2] - pat[0] <= max_bar_diff and pat[2] - pat[1] >= min_bar_diff and pat[1] - pat[0] >= min_bar_diff and abs(res.iloc[j - 2] - res.iloc[j - 1]) <= price_diff:
                # Check if the last ten candles before the first pivot high are generally moving upwards
                start_index = max(0, pat[0] - 20)  # Ensure start_index is at least 0
                end_index = pat[0]

                # Check if the overall trend is upwards
                if 'true':
                    # Linear regression between first top and middle bottom
                    y1 = df['low'].loc[pat[0]:pat[1]].values
                    x1 = np.arange(len(y1)).reshape(-1, 1)
                    slope1, angle1 = calculate_slope_angle(x1, y1)

                    # Linear regression between middle bottom and second top
                    y2 = df['high'].loc[pat[1]:pat[2]].values
                    x2 = np.arange(len(y2)).reshape(-1, 1)
                    slope2, angle2 = calculate_slope_angle(x2, y2)

                    if angle1 < -65 and angle2 > 65:
                        fig.add_shape(type='line', x0=df['date'][pat[0]], y0=res.iloc[j - 2],
                                    x1=df['date'][pat[2]], y1=res.iloc[j - 1])
                        print(pat, "test", angle1, angle2)

            if len(pat) == 3:
                pat.pop(0)
                pat.pop(0)
        # sup = df[df.low == df.low.rolling(srcands, center=True).min()].low
        # filtered_supports_indices = []
        # for idx, support in sup.items():
        #     left_avg_fall = np.mean(
        #         abs(df.low.iloc[idx - int(srcands/2):idx] - support))/support
        #     right_avg_fall = np.mean(
        #         abs(df.low.iloc[idx:idx + int(srcands/2)] - support))/support

        # # If both left and right average falls are greater than the threshold, keep the support
        #     if left_avg_fall > th and right_avg_fall > th:
        #         filtered_supports_indices.append(idx)

        # sup = df.iloc[filtered_supports_indices].low
        # res = df[df.high == df.high.rolling(srcands, center=True).max()].high
        # filtered_indices = []
        # for idx, resis in res.items():
        #     left_avg_fall = np.mean(
        #         abs(df.high.iloc[idx - int(srcands/2):idx] - resis))/resis
        #     right_avg_fall = np.mean(
        #         abs(df.high.iloc[idx:idx + int(srcands/2)] - resis))/resis

        # # If both left and right average falls are greater than the threshold, keep the support
        #     if left_avg_fall > th and right_avg_fall > th:
        #         filtered_indices.append(idx)

        # res = df.iloc[filtered_indices].high
        # price_diff = np.mean(df['high'] - df['low'])/2
        # pat = []
        # max_bar_diff = 50
        # min_bar_diff = 7
        # i = 1
        # j = 0
        # flag = 1
        # while i <= sup.size and j < res.size:
        #     if flag == 0 and i < sup.size:
        #         if sup.index[i] > pat[0]:
        #             pat.append(sup.index[i])
        #             flag = 1
        #         i += 1
        #     else:
        #         if len(pat) == 0 or res.index[j] > pat[len(pat)-1]:
        #             pat.append(res.index[j])
        #             flag = 0
        #         else:
        #             pat.pop(0)
        #             pat.insert(0, res.index[j])
        #         j += 1
        #     if len(pat) == 3 and pat[2]-pat[0] <= max_bar_diff and pat[2]-pat[1] >= min_bar_diff and pat[1]-pat[0] >= min_bar_diff and abs(res.iloc[j-2]-res.iloc[j-1]) <= price_diff:
        #         fig.add_shape(type='line', x0=df['date'][pat[0]], y0=res.iloc[j-2],
        #                       x1=df['date'][pat[2]],
        #                       y1=res.iloc[j-1]
        #                       )
        #     if len(pat) == 3:
        #         pat.pop(0)
        #         pat.pop(0)
    if dbottom == 'true':
        def calculate_slope_angle(x, y):
            # Fit a linear regression model
            model = LinearRegression().fit(x.reshape(-1, 1), y)
            
            # Get the slope from the linear regression model
            slope = model.coef_[0]
            
            # Calculate the difference in high and low for scaling
            diff = max(df['high']) - min(df['low'])
            
            # Calculate the scaled dy and dx
            dx = max(x) - min(x)
            dy = slope * dx * (len(df) / diff)
            
            # Calculate the angle using arctangent
            angle_rad = math.atan2(dy, dx)
            
            # Convert radians to degrees
            angle_deg = math.degrees(angle_rad)
            #angle_deg = abs(angle_deg)
            
            if angle_deg > 90:
                angle_deg = 180-angle_deg
                
            return slope, angle_deg

        srcands = 10
        sup = df[df.low == df.low.rolling(srcands, center=True).min()].low
        res = df[df.high == df.high.rolling(srcands, center=True).max()].high
        print(sup, res)
        price_diff = np.mean(df['high'] - df['low']) / 2
        pat = []
        max_bar_diff = 50
        min_bar_diff = 0
        i = 1
        j = 0
        flag = 1

        while i < sup.size and j < res.size:
            if flag == 1 and i < sup.size:
                if sup.index[i] > pat[0] if pat else True:
                    pat.append(sup.index[i])
                    flag = 0
                i += 1
            else:
                if len(pat) == 0 or res.index[j] > pat[len(pat) - 1]:
                    pat.append(res.index[j])
                    flag = 1
                else:
                    pat.pop(0)
                    pat.insert(0, res.index[j])
                j += 1

            if len(pat) == 3 and pat[2] - pat[0] <= max_bar_diff and pat[2] - pat[1] >= min_bar_diff and pat[1] - pat[0] >= min_bar_diff and abs(sup.iloc[i - 2] - sup.iloc[i - 1]) <= price_diff:
                # Check if the last ten candles before the first pivot low are generally moving downwards
                start_index = max(0, pat[0] - 20)  # Ensure start_index is at least 0
                end_index = pat[0]

                # Check if the overall trend is downwards
                if 'true':
                    # Linear regression between first bottom and middle top
                    y1 = df['high'].loc[pat[0]:pat[1]].values
                    x1 = np.arange(len(y1)).reshape(-1, 1)
                    slope1, angle1 = calculate_slope_angle(x1, y1)

                    # Linear regression between middle top and second bottom
                    y2 = df['low'].loc[pat[1]:pat[2]].values
                    x2 = np.arange(len(y2)).reshape(-1, 1)
                    slope2, angle2 = calculate_slope_angle(x2, y2)

                    if angle1 > 65 and angle2 < -65:
                        fig.add_shape(type='line', x0=df['date'][pat[0]], y0=sup.iloc[i - 2],
                                    x1=df['date'][pat[2]], y1=sup.iloc[i - 1])
                        print(pat, "test", angle1, angle2)

            if len(pat) == 3:
                pat.pop(0)
                pat.pop(0)

        
    if ttop == 'true':
        def calculate_slope_angle(x, y):
            # Fit a linear regression model
            model = LinearRegression().fit(x.reshape(-1, 1), y)
            
            # Get the slope from the linear regression model
            slope = model.coef_[0]
            
            # Calculate the difference in high and low for scaling
            diff = max(df['high']) - min(df['low'])
            
            # Calculate the scaled dy and dx
            dx = max(x) - min(x)
            dy = slope * dx * (len(df) / diff)
            
            # Calculate the angle using arctangent
            angle_rad = math.atan2(dy, dx)
            
            # Convert radians to degrees
            angle_deg = math.degrees(angle_rad)
            #angle_deg = abs(angle_deg)
            
            if angle_deg > 90:
                angle_deg = 180-angle_deg
                
            return slope, angle_deg
        srcands = 10
        sup = df[df.low == df.low.rolling(srcands, center=True).min()].low
        res = df[df.high == df.high.rolling(srcands, center=True).max()].high
        price_diff = np.mean(df['high'] - df['low']) / 2
        pat = []
        max_bar_diff = 50
        min_bar_diff = 0
        i = 1
        j = 0
        flag = 1

        while i < sup.size and j < res.size:
            if flag == 0 and i < sup.size:
                if sup.index[i] > pat[0]:
                    pat.append(sup.index[i])
                    flag = 1
                i += 1
            else:
                if len(pat) == 0 or res.index[j] > pat[len(pat) - 1]:
                    pat.append(res.index[j])
                    flag = 0
                else:
                    pat.pop(0)
                    pat.insert(0, res.index[j])
                j += 1

            if len(pat) == 4 and pat[3] - pat[0] <= max_bar_diff and pat[3] - pat[2] >= min_bar_diff and pat[2] - pat[1] >= min_bar_diff and pat[1] - pat[0] >= min_bar_diff and abs(res.iloc[j - 2] - res.iloc[j - 1]) <= price_diff:
                start_index = max(0, pat[0] - 20)
                end_index = pat[0]
                if 'true':
                    y1 = df['low'].loc[pat[0]:pat[1]].values
                    x1 = np.arange(len(y1)).reshape(-1, 1)
                    slope1, angle1 = calculate_slope_angle(x1, y1)
                    y2 = df['high'].loc[pat[1]:pat[2]].values
                    x2 = np.arange(len(y2)).reshape(-1, 1)
                    slope2, angle2 = calculate_slope_angle(x2, y2)
                    y3 = df['high'].loc[pat[2]:pat[3]].values
                    x3 = np.arange(len(y3)).reshape(-1, 1)
                    slope3, angle3 = calculate_slope_angle(x3, y3)
                    if angle1 < -65 and angle2 > 65 and angle3 > 65:
                        fig.add_shape(type='line', x0=df['date'][pat[0]], y0=res.iloc[j - 2],
                                    x1=df['date'][pat[3]], y1=res.iloc[j - 1])
                        print(pat, "test", angle1, angle2, angle3)

            if len(pat) == 4:
                pat.pop(0)
                pat.pop(0)

    if tbottom == 'true':

        def calculate_slope_angle(x, y):
            # Fit a linear regression model
            model = LinearRegression().fit(x.reshape(-1, 1), y)
            
            # Get the slope from the linear regression model
            slope = model.coef_[0]
            
            # Calculate the difference in high and low for scaling
            diff = max(df['high']) - min(df['low'])
            
            # Calculate the scaled dy and dx
            dx = max(x) - min(x)
            dy = slope * dx * (len(df) / diff)
            
            # Calculate the angle using arctangent
            angle_rad = math.atan2(dy, dx)
            
            # Convert radians to degrees
            angle_deg = math.degrees(angle_rad)
            #angle_deg = abs(angle_deg)
            
            if angle_deg > 90:
                angle_deg = 180-angle_deg
                
            return slope, angle_deg
        srcands = 10
        sup = df[df.low == df.low.rolling(srcands, center=True).min()].low
        res = df[df.high == df.high.rolling(srcands, center=True).max()].high
        price_diff = np.mean(df['high'] - df['low']) / 2
        pat = []
        max_bar_diff = 50
        min_bar_diff = 0
        i = 1
        j = 0
        flag = 1

        while i < sup.size and j < res.size:
            if flag == 1 and i < sup.size:
                if sup.index[i] > pat[0] if pat else True:
                    pat.append(sup.index[i])
                    flag = 0
                i += 1
            else:
                if len(pat) == 0 or res.index[j] > pat[len(pat) - 1]:
                    pat.append(res.index[j])
                    flag = 1
                else:
                    pat.pop(0)
                    pat.insert(0, res.index[j])
                j += 1

            if len(pat) == 4 and pat[3] - pat[0] <= max_bar_diff and pat[3] - pat[2] >= min_bar_diff and pat[2] - pat[1] >= min_bar_diff and pat[1] - pat[0] >= min_bar_diff and abs(sup.iloc[i - 2] - sup.iloc[i - 1]) <= price_diff:
                start_index = max(0, pat[0] - 20)
                end_index = pat[0]
                if 'true':
                    y1 = df['high'].loc[pat[0]:pat[1]].values
                    x1 = np.arange(len(y1)).reshape(-1, 1)
                    slope1, angle1 = calculate_slope_angle(x1, y1)
                    y2 = df['low'].loc[pat[1]:pat[2]].values
                    x2 = np.arange(len(y2)).reshape(-1, 1)
                    slope2, angle2 = calculate_slope_angle(x2, y2)
                    y3 = df['low'].loc[pat[2]:pat[3]].values
                    x3 = np.arange(len(y3)).reshape(-1, 1)
                    slope3, angle3 = calculate_slope_angle(x3, y3)
                    if angle1 > 65 and angle2 < -65 and angle3 < -65:
                        fig.add_shape(type='line', x0=df['date'][pat[0]], y0=sup.iloc[i - 2],
                                    x1=df['date'][pat[3]], y1=sup.iloc[i - 1])
                        print(pat, "test", angle1, angle2, angle3)

            if len(pat) == 4:
                pat.pop(0)
                pat.pop(0)

                
    if ibars == 'true':
        ibs = pd.Series()
        ibp = pd.Series()
        def cal_len(i):
            body_len = abs(df['open'][i] - df['close'][i])
            wick_len = df['high'][i] - df['low'][i] - body_len
            if body_len > 2 * wick_len :
                return 1
            return 0
        for cid in range(2,len(df)-2):
            if cid == 0:
                continue
            l1 = min(df['open'][cid], df['close'][cid])
            l2 = min(df['open'][cid-1], df['close'][cid-1])
            u1 = max(df['open'][cid], df['close'][cid])
            u2 = max(df['open'][cid-1], df['close'][cid-1])
            is_rc1 = True if df['open'][cid-1] < df['close'][cid-1] else False
            is_rc2 = True if df['open'][cid-2] < df['close'][cid-2] else False
            is_gc1 = True if df['open'][cid] > df['close'][cid] else False
            pcl1 = cal_len(cid-1)
            pcl2 = cal_len(cid-2)
            if l2 < l1 and u2 > u1 and df['high'][cid-1] > df['high'][cid] and df['low'][cid-1] < df['low'][cid] and((is_rc1 and is_rc2 and is_gc1) or (not is_rc1 and not is_rc2 and not is_gc1)) and pcl1 == 1 and pcl2 == 1 :
                ibs.loc[len(ibs)] = df['date'][cid]
                ibp.loc[len(ibp)] = df['high'][cid]
        fig.add_trace(go.Scatter(
            x=ibs,
            # Adjust y-axis based on your needs
            y=ibp+np.mean(df['high'] - df['low'])/2,
            mode='markers',
            marker=dict(size=5, color='black', symbol='circle')
        ))
    if ema5=='true':
        ac=0
        acs=pd.Series()
        hs=pd.Series()
        f=0
        pac=0
        df["EMA5"] = ta.ema(df["close"], length=5)

        for cid in df.index:
            if cid<4:
                continue
            down=df['close'][cid] if df['close'][cid]<df['open'][cid] else df['open'][cid]
            pdo=df['close'][cid-1] if df['close'][cid-1]<df['open'][cid-1] else df['open'][cid-1]
            if df['low'][cid]>=df['EMA5'][cid] or (f==1 and down>df['EMA5'][cid]):
                if ac==cid-1:
                    f=1
                    if pdo>down  and (len(acs)==0 or cid-pac>5):
                        acs.loc[len(acs)]=df['date'][cid]
                        hs.loc[len(hs)]=df['high'][cid]
                        ac=0
                        pac=cid
                        f=0
                        continue
                ac=cid  
        fig.add_trace(go.Scatter(
            x=acs,
            y=hs+np.mean(df['high'] - df['low'])/2,  # Adjust y-axis based on your needs
            mode='markers',
            marker=dict(size=5, color='blue', symbol='circle')  # Customize marker appearance
        ))
    if box=='true':
        sup = df[df.low == df.low.rolling(nbc, center=True).min()].low
        res = df[df.high == df.high.rolling(nbc, center=True).max()].high
        top = res.iloc[0]
        bot = sup.iloc[0]
        bi=sup.index[0]
        ti=res.index[0]
        box={ti:top,bi:bot}
        fbox=[]
        support_iter = iter(sup.items())
        resistance_iter = iter(res.items())
        next(support_iter, None)
        next(resistance_iter, None)
        f=0
        fboxes=[]
        next_support_index, next_support_price = next(support_iter)
        next_resistance_index, next_resistance_price = next(resistance_iter)
        while True:
            tolerance=(top-bot)/bth
            if next_support_index is None or next_resistance_index is None:
                break
            if next_support_price > bot + tolerance or next_support_price < bot - tolerance:
                bot = next_support_price
                bi = next_support_index
                if len(box)>4:
                    f=1
                    fbox=box
                    box={bi:bot}
                else:
                    box={ti:top,bi:bot}
            else:
                box[next_support_index]=next_support_price
            if next_resistance_price > top  + tolerance or next_resistance_price < top  - tolerance:
                top = next_resistance_price
                ti = next_resistance_index
                if len(box)>4:
                    f=1
                    fbox=box
                    box={ti:top}
                else:
                    box={ti:top,bi:bot}
            else:
                box[next_resistance_index]=next_resistance_price
            if f==1:
                fboxes.append(fbox)
                f=0
            if next_support_index < next_resistance_index:
                try:
                    next_support_index, next_support_price = next(support_iter)
                except StopIteration:
                    next_support_index = None
            else:
                try:
                    next_resistance_index, next_resistance_price = next(resistance_iter)
                except StopIteration:
                    next_resistance_index = None
        for fbox in fboxes:
            bot = min(fbox.values())
            top = max(fbox.values())
            bi=list(fbox.keys())[list(fbox.values()).index(bot)]
            ti=list(fbox.keys())[list(fbox.values()).index(top)]
            f = 0
            l = min(fbox.keys())
            if bi < ti:
                lp = bot
                r = ti
                rp = top
            else:
                lp = top
                r = bi
                rp = bot
            # while l>0 :
            #     if df['high'][l] > top or df['low'][l] < bot:
            #         print(l,top,bot)
            #         break
            #     l-=1
            while r < len(df)-1:
                if df['high'][r] > top or df['low'][r] < bot:
                    break
                r += 1
            fig.add_shape(
                type="rect",
                xref="x",
                yref="y",
                x0=df['date'][l],
                y0=lp,
                x1=df['date'][r],
                y1=rp,
                fillcolor="rgba(0,100,80,0.2)",
                line=dict(
                    color="rgba(0,100,80,0.7)",
                    width=2,
                )
            )
    if hsind == 'true':
    # Identifying support and resistance levels
        sup = df[df.low == df.low.rolling(24, center=True).min()].low
        res = df[df.high == df.high.rolling(24, center=True).max()].high
        
        sup = sup.to_frame()
        sup.columns = ['price']
        sup['val'] = 1
        
        res = res.to_frame()
        res.columns = ['price']
        res['val'] = 2
        
        lev = sup.combine_first(res)
        
        def hsf(hs):
            data = df['close']
            ls, lb, head, rb, rs = hs
            
            is_normal_hs = df['high'][head] > max(df['high'][ls], df['high'][rs])
            is_inverted_hs = df['low'][head] < min(df['low'][ls], df['low'][rs])
            
            # Determine if it's a valid head and shoulders pattern (normal or inverted)
            if not (is_normal_hs or is_inverted_hs):
                return None
            
            rh = rs - head
            lh = head - ls
            
            # Check head height symmetry
            if rh > 2.5 * lh or lh > 2.5 * rh:
                return None
            
            neck_run = rb - lb
            neck_rise = (df['low'][rb] - df['low'][lb]) if is_normal_hs else (df['high'][rb] - df['high'][lb])
            neck_slope = neck_rise / neck_run
            head_width = rb - lb
            
            pat_start = -1
            pat_end = -1
            
            # Identifying pattern start
            for j in range(1, head_width):
                neck1 = df['low'][lb] + (ls - lb - j) * neck_slope if is_normal_hs else df['high'][lb] + (ls - lb - j) * neck_slope
                if ls - j < 0:
                    return None
                if (df['low'][ls - j] < neck1) if is_normal_hs else (df['high'][ls - j] > neck1):
                    pat_start = ls - j
                    break
            
            # Identifying pattern end
            for j in range(1, head_width):
                neck2 = df['low'][lb] + (rs - lb + j) * neck_slope if is_normal_hs else df['high'][lb] + (rs - lb + j) * neck_slope
                if rs + j > len(df) - 1:
                    return None
                if (df['low'][rs + j] < neck2) if is_normal_hs else (df['high'][rs + j] > neck2):
                    pat_end = rs + j
                    break
            
            if pat_start == -1 or pat_end == -1:
                return None
            
            hs.insert(0, pat_start)
            hs.append(pat_end)
            
            # Plotting the pattern
            f = 0
            for i in range(len(hs)):
                if hs[i] == pat_start:
                    continue
                if f == 0:
                    col1 = 'low' if is_normal_hs else 'high'
                    col2 = 'high' if is_normal_hs else 'low'
                    f = 1
                else:
                    col1 = 'high' if is_normal_hs else 'low'
                    col2 = 'low' if is_normal_hs else 'high'
                    f = 0
                fig.add_shape(type='line', x0=df['date'][hs[i-1]], y0=df[col1][hs[i-1]],
                            x1=df['date'][hs[i]], y1=df[col2][hs[i]],
                            line=dict(color='blue', width=2))
            
            fig.add_shape(type='line', x0=df['date'][hs[0]], y0=df['low'][hs[0]] if is_normal_hs else df['high'][hs[0]],
                        x1=df['date'][hs[-1]], y1=df['low'][hs[-1]] if is_normal_hs else df['high'][hs[-1]],
                        line=dict(color='black', width=2))
        
        c = []
        p = lev.index[0]
        for i in lev.index:
            if not c:
                if lev['val'][i] == 2:
                    c.append(i)
                else:
                    p = i
                    continue
            else:
                if lev['val'][i] != lev['val'][p] and i - p > 3:
                    c.append(i)
                elif lev['val'][i] == 1:
                    c = []
                else:
                    c = [i]
            
            if len(c) == 5:
                if hsf(c):
                    c = []
                else:
                    c = c[2:]
            p = i
            sup = df[df.low == df.low.rolling(24, center=True).min()].low
            res = df[df.high == df.high.rolling(24, center=True).max()].high
            sup = sup.to_frame()
            sup.columns = ['price']
            sup['val'] = 1
            res = res.to_frame()
            res.columns = ['price']
            res['val'] = 2
            lev = sup.combine_first(res)
            def hsf(hs):
                data = df['close']
                ls = hs[0]
                lb = hs[1]
                head = hs[2]
                rb = hs[3]
                rs = hs[4]

                is_normal_hs = df['high'][head] > max(df['high'][ls], df['high'][rs])
                is_inverted_hs = df['low'][head] < min(df['low'][ls], df['low'][rs])
                
                # Determine if it's a valid head and shoulders pattern (normal or inverted)
                if not (is_normal_hs or is_inverted_hs):
                    return None
                
                rh = rs - head
                lh = head - ls
                
                # Check head height symmetry
                if rh > 2.5 * lh or lh > 2.5 * rh:
                    return None
                
                neck_run = rb - lb
                neck_rise = (df['low'][rb] - df['low'][lb]) if is_normal_hs else (df['high'][rb] - df['high'][lb])
                neck_slope = neck_rise / neck_run
                head_width = rb - lb
                
                pat_start = -1
                pat_end = -1
                f1 = 0
                f2 = 0
                
                # Identifying pattern start
                for j in range(1, head_width):
                    neck1 = df['low'][lb] + (ls - lb - j) * neck_slope if is_normal_hs else df['high'][lb] + (ls - lb - j) * neck_slope
                    if ls - j < 0:
                        return None
                    if (df['low'][ls - j] < neck1) if is_normal_hs else (df['high'][ls - j] > neck1):
                        pat_start = ls - j
                        break
                
                # Identifying pattern end
                for j in range(1, head_width):
                    neck2 = df['low'][lb] + (rs - lb + j) * neck_slope if is_normal_hs else df['high'][lb] + (rs - lb + j) * neck_slope
                    if rs + j > len(df) - 1:
                        return None
                    if (df['low'][rs + j] < neck2) if is_normal_hs else (df['high'][rs + j] > neck2):
                        pat_end = rs + j
                        break
                
                if pat_start == -1 or pat_end == -1:
                    return None
                
                hs.insert(0, pat_start)
                hs.append(pat_end)
                
                # Plotting the pattern
                f = 0
                for i in range(len(hs)):
                    if hs[i] == pat_start:
                        continue
                    if f == 0:
                        col1 = 'low' if is_normal_hs else 'high'
                        col2 = 'high' if is_normal_hs else 'low'
                        f = 1
                    else:
                        col1 = 'high' if is_normal_hs else 'low'
                        col2 = 'low' if is_normal_hs else 'high'
                        f = 0
                    fig.add_shape(type='line', x0=df['date'][hs[i-1]], y0=df[col1][hs[i-1]],
                                x1=df['date'][hs[i]], y1=df[col2][hs[i]],
                                line=dict(color='blue', width=2))
                
                fig.add_shape(type='line', x0=df['date'][hs[0]], y0=df['low'][hs[0]] if is_normal_hs else df['high'][hs[0]],
                            x1=df['date'][hs[-1]], y1=df['low'][hs[-1]] if is_normal_hs else df['high'][hs[-1]],
                            line=dict(color='black', width=2))
            c = []
            hs = None
            p = lev.index[0]
            for i in lev.index:
                if not c:
                    if lev['val'][i] == 2:
                        c.append(i)
                    else:
                        p = i
                        continue
                else:
                    if lev['val'][i] != lev['val'][p] and i - p > 3:
                        c.append(i)
                    elif lev['val'][i] == 1:
                        c = []
                    else:
                        c = [i]
                if len(c) == 5:
                    if hsf(c):
                        c = []
                    else:
                        c = c[2:]
                p = i


    
    if vshape == 'true' :
        def calculate_slope_angle(x, y):
            model = LinearRegression().fit(x, y)
            slope = model.coef_[0]
            angle_deg = math.degrees(math.atan(slope))
            return slope, angle_deg

        def find_v_shapes(df, lookback):
            v_shapes = []
            for i in range(lookback, len(df) - lookback):
                # Normal V-shape
                left = df['low'][i - lookback:i]
                right = df['low'][i + 1:i + lookback + 1]
                if df['low'][i] < left.min() and df['low'][i] < right.min():
                    v_shapes.append((i - lookback, i, i + lookback, 'normal'))

                # Upside-down V-shape
                left = df['high'][i - lookback:i]
                right = df['high'][i + 1:i + lookback + 1]
                if df['high'][i] > left.max() and df['high'][i] > right.max():
                    v_shapes.append((i - lookback, i, i + lookback, 'upside_down'))
            return v_shapes

        lookback = 10
        v_shapes = find_v_shapes(df, lookback)

        # Filter V-shapes based on slope angles and candle lengths
        filtered_v_shapes = []
        for left_idx, mid_idx, right_idx, v_type in v_shapes:
            if v_type == 'normal':
                # Slope before the pivot
                y1 = df['low'].iloc[left_idx:mid_idx + 1].values
                x1 = np.arange(len(y1)).reshape(-1, 1)
                slope1, angle1 = calculate_slope_angle(x1, y1)

                # Slope after the pivot
                y2 = df['low'].iloc[mid_idx:right_idx + 1].values
                x2 = np.arange(len(y2)).reshape(-1, 1)
                slope2, angle2 = calculate_slope_angle(x2, y2)

                # Length of the candles
                candle_lengths_before = df['high'].iloc[left_idx:mid_idx + 1] - df['low'].iloc[left_idx:mid_idx + 1]
                candle_lengths_after = df['high'].iloc[mid_idx:right_idx + 1] - df['low'].iloc[mid_idx:right_idx + 1]

                # Filter by angles and candle lengths
                if angle1 < -70 and angle2 > 70 and candle_lengths_before.mean() > price_diff and candle_lengths_after.mean() > price_diff:
                    filtered_v_shapes.append((left_idx, mid_idx, right_idx, v_type))
                    print(angle1, angle2, candle_lengths_before.mean(), candle_lengths_after.mean())

            elif v_type == 'upside_down':
                # Slope before the pivot
                y1 = df['high'].iloc[left_idx:mid_idx + 1].values
                x1 = np.arange(len(y1)).reshape(-1, 1)
                slope1, angle1 = calculate_slope_angle(x1, y1)

                # Slope after the pivot
                y2 = df['high'].iloc[mid_idx:right_idx + 1].values
                x2 = np.arange(len(y2)).reshape(-1, 1)
                slope2, angle2 = calculate_slope_angle(x2, y2)

                # Length of the candles
                candle_lengths_before = df['high'].iloc[left_idx:mid_idx + 1] - df['low'].iloc[left_idx:mid_idx + 1]
                candle_lengths_after = df['high'].iloc[mid_idx:right_idx + 1] - df['low'].iloc[mid_idx:right_idx + 1]

                # Filter by angles and candle lengths
                if angle1 > 70 and angle2 < -70 and candle_lengths_before.mean() > price_diff and candle_lengths_after.mean() > price_diff::
                    filtered_v_shapes.append((left_idx, mid_idx, right_idx, v_type))
                    print(angle1, angle2, candle_lengths_before.mean(), candle_lengths_after.mean())

        for left_idx, mid_idx, right_idx, v_type in filtered_v_shapes:
            if v_type == 'normal':
                fig.add_shape(type='line', x0=df['date'][left_idx], y0=df['low'][left_idx],
                              x1=df['date'][mid_idx], y1=df['low'][mid_idx],
                              line=dict(color='blue', width=2))
                fig.add_shape(type='line', x0=df['date'][mid_idx], y0=df['low'][mid_idx],
                              x1=df['date'][right_idx], y1=df['low'][right_idx],
                              line=dict(color='blue', width=2))
            elif v_type == 'upside_down':
                fig.add_shape(type='line', x0=df['date'][left_idx], y0=df['high'][left_idx],
                              x1=df['date'][mid_idx], y1=df['high'][mid_idx],
                              line=dict(color='red', width=2))
                fig.add_shape(type='line', x0=df['date'][mid_idx], y0=df['high'][mid_idx],
                              x1=df['date'][right_idx], y1=df['high'][right_idx],
                              line=dict(color='red', width=2))
   
    if mestar == 'true' :
        def cal_len(i):
            body_len = abs(df['open'][i] - df['close'][i])
            wick_len = df['high'][i] - df['low'][i] - body_len
            if body_len > 3 * wick_len :
                return 1
            elif wick_len > 3 * body_len :
                return 0
            return -1
        msc = pd.Series()
        msp = pd.Series()
        for i in range(2,len(df)-2):
            is_rc1 = True if df['open'][i-1] < df['close'][i-1] else False
            is_gc1 = True if df['open'][i] > df['close'][i] else False
            is_gc2 = True if df['open'][i+1] > df['close'][i+1] else False
            if (is_rc1  and is_gc1 and is_gc2) or (not is_rc1 and not is_gc1 and not is_gc2) :
                pcl1 = cal_len(i-1)
                cl = cal_len(i)
                acl = cal_len(i+1)
                if pcl1 == 1 and cl == 0 and acl == 1:
                    msc.loc[len(msc)] = df['date'][i]
                    msp.loc[len(msp)] = df['high'][i]
        fig.add_trace(go.Scatter(
            x=msc,
            y=msp+np.mean(df['high'] - df['low'])/2,  # Adjust y-axis based on your needs
            mode='markers',
            marker=dict(size=5, color='yellow', symbol='circle')  # Customize marker appearance
        ))
    con.close()
    return fig

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**db_config4)
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(query, data=None):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        if data:
            cursor.executemany(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()

def fetch_existing_data(table_name):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    existing_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return existing_data

def get_livemint_data():
    url = "https://www.livemint.com/market/quarterly-results-calendar"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    headers = ["stocks", "result_date", "purpose"]
    rows = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        cells_text = [cell.text.strip() for cell in cells]
        rows.append(cells_text)

    df = pd.DataFrame(rows, columns=headers)

    def parse_result_date(date_str):
        try:
            return pd.to_datetime(date_str, format='%d %b %Y').strftime('%Y-%m-%d')
        except ValueError:
            return None

    df['result_date'] = df['result_date'].apply(parse_result_date)
    df = df.dropna(subset=['result_date'])

    return df

def get_usi_data():
    url = "https://www.usinflationcalculator.com/inflation/consumer-price-index-release-schedule/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.select('tbody > tr')
    headers = ["release_date", "release_time"]
    data = []
    for row in rows:
        cells = [cell.text.strip() for cell in row.find_all('td')]
        data.append(cells[1:3])  # Skip the month column and fetch only release_date and release_time

    df = pd.DataFrame(data, columns=headers)

    def parse_release_date(date_str):
        if not date_str:
            return None
        try:
            return pd.to_datetime(date_str, format='%b. %d, %Y').strftime('%Y-%m-%d')
        except ValueError:
            try:
                return pd.to_datetime(date_str, format='%b %d, %Y').strftime('%Y-%m-%d')
            except ValueError:
                return None

    df['release_date'] = df['release_date'].apply(parse_release_date)
    df = df.dropna(subset=['release_date'])

    return df

def store_data(df, table_name):
    existing_data = fetch_existing_data(table_name)
    existing_rows = set([tuple(row[1:]) for row in existing_data])  # Exclude the id column

    new_data = [tuple(row) for row in df.values]
    new_rows = [row for row in new_data if row not in existing_rows]

    if new_rows:
        placeholders = ", ".join(["%s"] * len(df.columns))
        columns = ", ".join(df.columns)
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        execute_query(query, new_rows)

def fetch_data_for_current_month():
    current_month = datetime.now().month
    current_year = datetime.now().year

    connection = create_connection()
    cursor = connection.cursor()

    # Fetch LiveMint data for the current month
    query_livemint = """
    SELECT stocks, DATE_FORMAT(result_date, '%Y-%m-%d') as result_date, purpose
    FROM livemint_data
    WHERE MONTH(result_date) = %s AND YEAR(result_date) = %s
    ORDER BY result_date;
    """
    cursor.execute(query_livemint, (current_month, current_year))
    livemint_data = cursor.fetchall()
    livemint_df = pd.DataFrame(livemint_data, columns=["stocks", "result_date", "purpose"])

    # Fetch USI data for the current month
    query_usi = """
    SELECT DATE_FORMAT(release_date, '%Y-%m-%d') as release_date, release_time
    FROM usi_data
    WHERE MONTH(release_date) = %s AND YEAR(release_date) = %s
    ORDER BY release_date;
    """
    cursor.execute(query_usi, (current_month, current_year))
    usi_data = cursor.fetchall()
    usi_df = pd.DataFrame(usi_data, columns=["release_date", "release_time"])

    cursor.close()
    connection.close()

    return livemint_df, usi_df

@app.route('/news')
def news_page():
    livemint_df = get_livemint_data()
    usi_df = get_usi_data()

    # Store data in the database
    store_data(livemint_df, 'livemint_data')
    store_data(usi_df, 'usi_data')

    # Fetch data for the current month
    livemint_df, usi_df = fetch_data_for_current_month()

    # Convert DataFrames to HTML tables
    livemint_html = livemint_df.to_html(classes='data', index=False)
    usi_html = usi_df.to_html(classes='data', index=False)

    return render_template('news.html',
                           livemint_data=livemint_html,
                           usi_data=usi_html)


def fetch_data_from_db(symbol, interval):

    con = mysql.connector.connect(**db_config3)
    cur = con.cursor()
    sym = symbol
    parts = sym.split(':')[-1].replace('-', '_').replace('&', '_')
    sym = parts.lower()
    
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'stocks'")
    tables = cur.fetchall()
    tables = [table[0] for table in tables]
    if sym not in tables or interval == '1' or interval == '3':
        return []
    # Example SQL query (adjust as per your schema)
    query = f"""
        SELECT t.INTERVAL_START AS `Interval`, t.`Open`, t.`High`, t.`Low`, ae.`Close`, t.`Volume`
        FROM (
            SELECT 
                (UNIX_TIMESTAMP(`date`) - (UNIX_TIMESTAMP(DATE_FORMAT(`date`, '%Y-%m-%d 09:15:00')))) DIV ({interval} * 60) + UNIX_TIMESTAMP(DATE_FORMAT(`date`, '%Y-%m-%d 09:15:00')) AS interval_id,
                MIN(`date`) AS INTERVAL_START,
                `open` AS `Open`,
                MAX(`high`) AS `High`,
                MIN(`low`) AS `Low`,
                MAX(`date`) AS max_date,
                SUM(`volume`) AS `Volume`
            FROM {sym}
            GROUP BY interval_id
            ORDER BY max_date DESC
            LIMIT 5000  
        ) AS t
        INNER JOIN {sym} ae ON ae.`date` = t.max_date
        ORDER BY t.max_date ASC;
            """
    cur.execute(query)
    rows = cur.fetchall()
    seen = set()
    data = []
    for row in rows:
        row_data = {
            'Date': row[0].strftime('%Y-%m-%d %H:%M:%S'),  
            'Open': row[1],
            'High': row[2],
            'Low': row[3],
            'Close': row[4]
        }
        row_tuple = tuple(row_data.items())  # Convert dict to tuple for hashable set
        if row_tuple not in seen:
            seen.add(row_tuple)
            data.append(row_data)

    con.close()
    return data

def fetch_latest_data(symbol):
    con = mysql.connector.connect(**db_config3)
    cur = con.cursor()
    sym = symbol.split(':')[-1].replace('-', '_').replace('&', '_').lower()
    query = f"""
        SELECT `date`, `close`
        FROM {sym}
        ORDER BY `date` DESC
        LIMIT 2
    """
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
    return rows

dtime_datetime = dt.datetime.now()
dtime = dtime_datetime.strftime("%Y-%m-%d")

def fetch_currentday_data(symbol, interval):
    
    data = {
            "symbol": symbol,
            "resolution": '5S',
            "date_format": "1",
            "range_from": dtime,
            "range_to": dtime,
            "cont_flag": "1"
        }
    df = fyers.history(data=data)
    if 'candles' not in df:
        return []
    df = pd.DataFrame(df['candles'])
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df.date = (df.date.dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata'))
    df['date'] = df['date'].dt.tz_localize(None)
    df_sorted = df.sort_values(by=['date'], ascending=True)
    df = df_sorted.drop_duplicates(subset='date', keep='first')
    df.reset_index(drop=True, inplace=True)
    df['group'] = (df.index // (int(interval)*12))
    df2 = df.groupby('group').agg({
        'date': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last'
    }).reset_index(drop=True)
    df2['date'] = df2['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data2 = df2.rename(columns={
        'date': 'Date',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close'
    }).to_dict(orient='records')
    return data2

@app.route('/')
def index():
    return render_template('home.html')
    
def insert_user(user_data):
    conn = mysql.connector.connect(**db_config2)
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO users (name, lastname, mailid, phone, learning, experience, capital, password, user_type)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, user_data)
    conn.commit()
    cursor.close()
    conn.close()


def check_user_credentials(email, password):
    conn = mysql.connector.connect(**db_config2)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE mailid = %s AND password = %s AND user_type = 'admin'"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def compare_db_current_date(symbol):
    con = mysql.connector.connect(**db_config3)
    cur = con.cursor()
    sym = symbol
    parts = sym.split(':')[-1].replace('-', '_').replace('&', '_')
    sym = parts.lower()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'stocks'")
    tables = cur.fetchall()
    tables = [table[0] for table in tables]
    if sym not in tables :
        return True
    cur.execute(f"SELECT MAX(`date`) FROM {sym}")
    ltime = cur.fetchall()
    ltime = ltime[0][0].strftime('%Y-%m-%d')
    if dtime > ltime :
        return True
    return False

def is_email_registered(email):
    conn = mysql.connector.connect(**db_config2)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE mailid = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = check_user_credentials(email, password)
        if user:
            session['email'] = email  # Store the email in session
            # Assuming the user_type is the 9th field in the user tuple
            session['user_type'] = user[8]
            return redirect(url_for('graph'))
        else:
            return render_template('login.html', login_status=0)
    return render_template('login.html', login_status=-1)


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['mailid']
        if is_email_registered(email):
            return render_template('signup.html', email_exists=True)
        user_data = (
            request.form['name'],
            request.form['lastname'],
            email,
            request.form['phone'],
            request.form['learning'],
            request.form['experience'],
            request.form['capital'],
            request.form['password'],
            'user'  # Default user type
        )
        insert_user(user_data)
        return redirect(url_for('login'))
    return render_template('signup.html', email_exists=False)


@app.route('/old-graph')
def old_graph():
    if 'email' in session:
        symbol = "NSE:ASIANPAINT-EQ"
        start_date = "2024-03-01"
        end_date = "2024-05-06"
        interval = "15"
        graph = generate_graph(symbol, start_date, end_date,
                               interval, 'false', 20, 'false', 5, 'false', 'false', 20, 1, 'false', 'false', 'false', 5, 20, 'false', 'false', 'false')
        return render_template('index.html', graph=json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder), time_intervals=time_intervals, end_date=end_date)
    return redirect(url_for('login'))


@app.route('/update_graph', methods=['POST'])
def update_graph():
    role = session.get('role')

    # Allow only specific parameters for limited users
    if role == 'limited':
        symbol = request.form['watchlist-stocks']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        interval = request.form['interval']
        sr_visible = request.form['srVisible']
        nsr = request.form['nsr']
        if not nsr:
            nsr = 0
        trline = request.form['trVisible']
        graph = generate_graph(symbol, start_date, end_date, interval, 'false', 20, sr_visible, nsr, trline, 'false','false', 'false', 'false', 20, 1, 'false', 'false', 'false', 5, 'false', 'false', 'false', 'false')
    else:
        symbol = request.form['watchlist-stocks']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        interval = request.form['interval']
        ema_visible = request.form['emaVisible']
        sr_visible = request.form['srVisible']
        nsr = request.form['nsr']
        if not nsr:
            nsr = 0
        trline = request.form['trVisible']
        dtop = request.form['dtop']
        dbottom = request.form['dbottom']
        ttop = request.form['ttop']
        tbottom = request.form['tbottom']
        ndt = int(request.form['ndt'])
        th = float(request.form['thr'])
        ibars = request.form['ibars']
        emaval = int(request.form['emaval'])
        ema5 = request.form['ema5']
        box = request.form['box']
        bth = int(request.form['bth'])
        nbc = int(request.form['nbc'])
        hsind = request.form['hsind']
        vshape = request.form['vshape']
        mestar = request.form['mestar']
        graph = generate_graph(symbol, start_date, end_date,
                               interval, ema_visible,emaval, sr_visible, nsr, trline, dtop, dbottom, ttop, tbottom, ndt, th, ibars, ema5,box,bth,nbc,hsind,vshape,mestar)
    return json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/submit_stock', methods=['POST'])
def submit_stock():
    new_stock_input = request.json.get('newStockInput')
    try :
        data = {
        "symbol": new_stock_input,
        "resolution": "5",
        "date_format": "1",
        "range_from": "2024-07-03",
        "range_to": "2024-07-03",
        "cont_flag": "1"
        }
        df = pd.DataFrame(fyers.history(data=data)['candles'])
        return jsonify({'status': 1})
    except KeyError:
        return jsonify({'status': 0})

@app.route('/get_50_stocks', methods=['GET'])
def get_50_stocks():
    stocks_50 = read_stocks_from_file()
    return jsonify(stocks_50)

    
@app.route('/graph')
def graph():
    if 'email' in session:
        return render_template('graph.html')
    return redirect(url_for('login'))
    
@app.route('/stock-data')
def get_data():
    symbol = request.args.get('symbol', 'NSE:NIFTY50-INDEX')
    interval = request.args.get('interval', '5')
    # Fetch data from database
    data1 = fetch_data_from_db(symbol, interval)
    if compare_db_current_date(symbol):
        data2 = fetch_currentday_data(symbol, interval)
    else:
        data2 = []
    data = data1 + data2
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Data not found'}), 404
    

def calculate_sr_lines(df, prd, nsr):
    sup = df[df.low == df.low.rolling(prd, center=True).min()].low
    res = df[df.high == df.high.rolling(prd, center=True).max()].high
    lev = sup.tolist() + res.tolist()
    lev.sort()
    kmeans = KMeans(n_clusters=int(nsr), random_state=42).fit(
        np.array(lev).reshape(-1, 1))
    lset = []
    for cluster_center in kmeans.cluster_centers_:
        closest_index = np.argmin(np.abs(lev - cluster_center))
        lset.append(lev[closest_index])
    return lset

@app.route('/support-resistance')
def get_support_resistance():
    symbol = request.args.get('symbol', 'NSE:NIFTY50-INDEX')
    interval = request.args.get('interval', '5')

    data = fetch_data_from_db(symbol, interval)

    df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close'])
    df.columns = ['date', 'open', 'high', 'low', 'close']
    df['date'] = pd.to_datetime(df['date'])
    
    prd = 30  
    nsr = 13
    groups = 1
    group_size = 5100
    
    sr_lines_groups = []
    for i in range(groups):
        group_df = df.iloc[i*group_size:(i+1)*group_size]
        sr_lines = calculate_sr_lines(group_df, prd, nsr)
        sr_lines_groups.append({
            "start_date": group_df['date'].iloc[0].strftime('%Y-%m-%d %H:%M:%S'),
            "end_date": group_df['date'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S'),
            "sr_lines": sr_lines
        })
    
    return jsonify(sr_lines_groups)# This line retrieves the WSGI application instance
application = app.wsgi_app

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
