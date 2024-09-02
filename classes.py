import time

BUY, SELL = True, False


class Trade:
    """
    A class to represent a trade.

    Attributes:
    who : str
        name of the trader
    ticket : str
        name of the ticket
    type : bool
        type of the trade (BUY/SELL)
    price : float
        price of the trade
    volume : int
        volume of the trade
    time : float
        time of the trade
    is_deactivated : bool
        status of the trade
    """
    def __init__(self, who_name: str, ticket_name: str, trade_type: bool, price: float,
                 volume: int, time: float, is_deactivated=False):
        self.who = who_name
        self.ticket = ticket_name
        self.type = trade_type
        self.price = price
        self.volume = volume
        self.time = time
        self._is_deactivated = is_deactivated

    @property
    def is_deactivated(self):
        return self._is_deactivated

    @is_deactivated.setter
    def is_deactivated(self, is_deactivated: bool):
        self._is_deactivated = is_deactivated

    def print(self):
        print("Trade -> date: {}, who: {}, type: {}, price: {}, volume: {}".format(
            time.strftime("%m-%d-%Y", time.localtime(self.time)),
            self.who, 'BUY' if self.type else 'SELL', self.price, self.volume))


class Dividend:
    """
    A class to represent a dividend.

    Attributes:
    ticket : str
        name of the ticket
    amount : float
        amount of the dividend
    time : float
        time of the dividend
    is_deactivated : bool
        status of the dividend
    """
    def __init__(self, ticket_name: str, amount: float, time: float, is_deactivated=False):
        self.ticket = ticket_name
        self.amount = amount
        self.time = time
        self._is_deactivated = is_deactivated

    @property
    def is_deactivated(self):
        return self._is_deactivated

    @is_deactivated.setter
    def is_deactivated(self, is_deactivated: bool):
        self._is_deactivated = is_deactivated

    def print(self):
        print("Dividend -> date: {}, ticket: {}, amount: {}".format(
            time.strftime("%m-%d-%Y", time.localtime(self.time)),
            self.ticket, self.amount))


class Transaction:
    """
    A class to represent a transaction.

    Attributes:
    who : str
        name of the person involved in the transaction
    amount : float
        amount of the transaction
    time : float
        time of the transaction
    is_deactivated : bool
        status of the transaction
    """
    def __init__(self, who_name: str, amount: float, time: float, is_deactivated=False):
        self.who = who_name
        self.amount = amount
        self.time = time
        self._is_deactivated = is_deactivated

    @property
    def is_deactivated(self):
        return self._is_deactivated

    @is_deactivated.setter
    def is_deactivated(self, is_deactivated: bool):
        self._is_deactivated = is_deactivated

    def print(self):
        print("Transaction -> date: {}, who: {}, amount: {}".format(
            time.strftime("%m-%d-%Y", time.localtime(self.time)),
            self.who, self.amount))


class Status:
    """
    A class to represent a status.

    Attributes:
    who : str
        name of the person
    balance : float
        balance of the person
    time : float
        time of the status
    portfolio : dict
        portfolio of the person
    is_deactivated : bool
        status of the person
    """
    def __init__(self, who_name: str, balance: float, time: float, portfolio=None, is_deactivated=False):
        if portfolio is None:
            portfolio = {}
        self.who = who_name
        self._balance = balance
        self._portfolio = portfolio
        self._time = time
        self._is_deactivated = is_deactivated

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value: float):
        self._balance = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time: float):
        self._time = time

    @property
    def is_deactivated(self):
        return self._is_deactivated

    @is_deactivated.setter
    def is_deactivated(self, is_deactivated: bool):
        self._is_deactivated = is_deactivated

    def add_portfolio(self, ticket_name: str, volume: int):
        self._portfolio[ticket_name] = volume

    def get_portfolio(self):
        return self._portfolio

    def set_portfolio(self, portfolio: dict):
        self._portfolio = portfolio

    def print(self):
        print("Status -> date: {}, who: {}, balance: {}, tickets:{}".format(
            time.strftime("%m-%d-%Y", time.localtime(self.time)),
            self.who, self.balance, '_'.join([ticket + '-' + str(vol) for ticket, vol in self.get_portfolio().items()])
        ))


class Ticket:
    """
    A class to represent a ticket.

    Attributes:
    name : str
        name of the ticket
    symbol : str
        symbol of the ticket
    is_deactivated : bool
        status of the ticket
    """
    def __init__(self, name: str, symbol: str, is_deactivated=False):
        self.name = name
        self.symbol = symbol
        self._is_deactivated = is_deactivated

    @property
    def is_deactivated(self):
        return self._is_deactivated

    @is_deactivated.setter
    def is_deactivated(self, is_deactivated: bool):
        self._is_deactivated = is_deactivated

    def find_its_trade(self, trades):
        res = []
        for trade in trades:
            if trade.ticket == self.name or trade.ticket == self.symbol:
                res.append(trade)
        return res

    def find_its_dividend(self, dividends):
        res = []
        for div in dividends:
            if div.ticket == self.name or div.ticket == self.symbol:
                res.append(div)
        return res

    def history(self, fromwhen, tillwhen, trades):
        """
        Retrieves and prints the trade history for a given time range.

        Args:
            fromwhen (int): The starting timestamp of the time range.
            tillwhen (int): The ending timestamp of the time range.
            trades (list): A list of trade objects.

        Returns:
            None: If there is no trade history for the given stock.
        """
        its_trade = self.find_its_trade(trades)
        if not its_trade:
            print("No trade history on {}".format(self.name))
            return None
        print("----------------------------")
        print("Trade history for {} from {} to {}".format(self.name,
                                                          time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime(fromwhen)),
                                                          time.strftime("%m/%d/%Y, %H:%M:%S",
                                                                        time.localtime(tillwhen))))
        for trade in its_trade:
            if fromwhen < trade.time < tillwhen:
                trade.print()
        print("----------------------------")
        return None


class User:
    """
    A class to represent a user.

    Attributes:
    name : str
        name of the user
    nickname : str
        nickname of the user
    balance : float
        balance of the user
    inittime : float
        initial time of the user
    portfolio : dict
        portfolio of the user
    is_deactivated : bool
        status of the user
    """
    def __init__(self, name: str, nickname: str, balance=0, inittime=None, portfolio=None, is_deactivated=False):
        if inittime is None:
            inittime = time.time()
        if portfolio is None:
            portfolio = {}
        self.name = name
        self.nickname = nickname
        self._balance = balance
        self._inittime = inittime
        self._portfolio = portfolio
        self._is_deactivated = is_deactivated

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value: float):
        self._balance = value

    @property
    def init_time(self):
        return self._inittime

    @init_time.setter
    def init_time(self, init_time: float):
        self._inittime = init_time

    @property
    def is_deactivated(self):
        return self._is_deactivated

    @is_deactivated.setter
    def is_deactivated(self, is_deactivated: bool):
        self._is_deactivated = is_deactivated

    def add_portfolio(self, ticket_name: str, volume: int):
        self._portfolio[ticket_name] = volume

    def get_portfolio(self):
        return self._portfolio

    def find_my_trade(self, trades):
        res = []
        for trade in trades:
            if trade.who == self.name or trade.who == self.nickname:
                res.append(trade)
        return res

    def find_my_transaction(self, transactions):
        res = []
        for trans in transactions:
            if trans.who == self.name or trans.who == self.nickname:
                res.append(trans)
        return res

    def find_my_status(self, statuses):
        res = []
        for stat in statuses:
            if stat.who == self.name or stat.who == self.nickname:
                res.append(stat)
        return res

    def portfolio_when(self, when: float, trades):
        my_trades = self.find_my_trade(trades)
        ticket_viewed = {}
        portfolio = {}
        for trade in my_trades:
            if trade.time < when:
                if trade.ticket not in ticket_viewed:
                    ticket_viewed[trade.ticket] = trade.volume * (int(trade.type) * 2 - 1)
                else:
                    ticket_viewed[trade.ticket] += trade.volume * (int(trade.type) * 2 - 1)
        print("----------------------------")
        print("Portfolio for {} at {}".format(self.name, time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime(when))))
        for ticket in ticket_viewed:
            if ticket_viewed[ticket] > 0:
                portfolio[ticket] = ticket_viewed[ticket]
                print("{}: {}".format(ticket, portfolio[ticket]))
        print("----------------------------")

    def winlose_during(self, fromwhen: float, tillwhen: float, trades):
        # need to check the win-lose of each ticket that has been traded in SELL direction
        pass


def find_user_by_name(name: str, users):
    """
    Find a user by name or nickname.

    Parameters:
    name : str
        name or nickname of the user
    users : list
        list of users

    Returns:
    User or None
        the user if found, otherwise None
    """
    for user in users:
        if name in (user.name,user.nickname):
            return user
    return None


def find_ticket_by_name(name: str, tickets):
    """
    Find a ticket by name or symbol.

    Parameters:
    name : str
        name or symbol of the ticket
    tickets : list
        list of tickets

    Returns:
    Ticket or None
        the ticket if found, otherwise None
    """
    for ticket in tickets:
        if name in (ticket.name,ticket.symbol):
            return ticket
    return None
