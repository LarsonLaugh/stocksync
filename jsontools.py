import json
from classes import Trade, Ticket, User, Dividend, Transaction, Status


def encode_user(user: User):
    if isinstance(user, User):
        return {'name': user.name,
                'nickname': user.nickname,
                'balance': user.balance,
                'inittime': user.init_time,
                'portfolio': user.get_portfolio(),
                'is_deactivated': user.is_deactivated
                }
    else:
        type_name = user.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

def encode_ticket(ticket: Ticket):
    if isinstance(ticket, Ticket):
        return {'name': ticket.name,
                'symbol': ticket.symbol,
                'is_deactivated': ticket.is_deactivated
                }
    else:
        type_name = ticket.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

def encode_trade(trade: Trade):
    if isinstance(trade, Trade):
        return {'who': trade.who,
                'ticket': trade.ticket,
                'type': trade.type,
                'price': trade.price,
                'volume': trade.volume,
                'time': trade.time,
                'is_deactivated': trade.is_deactivated
                }
    else:
        type_name = trade.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

def encode_div(div: Dividend):
    if isinstance(div, Dividend):
        return {'ticket': div.ticket,
                'amount': div.amount,
                'time': div.time,
                'is_deactivated': div.is_deactivated
                }
    else:
        type_name = div.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

def encode_trans(trans: Transaction):
    if isinstance(trans, Transaction):
        return {'who': trans.who,
                'amount': trans.amount,
                'time': trans.time,
                'is_deactivated': trans.is_deactivated
                }
    else:
        type_name = trans.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

def encode_stat(status: Status):
    if isinstance(status, Status):
        return {'who': status.who,
                'balance': status.balance,
                'time': status.time,
                'tickets': status.get_portfolio(),
                'is_deactivated': status.is_deactivated
                }
    else:
        type_name = status.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

def load_trade_from_json(json_file_path='trades.json'):
    res = []
    with open(json_file_path, 'r') as f:
        try:
            trade_history = json.load(f)
        except:
            raise FileExistsError('{} is not accessible or empty'.format(json_file_path))
    if isinstance(trade_history, list):
        for trade in trade_history:
            res.append(
                Trade(trade['who'], trade['ticket'], trade['type'], trade['price'], trade['volume'], trade['time'], trade['is_deactivated']))
    return res

def save_trade_to_json(trades, json_file_path='trades.json'):
    trades_json = []
    for trade in trades:
        trades_json.append({'who': trade.who, 'ticket': trade.ticket, 'type': trade.type,
                            'price': trade.price, 'volume': trade.volume, 'time': trade.time, 'is_deactivated': trade.is_deactivated})
    with open(json_file_path, 'w') as f:
        json.dump(trades_json, f, default=encode_trade)

def load_user_from_json(json_file_path='users.json'):
    res = []
    with open(json_file_path, 'r') as f:
        try:
            user_info = json.load(f)
        except:
            raise FileExistsError('{} is not accessible or empty'.format(json_file_path))
    if isinstance(user_info, list):
        for user in user_info:
            res.append(User(user['name'], user['nickname'], user['balance'], user['inittime'], user['portfolio'], user['is_deactivated']))
    return res

def save_user_to_json(users, json_file_path='users.json'):
    users_json = []
    for user in users:
        users_json.append({'name': user.name, 'nickname': user.nickname, 'balance': user.balance, 'inittime': user.init_time, 'portfolio': user.get_portfolio(), 'is_deactivated': user.is_deactivated})
    with open(json_file_path, 'w') as f:
        json.dump(users_json, f, default=encode_user)

def load_ticket_from_json(json_file_path='tickets.json'):
    res = []
    with open(json_file_path, 'r') as f:
        try:
            tickets = json.load(f)
        except:
            raise FileExistsError('{} is not accessible or empty'.format(json_file_path))
    if isinstance(tickets, list):
        for ticket in tickets:
            res.append(Ticket(ticket['name'], ticket['symbol'], ticket['is_deactivated']))
    return res

def save_ticket_to_json(tickets, json_file_path='tickets.json'):
    tickets_json = []
    for ticket in tickets:
        tickets_json.append({'name': ticket.name, 'symbol': ticket.symbol, 'is_deactivated': ticket.is_deactivated})
    with open(json_file_path, 'w') as f:
        json.dump(tickets_json, f, default=encode_ticket)

def load_dividend_from_json(json_file_path='dividends.json'):
    res = []
    with open(json_file_path, 'r') as f:
        try:
            dividends = json.load(f)
        except:
            raise FileExistsError('{} is not accessible or empty'.format(json_file_path))
    if isinstance(dividends, list):
        for div in dividends:
            res.append(Dividend(div['ticket'], div['amount'], div['time'], div['is_deactivated']))
    return res

def save_dividend_to_json(dividend, json_file_path='dividends.json'):
    div_json = []
    for div in dividend:
        div_json.append({'ticket': div.ticket, 'amount': div.amount, 'time': div.time, 'is_deactivated': div.is_deactivated})
    with open(json_file_path, 'w') as f:
        json.dump(div_json, f, default=encode_div)

def load_transaction_from_json(json_file_path='transactions.json'):
    res = []
    with open(json_file_path, 'r') as f:
        try:
            transactions = json.load(f)
        except:
            raise FileExistsError('{} is not accessible or empty'.format(json_file_path))
    if isinstance(transactions, list):
        for trans in transactions:
            res.append(Transaction(trans['who'], trans['amount'], trans['time'], trans['is_deactivated']))
    return res

def save_transaction_to_json(transaction, json_file_path='transactions.json'):
    trans_json = []
    for trans in transaction:
        trans_json.append({'who': trans.who, 'amount': trans.amount, 'time': trans.time, 'is_deactivated': trans.is_deactivated})
    with open(json_file_path, 'w') as f:
        json.dump(trans_json, f, default=encode_trans)

def load_status_from_json(json_file_path='status.json'):
    res = []
    with open(json_file_path, 'r') as f:
        try:
            status = json.load(f)
        except:
            raise FileExistsError('{} is not accessible or empty'.format(json_file_path))
    if isinstance(status, list):
        for stat in status:
            res.append(Status(stat['who'], stat['balance'], stat['time'], stat['portfolio'], stat['is_deactivated']))
    return res

def save_status_to_json(status, json_file_path='status.json'):
    status_json = []
    for stat in status:
        status_json.append({'who': stat.who, 'balance': stat.balance, 'time': stat.time, 'portfolio': stat.get_portfolio(), 'is_deactivated': stat.is_deactivated})
    with open(json_file_path, 'w') as f:
        json.dump(status_json, f, default=encode_stat)