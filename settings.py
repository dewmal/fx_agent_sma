xmpp_host = "127.0.0.1"
app_id = 1089
binary_api_end_point = f'wss://ws.binaryws.com/websockets/v3?app_id={app_id}'

# stock_indexes = [
#     {
#         "name": "EUR_USD",
#         "api_name": "R_50",
#         "symbol": "EURUSD"
#     }
# ]
stock_indexes = [
    {
        "name": "EUR_USD",
        "api_name": "frxEURUSD",
        "symbol": "EURUSD"
    },
    {
        "name": "USD_JPY",
        "api_name": "frxUSDJPY",
        "symbol": "USDJPY"
    },
    {
        "name": "AUD_JPY",
        "api_name": "frxAUDJPY",
        "symbol": "AUDJPY"
    },
    {
        "name": "EUR_CAD",
        "api_name": "frxEURCAD",
        "symbol": "EURCAD"
    }
]

users = {
    "oracle": {
        "name": "oracle",
        "description": "History recode manager stock market",
        "username": "orcale",
        "password": "123456",
        "port": "50001"

    },
    "coordinator": {
        "name": "coordinator",
        "description": "Coordinate all operation",
        "username": "coordinator",
        "password": "123456",
        "port": "50002"
    },
    "decision": {
        "name": "decision",
        "description": "Decision making from in coming message stock market",
        "username": "decision",
        "password": "123456",
        "port": "50003"
    },
    "fundamental": {
        "name": "fundamental",
        "description": "Fundamental new  analysing stock market",
        "username": "fundamental",
        "password": "123456",
        "port": "50004"
    },
    "pattern": {
        "name": "pattern",
        "description": "Pattern analysing stock market",
        "username": "pattern",
        "password": "123456",
        "port": "50005"
    },
    "technical": {
        "name": "technical",
        "description": "Technical analysing stock market",
        "username": "technical",
        "password": "123456",
        "port": "50006"
    },
    "publisher": {
        "name": "publisher",
        "description": "Publish all analysing data to portal",
        "username": "publisher",
        "password": "123456",
        "port": "50007"
    },
    "stream_agent": {
        "name": "stream_agent",
        "description": "Publish all analysing data to portal",
        "username": "stream_agent",
        "password": "123456",
        "port": "50008"
    }
}
sleep_delay = 0.0001


def get_xmpp_username(username):
    return f"{username}@{xmpp_host}"


def get_username(user):
    return get_xmpp_username(user['username'])
