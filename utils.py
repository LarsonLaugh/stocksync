import requests, json

def quote_yahooapi(ticket: str):
# TODO: add history data request
    url = "https://yfapi.net/v6/finance/quote"
    querystring = {"symbols": ticket}
    headers = {
        'x-api-key': "imQSb42RmJ4GkRfZZJveWaflQkn7tMji6sya7VAb"
    }
    resp_info = {}
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)

        # with open('cache.json', 'w') as f:
        #     json.dump(response.json(), f)
        resp_info = response.json()['quoteResponse']['result'][0]


    except KeyError:
        with open('cache.json', 'r') as f:
            cache = json.load(f)
        for resp in cache['quoteResponse']['result']:
            if resp['symbol'] == ticket:
                resp_info = resp

    return {"ReMaPr": resp_info['regularMarketPrice'],
            "currency": resp_info['currency'],
            "52Lo": resp_info['fiftyTwoWeekLow'],
            "52Hi": resp_info['fiftyTwoWeekHigh'],
            "symbol": resp_info['symbol']}

requests.request("GET", "https://yfapi.net/v11/finance/quote", headers={'x-api-key': "imQSb42RmJ4GkRfZZJveWaflQkn7tMji6sya7VAb"}, params={"symbols": "002409.SZ"})