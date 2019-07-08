xmpp_host = "127.0.0.1"

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
        "port": "50006"
    },
    "stream_agent": {
        "name": "stream_agent",
        "description": "Publish all analysing data to portal",
        "username": "stream_agent",
        "password": "123456",
        "port": "50007"
    }
}


def get_xmpp_username(username):
    return f"{username}@{xmpp_host}"
