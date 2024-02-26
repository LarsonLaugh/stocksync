#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from tkinter import *
import tkinter.messagebox
import time
from datetime import datetime
from classes import Trade, Ticket, Dividend, Transaction, User, Status, find_user_by_name, find_ticket_by_name
from jsontools import (save_user_to_json, save_ticket_to_json,
                       save_trade_to_json, load_ticket_from_json,
                       load_user_from_json, load_trade_from_json,
                       load_dividend_from_json, save_dividend_to_json,
                       load_transaction_from_json, save_transaction_to_json,
                       load_status_from_json, save_status_to_json)
from utils import quote_yahooapi

LOG_LINE_NUM = 0


class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        try:
            self.users = load_user_from_json()
        except:
            self.users = []
        try:
            self.trades = load_trade_from_json()
        except:
            self.trades = []
        try:
            self.tickets = load_ticket_from_json()
        except:
            self.tickets = []
        try:
            self.dividend = load_dividend_from_json()
        except:
            self.dividend = []
        try:
            self.transaction = load_transaction_from_json()
        except:
            self.transaction = []
        try:
            self.status = load_status_from_json()
        except:
            self.status = []

    def set_init_window(self):
        # TODO: Add another way to update portfolio instead of building it from trade history
        # TODO: Add Menu button to add a new user
        # TODO: Gain and loss for one ticket
        # TODO: Plot the trade history
        self.init_window_name.title("stock bookkeeper_v0.0")
        self.init_window_name.geometry('1000x800+10+10')
        # self.init_window_name["bg"] = "pink"   #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha", 0.9)  # 虚化，值越小虚化程度越高
        # Portfolio panel
        self.portfolio_label = Label(self.init_window_name, text="Portfolio", fg='lightblue')
        self.portfolio_label.grid(row=0, column=0)
        # whose portfolio
        self.whose_label = Label(self.init_window_name, text="Whose")
        self.whose_label.grid(row=1, column=0)
        whoList = [user.name for user in self.users] if len(self.users) > 0 else ['NoUser']
        self.whoList = StringVar()
        self.whoList.set(whoList[0])
        self.whose_portfolio = OptionMenu(self.init_window_name, self.whoList, *whoList)
        self.whose_portfolio.grid(row=2, column=0, rowspan=1, columnspan=1, padx=5, pady=5)
        # tillwhen
        self.when_label = Label(self.init_window_name, text="Till (DD-MM-YYYY)")
        self.when_label.grid(row=1, column=1)
        self.when_Text = Text(self.init_window_name, width=10, height=1)
        self.when_Text.grid(row=2, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        # show portfolio button
        self.portfolio_button = Button(self.init_window_name, text="Portfolio", bg="lightblue", width=10,
                                       command=self.API_portfolio)
        self.portfolio_button.grid(row=3, column=0, rowspan=1, columnspan=1)
        self.portfolio_button = Button(self.init_window_name, text="noAPI", bg="lightblue", width=10,
                                       command=self.noAPI_portfolio)
        self.portfolio_button.grid(row=3, column=1, rowspan=1, columnspan=1)

        # Trade search panel
        self.trade_label = Label(self.init_window_name, text="Trade Search", fg='lightblue')
        self.trade_label.grid(row=4, column=0)
        # whosetrade
        whoList_search = ['All'] + [user.name for user in self.users]
        self.who_label = Label(self.init_window_name, text="whoseTrade")
        self.who_label.grid(row=5, column=0)
        self.whoList_search = StringVar()
        self.whoList_search.set(whoList_search[0])
        self.whose_search = OptionMenu(self.init_window_name, self.whoList_search, *whoList_search)
        self.whose_search.grid(row=6, column=0, rowspan=1, columnspan=1, padx=5, pady=5)
        # whichticket
        whichList_search = ['All'] + [ticket.name for ticket in self.tickets]
        self.which_label = Label(self.init_window_name, text="whichTicket")
        self.which_label.grid(row=5, column=1)
        self.whichList_search = StringVar()
        self.whichList_search.set(whichList_search[0])
        self.which_search = OptionMenu(self.init_window_name, self.whichList_search, *whichList_search)
        self.which_search.grid(row=6, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        # fromwhen
        self.fromwhen_label = Label(self.init_window_name, text="From (DD-MM-YYYY)")
        self.fromwhen_label.grid(row=7, column=0)
        self.fromwhen_Text = Text(self.init_window_name, width=10, height=1)
        self.fromwhen_Text.grid(row=8, column=0, rowspan=1, columnspan=1, padx=5, pady=5)
        # tillwhen
        self.tillwhen_label = Label(self.init_window_name, text="Till (DD-MM-YYYY)")
        self.tillwhen_label.grid(row=7, column=1)
        self.tillwhen_Text = Text(self.init_window_name, width=10, height=1)
        self.tillwhen_Text.grid(row=8, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        # Show trade button
        self.show_ticker_button = Button(self.init_window_name, text="Show Trade History", bg="lightblue", width=15,
                                         command=self.table_history)
        self.show_ticker_button.grid(row=9, column=0, rowspan=1, columnspan=2)
        # Second column
        # Display panel
        self.display_panel_label = Label(self.init_window_name, text="Display Panel")
        self.display_panel_label.grid(row=0, column=20)
        self.result_data_Text = Text(self.init_window_name, width=80, height=30)
        self.result_data_Text.grid(row=1, column=20, rowspan=8, columnspan=20, padx=10, pady=10)
        # Save to json button
        self.save_button = Button(self.init_window_name, text="Save Changes", bg="lightblue", width=10,
                                  command=self.save_to_json)
        self.save_button.grid(row=1, column=50)
        # Log panel
        self.log_panel_label = Label(self.init_window_name, text="Log")
        self.log_panel_label.grid(row=10, column=20)
        self.log_data_Text = Text(self.init_window_name, width=80, height=10)
        self.log_data_Text.grid(row=11, column=20, rowspan=3, columnspan=20, padx=5, pady=5)

    def new_user_update(self, name: str, nickname: str):
        self.users.append(User(name, nickname))

    def new_trade_update(self, who: str, ticker: str, symbol: str, type: bool, price: float, volume: int, date: float):
        self.trades.append(Trade(who, ticker, type, price, volume, date))
        if not find_ticket_by_name(ticker, self.tickets):
            self.tickets.append(Ticket(ticker, symbol))
        if not find_user_by_name(who, self.users):
            self.tickets.append(User(who, who))

    def new_div_update(self, ticker: str, amount: float, date: float):
        self.dividend.append(Dividend(ticker, amount, date))
        if not find_ticket_by_name(ticker, self.tickets):
            self.tickets.append(Ticket(ticker, ticker))

    def new_trans_update(self, who: str, amount: float, date: float):
        self.transaction.append(Transaction(who, amount, date))
        if not find_user_by_name(who, self.users):
            self.users.append(User(who, who))

    def new_status_update(self, who: str, balance: float, date: float, tickets):
        self.status.append(Status(who, balance, date, tickets))
        if not find_user_by_name(who, self.users):
            self.users.append(User(who, who))

    def save_to_json(self):
        save_user_to_json(self.users)
        save_ticket_to_json(self.tickets)
        save_trade_to_json(self.trades)
        save_dividend_to_json(self.dividend)
        save_transaction_to_json(self.transaction)
        save_status_to_json(self.status)
        self.Savejson_to_Log()

    def table_portfolio(self):
        who = find_user_by_name(self.whoList.get().strip('\n'), self.users)
        when = self.when_Text.get(0.0, END).strip('\n')
        if when == '':
            when = datetime.now().strftime("%d-%m-%Y")
        my_trades = who.find_my_trade([trade for trade in self.trades if trade.is_deactivated == False])
        ticket_viewed = {}
        portfolio = {}
        my_status = who.find_my_status([stat for stat in self.status if stat.is_deactivated == False])  # find status for this person
        my_transaction = who.find_my_transaction([trans for trans in self.transaction if trans.is_deactivated == False])
        self.sort_status_bydate(my_status)
        stat_time = 0.0
        balance = 0.0
        for stat in my_status[::-1]:
            if stat.time <= self.convert_date(when):
                stat_time = stat.time
                balance = stat.balance
                stat_tickets = stat.get_portfolio()
                for ticket in stat_tickets:
                    if ticket['ticket'] != "":
                        ticket_viewed[ticket['ticket']] = (float(ticket['volume']), float(ticket['cost']), 0)
                        if not find_ticket_by_name(ticket['ticket'], self.tickets):
                            self.tickets.append(Ticket(ticket['ticket'], ticket['symbol']))
                break

        for trade in my_trades:
            if stat_time <= trade.time <= self.convert_date(when):
                if trade.ticket not in ticket_viewed:
                    ticket_viewed[trade.ticket] = (trade.volume * (int(trade.type) * 2 - 1),
                                                   trade.price * int(trade.type), 1)
                else:
                    new_volume = ticket_viewed[trade.ticket][0] + trade.volume * (int(trade.type) * 2 - 1)
                    new_price = 0
                    if new_volume > 0:
                        new_price = (int(trade.type) * trade.price * trade.volume + ticket_viewed[trade.ticket][0] *
                                     ticket_viewed[trade.ticket][1]) / new_volume
                    ticket_viewed[trade.ticket] = (new_volume, new_price, ticket_viewed[trade.ticket][2] + 1)

                balance -= trade.volume * (int(trade.type) * 2 - 1) * trade.price

        for trans in my_transaction:
            if stat_time <= trans.time <= self.convert_date(when):
                balance += trans.amount
        self.result_data_Text.delete(0.0, END)
        self.result_data_Text.insert(0.0, "Portfolio for {} at {}\n".format(who.name, when))
        self.result_data_Text.insert(END, "Loading status at {}, Balance is {}\n".format(
            self.convert_second_to_ddmmyyyy(stat_time), balance))
        who.balance = balance
        return ticket_viewed, portfolio

    def noAPI_portfolio(self):
        ticket_viewed, portfolio = self.table_portfolio()
        for ticket in ticket_viewed:
            if ticket_viewed[ticket][0] > 0:
                portfolio[ticket] = ticket_viewed[ticket]
                self.result_data_Text.insert(END,
                                             "{}: Vol.: {}, Avg.Cost {:.2f}, No.Trade {}\n\n".
                                             format(ticket, portfolio[ticket][0], portfolio[ticket][1],
                                                    portfolio[ticket][2]))

    def API_portfolio(self):
        ticket_viewed, portfolio = self.table_portfolio()
        for ticket in ticket_viewed:
            if ticket_viewed[ticket][0] > 0:
                portfolio[ticket] = ticket_viewed[ticket]
                quote_info = quote_yahooapi(find_ticket_by_name(ticket, self.tickets).symbol)
                self.result_data_Text.insert(END,
                                             "{}: Vol.: {}, Avg.Cost {:.2f}, No.Trade {}, LastPrice {}, Currency {}, 52WeekLow {}, 52WeekHigh {}\n\n".
                                             format(ticket, portfolio[ticket][0], portfolio[ticket][1],
                                                    portfolio[ticket][2], quote_info.get("ReMaPr"),
                                                    quote_info.get("currency"), quote_info.get("52Lo"),
                                                    quote_info.get("52Hi")
                                                    ))

    def plot_portfolio(self):
        print("Plot of portfolio")

    def table_history(self):
        self.result_data_Text.delete(0.0, END)
        who = self.whoList_search.get().strip('\n')
        which = self.whichList_search.get().strip('\n')
        fromwhen = self.fromwhen_Text.get(0.0, END).strip('\n')
        tillwhen = self.tillwhen_Text.get(0.0, END).strip('\n')
        if fromwhen == '':
            fromwhen = r"01-01-1990"
        if tillwhen == '':
            tillwhen = datetime.now().strftime("%d-%m-%Y")
        trades_to_show = []

        if who != 'All':
            who_is_user = [find_user_by_name(who, self.users)]
        else:
            who_is_user = self.users
        if which != 'All':
            which_is_ticker = [find_ticket_by_name(which, self.tickets)]
        else:
            which_is_ticker = self.tickets
        for trade in self.trades:
            if (trade.is_deactivated == False) and(trade.who in [user.name for user in who_is_user]) and (trade.ticket in [ticket.name for ticket in
                                                                                        which_is_ticker]) and (
                    self.convert_date(fromwhen) < trade.time <= self.convert_date(tillwhen)):
                trades_to_show.append(trade)
        if not trades_to_show:
            self.result_data_Text.insert(0.0, "No relevant history is found")
            return None
        self.result_data_Text.insert(0.0, "Relevant trade history from {} till {}\n".format(fromwhen, tillwhen))
        self.sort_trade_bydate(trades_to_show)
        for trade in trades_to_show:
            self.result_data_Text.insert(END, "date: {}, who: {}, ticker: {}, type: {}, price: {}, volume: {}\n".format(
                time.strftime("%d-%m-%Y", time.localtime(trade.time)),
                trade.who, trade.ticket, 'BUY' if trade.type else 'SELL', trade.price, trade.volume))

    def sort_trade_bydate(self, trades):
        def tradetime(trade):
            return trade.time

        trades.sort(key=tradetime)

    def sort_status_bydate(self, status):
        def statustime(stat):
            return stat.time

        status.sort(key=statustime)

    def plot_history(self):
        print("Plot of trade in history")

    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    def convert_date(self, date: str):
        if re.match(r'^\d\d-\d\d-\d\d\d\d$', date):
            return datetime(int(date.split('-')[2]), int(date.split('-')[1]),
                            int(date.split('-')[0])).timestamp()
        else:
            tkinter.messagebox.showerror(title='ValueError', message='The date must be in DD-MM-YYYY format！')

    def convert_second_to_ddmmyyyy(self, time_in_second: float):
        return datetime.fromtimestamp(time_in_second).strftime("%d-%m-%Y")


    def logmsg(self, msgtype: str):
        if msgtype == 'adduser':
            name, nickname = self.name_text.get(1.0, END).strip('\n'), self.nname_text.get(1.0, END).strip('\n')
            if name and nickname:
                self.new_user_update(name, nickname)
                return 'New User:' + '_'.join((name, nickname))
            else:
                tkinter.messagebox.showerror(title='ValueError', message='Your input is incorrect!')
        if msgtype == 'inputtrade':
            who, ticker, symbol, tradetype, price, volume, date = self.who_options.get().strip(
                '\n'), self.ticker_Text.get(1.0, END).strip(
                '\n'), self.symbol_Text.get(1.0, END).strip('\n'), self.type_bool.get(), self.price_Text.get(1.0,
                                                                                                             END).strip(
                '\n'), self.volume_Text.get(1.0,
                                            END).strip(
                '\n'), self.date_Text.get(1.0, END).strip('\n')

            if ticker and tradetype and price and volume and date:
                self.new_trade_update(who, ticker, symbol, IsBuy(tradetype), float(price), int(volume),
                                      self.convert_date(date))
                return 'New Trade: ' + '_'.join((who, ticker, symbol, tradetype, price, volume, date))
            else:
                tkinter.messagebox.showerror(title='ValueError', message='Your input is incorrect!')
                return "Input Error"

        if msgtype == 'inputdividend':
            ticker, amount, date = self.ticker_Text.get(1.0, END).strip('\n'), self.volume_Text.get(1.0, END).strip(
                '\n'), self.date_Text.get(1.0, END).strip('\n')
            if ticker and amount and date:
                self.new_div_update(ticker, float(amount), self.convert_date(date))
                return 'New Dividend: ' + '_'.join((ticker, amount, date))
            else:
                tkinter.messagebox.showerror(title='ValueError', message='Your input is incorrect!')
                return "Input Error"

        if msgtype == 'inputtransaction':
            who, amount, date = self.whosemoney_input.get().strip('\n'), self.amount_Text.get(1.0, END).strip(
                '\n'), self.transactiondate_Text.get(1.0, END).strip('\n')
            if who and amount and date:
                self.new_trans_update(who, float(amount), self.convert_date(date))
                return 'New Transaction: ' + '_'.join((who, amount, date))
            else:
                tkinter.messagebox.showerror(title='ValueError', message='Your input is incorrect!')
                return "Input Error"

        if msgtype == 'inputstatus':
            who, balance, date, tickets = self.whosestatus_input.get().strip('\n'), self.balance_Text.get(1.0,
                                                                                                          END).strip(
                '\n'), self.statusdate_Text.get(1.0, END).strip('\n'), \
                                          [{'ticket': self.ticket01_Text.get(1.0, END).strip('\n'),
                                            'symbol': self.symbol01_Text.get(1.0, END).strip('\n'),
                                            'volume': self.volume01_Text.get(1.0, END).strip('\n'),
                                            'cost': self.cost01_Text.get(1.0, END).strip('\n')},
                                           {'ticket': self.ticket02_Text.get(1.0, END).strip('\n'),
                                            'symbol': self.symbol02_Text.get(1.0, END).strip('\n'),
                                            'volume': self.volume02_Text.get(1.0, END).strip('\n'),
                                            'cost': self.cost02_Text.get(1.0, END).strip('\n')},
                                           {'ticket': self.ticket03_Text.get(1.0, END).strip('\n'),
                                            'symbol': self.symbol03_Text.get(1.0, END).strip('\n'),
                                            'volume': self.volume03_Text.get(1.0, END).strip('\n'),
                                            'cost': self.cost03_Text.get(1.0, END).strip('\n')},
                                           {'ticket': self.ticket04_Text.get(1.0, END).strip('\n'),
                                            'symbol': self.symbol04_Text.get(1.0, END).strip('\n'),
                                            'volume': self.volume04_Text.get(1.0, END).strip('\n'),
                                            'cost': self.cost04_Text.get(1.0, END).strip('\n')},
                                           {'ticket': self.ticket05_Text.get(1.0, END).strip('\n'),
                                            'symbol': self.symbol05_Text.get(1.0, END).strip('\n'),
                                            'volume': self.volume05_Text.get(1.0, END).strip('\n'),
                                            'cost': self.cost05_Text.get(1.0, END).strip('\n')}
                                           ]

            if who and balance and date:
                self.new_status_update(who, float(balance), self.convert_date(date), tickets)
                return 'New Status created: ' + '_'.join((who, balance, date))
            else:
                tkinter.messagebox.showerror(title='ValueError', message='Your input is incorrect!')
                return "Input Error"

        if msgtype == 'arkuser':
            selected = []
            active_user = [user for user in self.users if user.is_deactivated == False]
            for idx, user_int in enumerate(self.user_Intlist):
                if user_int.get() == 1:
                    selected.append(active_user[idx])
            if len(selected) == 0:
                return 'There are no user selected!'
            else:
                for user in selected:
                    user.is_deactivated = True
                return 'Selected users are archived: ' + '_'.join(set([user.name for user in selected]))

        if msgtype == 'arktrade':
            selected = []
            active_trade = [trade for trade in self.trades if trade.is_deactivated == False]
            for idx, trade_int in enumerate(self.trade_Intlist):
                if trade_int.get() == 1:
                    selected.append(active_trade[idx])
            if len(selected) == 0:
                return 'There are no trade selected!'
            else:
                for trade in selected:
                    trade.is_deactivated = True
                return 'Selected trades are archived: ' + '\n'.join(set([self.convert_second_to_ddmmyyyy(trade.time)+'_'+trade.who+'_'+trade.ticket+'_'+BooltoStr(trade.type)+'_'+str(trade.volume) for trade in selected]))

        if msgtype == 'arktran':
            selected = []
            active_tran = [tran for tran in self.transaction if tran.is_deactivated == False]
            for idx, tran_int in enumerate(self.transaction_Intlist):
                if tran_int.get() == 1:
                    selected.append(active_tran[idx])
            if len(selected) == 0:
                return 'There are no transaction selected!'
            else:
                for tran in selected:
                    tran.is_deactivated = True
                return 'Selected trades are archived: ' + '\n'.join(set([self.convert_second_to_ddmmyyyy(tran.time)+'_'+tran.who+'_'+str(tran.amount) for tran in selected]))

        if msgtype == 'arkstat':
            selected = []
            active_status = [stat for stat in self.status if stat.is_deactivated == False]
            for idx, stat_int in enumerate(self.status_Intlist):
                if stat_int.get() == 1:
                    selected.append(active_status[idx])
            if len(selected) == 0:
                return 'There are no status selected!'
            else:
                for stat in selected:
                    stat.is_deactivated = True
                return 'Selected status are archived: ' + '\n'.join(set([self.convert_second_to_ddmmyyyy(stat.time)+'_'+stat.who+'_'+str(stat.balance) for stat in selected]))

        if msgtype == 'dearkuser':
            selected = []
            inactive_user = [user for user in self.users if user.is_deactivated == True]
            for idx, user_int in enumerate(self.recover_user_Intlist):
                if user_int.get() == 1:
                    selected.append(inactive_user[idx])
            if len(selected) == 0:
                return 'There are no user selected!'
            else:
                for user in selected:
                    user.is_deactivated = False
                return 'Selected users are recoverd: ' + '_'.join(set([user.name for user in selected]))

        if msgtype == 'dearktrade':
            selected = []
            inactive_trade = [trade for trade in self.trades if trade.is_deactivated == True]
            for idx, trade_int in enumerate(self.recover_trade_Intlist):
                if trade_int.get() == 1:
                    selected.append(inactive_trade[idx])
            if len(selected) == 0:
                return 'There are no trade selected!'
            else:
                for trade in selected:
                    trade.is_deactivated = False
                return 'Selected trades are recovered: ' + '\n'.join(set([self.convert_second_to_ddmmyyyy(trade.time)+'_'+trade.who+'_'+trade.ticket+'_'+BooltoStr(trade.type)+'_'+str(trade.volume) for trade in selected]))

        if msgtype == 'dearktran':
            selected = []
            inactive_transactions = [tran for tran in self.transaction if tran.is_deactivated == True]
            for idx, tran_int in enumerate(self.recover_transaction_Intlist):
                if tran_int.get() == 1:
                    selected.append(inactive_transactions[idx])
            if len(selected) == 0:
                return 'There are no transaction selected!'
            else:
                for trade in selected:
                    trade.is_deactivated = False
                return 'Selected transactions are recovered: ' + '\n'.join(set([self.convert_second_to_ddmmyyyy(tran.time)+'_'+tran.who+'_'+str(tran.amount) for tran in selected]))

        if msgtype == 'dearkstat':
            selected = []
            inactive_status = [stat for stat in self.status if stat.is_deactivated == True]
            for idx, stat_int in enumerate(self.recover_status_Intlist):
                if stat_int.get() == 1:
                    selected.append(inactive_status[idx])
            if len(selected) == 0:
                return 'There are no status selected!'
            else:
                for stat in selected:
                    stat.is_deactivated = False
                return 'Selected status are recovered: ' + '\n'.join(set([self.convert_second_to_ddmmyyyy(stat.time)+'_'+stat.who+'_'+str(stat.balance) for stat in selected]))

        if msgtype == 'savejson':
            return 'New updates to database has been written into json files.'

    def User_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('adduser') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def Trade_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('inputtrade') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def Div_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('inputdividend') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def Transaction_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('inputtransaction') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def Status_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('inputstatus') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def ArkUser_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('arkuser') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def ArkTrade_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('arktrade') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def ArkTran_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('arktran') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def ArkStat_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('arkstat') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def DeArkUser_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('dearkuser') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def DeArkTrade_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('dearktrade') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def DeArkTran_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('dearktran') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def DeArkStat_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('dearkstat') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    def Savejson_to_Log(self):
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + self.logmsg('savejson') + "\n"
        self.log_data_Text.insert(END, logmsg_in)
        with open("log.txt", 'a', encoding='utf-8') as f:
            f.write(logmsg_in)

    # Add a new user
    def menuAddUser(self):
        add_user = Toplevel()
        add_user.title("User Box")
        add_user.geometry('660x300+10+10')
        # Input panel
        self.input_panel_label = Label(add_user, text="New user information Here", fg='lightblue')
        self.input_panel_label.grid(row=0, column=0)
        # Name
        self.name_label = Label(add_user, text="Name")
        self.name_label.grid(row=1, column=0)
        self.name_text = Text(add_user, width=20, height=1)
        self.name_text.grid(row=2, column=0, rowspan=1, columnspan=1, padx=5, pady=5)
        # Nickname
        self.nname_label = Label(add_user, text="Nickname")
        self.nname_label.grid(row=1, column=1)
        self.nname_text = Text(add_user, width=20, height=1)
        self.nname_text.grid(row=2, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        # submit button
        self.trade_button = Button(add_user, text="Enter", bg="lightblue", width=20, height=2,
                                   command=self.User_to_Log)
        self.trade_button.grid(row=3, column=1, rowspan=2, columnspan=1, padx=5, pady=5)

    # Add menu/Trade item
    def menuAddTrade(self):
        add_trade = Toplevel()
        add_trade.title("Trade Box")
        add_trade.geometry('660x300+10+10')
        # Input panel
        self.input_panel_label = Label(add_trade, text="Input New Trade Here", fg='lightblue')
        self.input_panel_label.grid(row=0, column=0)
        # who
        self.who_label = Label(add_trade, text="Who")
        self.who_label.grid(row=1, column=0)
        whoList = [user.name for user in self.users]
        self.who_options = StringVar()
        self.who_options.set(whoList[0])
        self.wholist_input = OptionMenu(add_trade, self.who_options, *whoList)
        self.wholist_input.grid(row=2, column=0, rowspan=1, columnspan=1)
        # ticker
        self.ticker_label = Label(add_trade, text="Ticker")
        self.ticker_label.grid(row=1, column=1)
        self.ticker_Text = Text(add_trade, width=20, height=1)
        self.ticker_Text.grid(row=2, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        # symbol
        self.symbol_label = Label(add_trade, text="Symbol")
        self.symbol_label.grid(row=1, column=2)
        self.symbol_Text = Text(add_trade, width=20, height=1)
        self.symbol_Text.grid(row=2, column=2, rowspan=1, columnspan=1, padx=5, pady=5)
        # type
        type_bool = ["Buy", "Sell"]
        self.type_label = Label(add_trade, text="Type(Buy/Sell)")
        self.type_label.grid(row=3, column=0)
        self.type_bool = StringVar()
        self.type_bool.set(type_bool[0])
        self.type_input = OptionMenu(add_trade, self.type_bool, *type_bool)
        self.type_input.grid(row=4, column=0, rowspan=1, columnspan=1, padx=5, pady=5)
        # price
        self.price_label = Label(add_trade, text="Price")
        self.price_label.grid(row=3, column=1)
        self.price_Text = Text(add_trade, width=20, height=1)
        self.price_Text.grid(row=4, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        # volume
        self.volume_label = Label(add_trade, text="Volume/Amount(Dividend)")
        self.volume_label.grid(row=3, column=2)
        self.volume_Text = Text(add_trade, width=20, height=1)
        self.volume_Text.grid(row=4, column=2, rowspan=1, columnspan=1, padx=5, pady=5)
        # date
        self.date_label = Label(add_trade, text="Date(DD-MM-YYYY)")
        self.date_label.grid(row=5, column=1)
        self.date_Text = Text(add_trade, width=20, height=1)
        self.date_Text.grid(row=6, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        # submit button
        self.trade_button = Button(add_trade, text="Enter", bg="lightblue", width=20, height=2,
                                   command=self.Trade_to_Log)
        self.trade_button.grid(row=7, column=1, rowspan=2, columnspan=1, padx=5, pady=5)
        add_trade.mainloop()

    # Add menu/Dividend item
    def menuAddDividend(self):
        add_div = Toplevel()
        add_div.title("Dividend Box")
        add_div.geometry('660x300+10+10')
        # Input panel
        self.input_panel_label = Label(add_div, text="Input New Dividend Here", fg='lightblue')
        self.input_panel_label.grid(row=0, column=0)
        # ticker
        self.ticker_label = Label(add_div, text="Ticker")
        self.ticker_label.grid(row=1, column=1)
        self.ticker_Text = Text(add_div, width=20, height=1)
        self.ticker_Text.grid(row=2, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        # symbol
        self.symbol_label = Label(add_div, text="Symbol")
        self.symbol_label.grid(row=1, column=2)
        self.symbol_Text = Text(add_div, width=20, height=1)
        self.symbol_Text.grid(row=2, column=2, rowspan=1, columnspan=1, padx=5, pady=5)
        # amount
        self.volume_label = Label(add_div, text="Amount")
        self.volume_label.grid(row=3, column=1)
        self.volume_Text = Text(add_div, width=20, height=1)
        self.volume_Text.grid(row=4, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        # date
        self.date_label = Label(add_div, text="Date(DD-MM-YYYY)")
        self.date_label.grid(row=3, column=2)
        self.date_Text = Text(add_div, width=20, height=1)
        self.date_Text.grid(row=4, column=2, rowspan=1, columnspan=1, padx=5, pady=5)
        # submit button
        self.div_button = Button(add_div, text="Enter", bg="lightblue", width=10, height=2,
                                 command=self.Div_to_Log)
        self.div_button.grid(row=5, column=2)
        add_div.mainloop()

    # Add menu/Transaction item
    def menuAddTransaction(self):
        add_trans = Toplevel()
        add_trans.title("Transaction Box")
        add_trans.geometry('660x440+10+10')
        # Input panel
        self.input_panel_label = Label(add_trans, text="Input New Transaction Here", fg='lightblue')
        self.input_panel_label.grid(row=0, column=0)
        # whosemoney
        whosemoney = [user.name for user in self.users]
        self.whosemoney_label = Label(add_trans, text="whoseMoney")
        self.whosemoney_label.grid(row=1, column=0)
        self.whosemoney_input = StringVar()
        self.whosemoney_input.set(whosemoney[0])
        self.whosemoney = OptionMenu(add_trans, self.whosemoney_input, *whosemoney)
        self.whosemoney.grid(row=2, column=0, rowspan=1, columnspan=1, padx=5, pady=5)
        # amount
        self.amount_label = Label(add_trans, text="Amount")
        self.amount_label.grid(row=1, column=1)
        self.amount_Text = Text(add_trans, width=20, height=1)
        self.amount_Text.grid(row=2, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        # date
        self.transactiondate_label = Label(add_trans, text="Date(DD-MM-YYYY)")
        self.transactiondate_label.grid(row=1, column=2)
        self.transactiondate_Text = Text(add_trans, width=20, height=1)
        self.transactiondate_Text.grid(row=2, column=2, rowspan=1, columnspan=1, padx=5, pady=5)
        # Import Transaction button
        self.import_transaction_button = Button(add_trans, text="Enter", bg="lightblue", width=15, height=2,
                                                command=self.Transaction_to_Log)
        self.import_transaction_button.grid(row=3, column=2)
        add_trans.mainloop()

    # Add menu/Status item
    def menuAddStatus(self):
        add_status = Toplevel()
        add_status.title("Status Box")
        add_status.geometry('850x350+10+10')
        # Input panel
        self.input_panel_label = Label(add_status, text="Input New Status Here", fg='lightblue')
        self.input_panel_label.grid(row=0, column=0)
        # Input status
        whosestatus = [user.name for user in self.users]
        self.whosestatus_label = Label(add_status, text="whoseStatus")
        self.whosestatus_label.grid(row=1, column=0)
        self.whosestatus_input = StringVar()
        self.whosestatus_input.set(whosestatus[0])
        self.whosestatus = OptionMenu(add_status, self.whosestatus_input, *whosestatus)
        self.whosestatus.grid(row=2, column=0, rowspan=1, columnspan=1, padx=5, pady=5)
        # balance
        self.balance_label = Label(add_status, text="Balance")
        self.balance_label.grid(row=1, column=1)
        self.balance_Text = Text(add_status, width=20, height=1)
        self.balance_Text.grid(row=2, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        # date
        self.statusdate_label = Label(add_status, text="Date(DD-MM-YYYY)")
        self.statusdate_label.grid(row=1, column=2)
        self.statusdate_Text = Text(add_status, width=20, height=1)
        self.statusdate_Text.grid(row=2, column=2, rowspan=1, columnspan=1, padx=5, pady=5)
        # ticket
        self.ticket_label = Label(add_status, text="Ticket")
        self.ticket_label.grid(row=3, column=1)
        # symbol
        self.symbol_label = Label(add_status, text="Symbol")
        self.symbol_label.grid(row=3, column=2)
        # Volume
        self.volume_label = Label(add_status, text="Volume")
        self.volume_label.grid(row=3, column=3)
        # Cost
        self.volume_label = Label(add_status, text="Cost")
        self.volume_label.grid(row=3, column=4)
        # Ticket 01
        self.ticket01_Text = Text(add_status, width=20, height=1)
        self.ticket01_Text.grid(row=4, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        self.symbol01_Text = Text(add_status, width=20, height=1)
        self.symbol01_Text.grid(row=4, column=2, rowspan=1, columnspan=1, padx=5, pady=5)
        self.volume01_Text = Text(add_status, width=20, height=1)
        self.volume01_Text.grid(row=4, column=3, rowspan=1, columnspan=1, padx=5, pady=5)
        self.cost01_Text = Text(add_status, width=20, height=1)
        self.cost01_Text.grid(row=4, column=4, rowspan=1, columnspan=1, padx=5, pady=5)
        self.ticket01_label = Label(add_status, text="T01")
        self.ticket01_label.grid(row=4, column=5)
        # Ticket 02
        self.ticket02_Text = Text(add_status, width=20, height=1)
        self.ticket02_Text.grid(row=5, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        self.symbol02_Text = Text(add_status, width=20, height=1)
        self.symbol02_Text.grid(row=5, column=2, rowspan=1, columnspan=1, padx=5, pady=5)
        self.volume02_Text = Text(add_status, width=20, height=1)
        self.volume02_Text.grid(row=5, column=3, rowspan=1, columnspan=1, padx=5, pady=5)
        self.cost02_Text = Text(add_status, width=20, height=1)
        self.cost02_Text.grid(row=5, column=4, rowspan=1, columnspan=1, padx=5, pady=5)
        self.ticket02_label = Label(add_status, text="T02")
        self.ticket02_label.grid(row=5, column=5)
        # Ticket 03
        self.ticket03_Text = Text(add_status, width=20, height=1)
        self.ticket03_Text.grid(row=6, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        self.symbol03_Text = Text(add_status, width=20, height=1)
        self.symbol03_Text.grid(row=6, column=2, rowspan=1, columnspan=1, padx=5, pady=5)
        self.volume03_Text = Text(add_status, width=20, height=1)
        self.volume03_Text.grid(row=6, column=3, rowspan=1, columnspan=1, padx=5, pady=5)
        self.cost03_Text = Text(add_status, width=20, height=1)
        self.cost03_Text.grid(row=6, column=4, rowspan=1, columnspan=1, padx=5, pady=5)
        self.ticket03_label = Label(add_status, text="T03")
        self.ticket03_label.grid(row=6, column=5)
        # Ticket 04
        self.ticket04_Text = Text(add_status, width=20, height=1)
        self.ticket04_Text.grid(row=7, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        self.symbol04_Text = Text(add_status, width=20, height=1)
        self.symbol04_Text.grid(row=7, column=2, rowspan=1, columnspan=1, padx=5, pady=5)
        self.volume04_Text = Text(add_status, width=20, height=1)
        self.volume04_Text.grid(row=7, column=3, rowspan=1, columnspan=1, padx=5, pady=5)
        self.cost04_Text = Text(add_status, width=20, height=1)
        self.cost04_Text.grid(row=7, column=4, rowspan=1, columnspan=1, padx=5, pady=5)
        self.ticket04_label = Label(add_status, text="T04")
        self.ticket04_label.grid(row=7, column=5)
        # Ticket 05
        self.ticket05_Text = Text(add_status, width=20, height=1)
        self.ticket05_Text.grid(row=8, column=1, rowspan=1, columnspan=1, padx=5, pady=5)
        self.symbol05_Text = Text(add_status, width=20, height=1)
        self.symbol05_Text.grid(row=8, column=2, rowspan=1, columnspan=1, padx=5, pady=5)
        self.volume05_Text = Text(add_status, width=20, height=1)
        self.volume05_Text.grid(row=8, column=3, rowspan=1, columnspan=1, padx=5, pady=5)
        self.cost05_Text = Text(add_status, width=20, height=1)
        self.cost05_Text.grid(row=8, column=4, rowspan=1, columnspan=1, padx=5, pady=5)
        self.ticket05_label = Label(add_status, text="T05")
        self.ticket05_label.grid(row=8, column=5)
        # Import button
        self.import_status_button = Button(add_status, text="Enter", bg="lightblue", width=15, height=2,
                                           command=self.Status_to_Log)
        self.import_status_button.grid(row=9, column=4)
        add_status.mainloop()

    # Manage menu/User item
    def menuMaUser(self):
        ma_user = Toplevel()
        ma_user.title("User Management")
        ma_user.geometry('300x350+10+10')
        # Label
        self.display_label = Label(ma_user, text="Display User Here", fg='lightblue')
        self.display_label.grid(row=0, column=0)
        Intlist = []
        idx = 0
        active_users = [user for user in self.users if user.is_deactivated == False]
        if len(active_users) == 0:
            self.no_active_user_label = Label(ma_user, text="No achived User found", fg='lightblue')
            self.no_active_user_label.grid(row=1, column=0)
        else:
            for idx, user in enumerate(active_users):
                Intlist.append(IntVar())
                Checkbutton(ma_user, text=user.name + ' , ' + user.nickname, variable=Intlist[idx], onvalue=1,
                            offvalue=0).grid(sticky="W", row=idx + 1, column=1)
            self.user_Intlist = Intlist
            self.archive_user_button = Button(ma_user, text="Achive", bg="lightblue", width=15, height=2,
                                         command=self.ArkUser_to_Log)
            self.archive_user_button.grid(row=idx + 2, column=1)
        ma_user.mainloop()

    def menuMaTrade(self):
        ma_trade = Toplevel()
        ma_trade.title("Trade Management")
        ma_trade.geometry('500x350+10+10')
        # Label
        self.display_label = Label(ma_trade, text="Display Trade Here", fg='lightblue')
        self.display_label.grid(row=0, column=0)
        Intlist = []
        idx = 0
        active_trades = [trade for trade in self.trades if trade.is_deactivated == False]
        if len(active_trades) == 0:
            self.no_trade_label = Label(ma_trade, text="No active Trade found", fg='lightblue')
            self.no_trade_label.grid(row=1, column=0)
        else:
            for idx, trade in enumerate(active_trades):
                Intlist.append(IntVar())
                Checkbutton(ma_trade, text=self.convert_second_to_ddmmyyyy(trade.time)+' , '+trade.who+' , '+trade.ticket+' , '+str(trade.volume)+' , '+BooltoStr(trade.type)+' , '+str(trade.price), variable=Intlist[idx], onvalue=1,
                            offvalue=0).grid(sticky="W", row=idx + 1, column=1)
            self.trade_Intlist = Intlist
            self.archive_trade_button = Button(ma_trade, text="Achive", bg="lightblue", width=15, height=2,
                                         command=self.ArkTrade_to_Log)
            self.archive_trade_button.grid(row=idx + 2, column=1)
        ma_trade.mainloop()

    def menuMaDividend(self):
        pass

    def menuMaTransaction(self):
        ma_tran = Toplevel()
        ma_tran.title("Transaction Management")
        ma_tran.geometry('500x350+10+10')
        # Label
        self.display_label = Label(ma_tran, text="Display Transaction Here", fg='lightblue')
        self.display_label.grid(row=0, column=0)
        Intlist = []
        idx = 0
        active_transactions = [tran for tran in self.transaction if tran.is_deactivated == False]
        if len(active_transactions) == 0:
            self.no_transaction_label = Label(ma_tran, text="No active Transaction found", fg='lightblue')
            self.no_transaction_label.grid(row=1, column=0)
        else:
            for idx, tran in enumerate(active_transactions):
                Intlist.append(IntVar())
                Checkbutton(ma_tran, text=self.convert_second_to_ddmmyyyy(tran.time)+' , '+tran.who+' , '+str(tran.amount), variable=Intlist[idx], onvalue=1,
                            offvalue=0).grid(sticky="W", row=idx + 1, column=1)
            self.transaction_Intlist = Intlist
            self.archive_transaction_button = Button(ma_tran, text="Achive", bg="lightblue", width=15, height=2,
                                         command=self.ArkTran_to_Log)
            self.archive_transaction_button.grid(row=idx + 2, column=1)
        ma_tran.mainloop()

    def menuMaStatus(self):
        ma_stat = Toplevel()
        ma_stat.title("Status Management")
        ma_stat.geometry('500x350+10+10')
        # Label
        self.display_label = Label(ma_stat, text="Display Status Here", fg='lightblue')
        self.display_label.grid(row=0, column=0)
        Intlist = []
        idx = 0
        active_status = [stat for stat in self.status if stat.is_deactivated == False]
        if len(active_status) == 0:
            self.no_status_label = Label(ma_stat, text="No active Status found", fg='lightblue')
            self.no_status_label.grid(row=1, column=0)
        else:
            for idx, stat in enumerate(active_status):
                Intlist.append(IntVar())
                Checkbutton(ma_stat, text=self.convert_second_to_ddmmyyyy(stat.time) + ' , ' + stat.who + ' , ' + str(
                    stat.balance), variable=Intlist[idx], onvalue=1,
                            offvalue=0).grid(sticky="W", row=idx + 1, column=1)
            self.status_Intlist = Intlist
            self.archive_status_button = Button(ma_stat, text="Achive", bg="lightblue", width=15, height=2,
                                         command=self.ArkStat_to_Log)
            self.archive_status_button.grid(row=idx + 2, column=1)
        ma_stat.mainloop()

    def menuArkUser(self):
        ark_user = Toplevel()
        ark_user.title("Archived User")
        ark_user.geometry('300x350+10+10')
        # Label
        self.display_label = Label(ark_user, text="Display User Here", fg='lightblue')
        self.display_label.grid(row=0, column=0)

        inactive_users = [user for user in self.users if user.is_deactivated == True]
        if len(inactive_users) == 0:
            self.no_archived_user_label = Label(ark_user, text="No achived User found", fg='lightblue')
            self.no_archived_user_label.grid(row=1, column=0)
        else:
            Intlist = []
            idx = 0
            for idx, user in enumerate(inactive_users):
                Intlist.append(IntVar())
                Checkbutton(ark_user, text=user.name + ',' + user.nickname, variable=Intlist[idx], onvalue=1,
                            offvalue=0).grid(sticky="W", row=idx + 1, column=1)
            self.recover_user_Intlist = Intlist
            self.recover_user_button = Button(ark_user, text="Recover", bg="lightblue", width=15, height=2,
                                         command=self.DeArkUser_to_Log)
            self.recover_user_button.grid(row=idx + 2, column=1)
        ark_user.mainloop()

    def menuArkTrade(self):
        ark_trade = Toplevel()
        ark_trade.title("Archived Trade")
        ark_trade.geometry('500x350+10+10')
        # Label
        self.display_label = Label(ark_trade, text="Display Trade Here", fg='lightblue')
        self.display_label.grid(row=0, column=0)

        inactive_trades = [trade for trade in self.trades if trade.is_deactivated == True]
        if len(inactive_trades) == 0:
            self.no_archived_trade_label = Label(ark_trade, text="No achived Trade found", fg='lightblue')
            self.no_archived_trade_label.grid(row=1, column=0)
        else:
            Intlist = []
            idx = 0
            for idx, trade in enumerate(inactive_trades):
                Intlist.append(IntVar())
                Checkbutton(ark_trade, text=self.convert_second_to_ddmmyyyy(trade.time)+' , '+trade.who+' , '+trade.ticket+' , '+str(trade.volume)+' , '+BooltoStr(trade.type)+' , '+str(trade.price), variable=Intlist[idx], onvalue=1,
                            offvalue=0).grid(sticky="W", row=idx + 1, column=1)
            self.recover_trade_Intlist = Intlist
            self.recover_trade_button = Button(ark_trade, text="Recover", bg="lightblue", width=15, height=2,
                                         command=self.DeArkStat_to_Log)
            self.recover_trade_button.grid(row=idx + 2, column=1)
        ark_trade.mainloop()

    def menuArkDividend(self):
        pass

    def menuArkTransaction(self):
        ark_tran = Toplevel()
        ark_tran.title("Archived Trade")
        ark_tran.geometry('500x350+10+10')
        # Label
        self.display_label = Label(ark_tran, text="Display Transaction Here", fg='lightblue')
        self.display_label.grid(row=0, column=0)

        inactive_transactions = [tran for tran in self.transaction if tran.is_deactivated == True]
        if len(inactive_transactions) == 0:
            self.no_archived_transaction_label = Label(ark_tran, text="No achived Transaction found", fg='lightblue')
            self.no_archived_transaction_label.grid(row=1, column=0)
        else:
            Intlist = []
            idx = 0
            for idx, tran in enumerate(inactive_transactions):
                Intlist.append(IntVar())
                Checkbutton(ark_tran, text=self.convert_second_to_ddmmyyyy(tran.time)+' , '+tran.who+' , '+str(tran.amount), variable=Intlist[idx],
                            onvalue=1, offvalue=0).grid(sticky="W", row=idx + 1, column=1)
            self.recover_transaction_Intlist = Intlist
            self.recover_transaction_button = Button(ark_tran, text="Recover", bg="lightblue", width=15, height=2,
                                               command=self.DeArkTran_to_Log)
            self.recover_transaction_button.grid(row=idx + 2, column=1)
        ark_tran.mainloop()

    def menuArkStatus(self):
        ark_stat = Toplevel()
        ark_stat.title("Archived Status")
        ark_stat.geometry('500x350+10+10')
        # Label
        self.display_label = Label(ark_stat, text="Display Status Here", fg='lightblue')
        self.display_label.grid(row=0, column=0)

        inactive_status = [stat for stat in self.status if stat.is_deactivated == True]
        if len(inactive_status) == 0:
            self.no_archived_status_label = Label(ark_stat, text="No achived status found", fg='lightblue')
            self.no_archived_status_label.grid(row=1, column=0)
        else:
            Intlist = []
            idx = 0
            for idx, stat in enumerate(inactive_status):
                Intlist.append(IntVar())
                Checkbutton(ark_stat, text=self.convert_second_to_ddmmyyyy(stat.time) + ' , ' + stat.who + ' , ' + str(
                    stat.balance), variable=Intlist[idx],
                            onvalue=1, offvalue=0).grid(sticky="W", row=idx + 1, column=1)
            self.recover_status_Intlist = Intlist
            self.recover_status_button = Button(ark_stat, text="Recover", bg="lightblue", width=15, height=2,
                                                     command=self.DeArkStat_to_Log)
            self.recover_status_button.grid(row=idx + 2, column=1)
        ark_stat.mainloop()


def IsBuy(string: str):
    if string == 'Buy':
        return True
    else:
        return False

def BooltoStr(type: bool):
    if type == True:
        return 'Buy'
    else:
        return 'Sell'

def gui_start():
    init_window = Tk()
    mainmenu = Menu(init_window)
    addmenu = Menu(mainmenu, tearoff=False)
    managemenu = Menu(mainmenu, tearoff=False)
    archivemenu = Menu(mainmenu, tearoff=False)
    mainmenu.add_cascade(label="Add", menu=addmenu)
    mainmenu.add_cascade(label="Manage", menu=managemenu)
    mainmenu.add_cascade(label="Archived", menu=archivemenu)
    init_window.config(menu=mainmenu)
    ZMJ_PORTAL = MY_GUI(init_window)
    addmenu.add_command(label="User", command=ZMJ_PORTAL.menuAddUser)
    addmenu.add_command(label="Trade", command=ZMJ_PORTAL.menuAddTrade)
    addmenu.add_command(label="Dividend", command=ZMJ_PORTAL.menuAddDividend)
    addmenu.add_command(label="Transaction", command=ZMJ_PORTAL.menuAddTransaction)
    addmenu.add_command(label="Status", command=ZMJ_PORTAL.menuAddStatus)
    addmenu.add_separator()
    addmenu.add_command(label="Exit", command=init_window.quit)
    # TODO: in Manage menu, add items: User, Trade, Status, Dividend, Transaction. Each item generates a window to allow for archiving or permanently deleting input history.
    managemenu.add_command(label="User", command=ZMJ_PORTAL.menuMaUser)
    managemenu.add_command(label="Trade", command=ZMJ_PORTAL.menuMaTrade)
    managemenu.add_command(label="Dividend", command=ZMJ_PORTAL.menuMaDividend)
    managemenu.add_command(label="Transaction", command=ZMJ_PORTAL.menuMaTransaction)
    managemenu.add_command(label="Status", command=ZMJ_PORTAL.menuMaStatus)
    # TODO: in Archived menu, add items: User, Trade, Status, Dividend, Transaction. Each item generates a window to allow for recovering or permanently deleting archived history.
    archivemenu.add_command(label="User", command=ZMJ_PORTAL.menuArkUser)
    archivemenu.add_command(label="Trade", command=ZMJ_PORTAL.menuArkTrade)
    archivemenu.add_command(label="Dividend", command=ZMJ_PORTAL.menuArkDividend)
    archivemenu.add_command(label="Transaction", command=ZMJ_PORTAL.menuArkTransaction)
    archivemenu.add_command(label="Status", command=ZMJ_PORTAL.menuArkStatus)
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()


gui_start()
