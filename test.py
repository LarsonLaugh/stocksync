import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from gui import MY_GUI, User, Trade, Ticket, Dividend, Transaction, Status

class TestMY_GUI(unittest.TestCase):

    @patch('gui.load_user_from_json', return_value=[User("Alice", "A")])
    @patch('gui.load_trade_from_json', return_value=[])
    @patch('gui.load_ticket_from_json', return_value=[])
    @patch('gui.load_dividend_from_json', return_value=[])
    @patch('gui.load_transaction_from_json', return_value=[])
    @patch('gui.load_status_from_json', return_value=[])
    def setUp(self, mock_load_user, mock_load_trade, mock_load_ticket, mock_load_dividend, mock_load_transaction, mock_load_status):
        self.gui = MY_GUI(MagicMock())

    def test_init(self):
        self.assertEqual(len(self.gui.users), 1)
        self.assertEqual(len(self.gui.trades), 0)
        self.assertEqual(len(self.gui.tickets), 0)
        self.assertEqual(len(self.gui.dividend), 0)
        self.assertEqual(len(self.gui.transaction), 0)
        self.assertEqual(len(self.gui.status), 0)

    def test_new_user_update(self):
        self.gui.new_user_update("Bob", "B")
        self.assertEqual(len(self.gui.users), 2)
        self.assertEqual(self.gui.users[1].name, "Bob")
        self.assertEqual(self.gui.users[1].nickname, "B")

    def test_new_trade_update(self):
        self.gui.new_trade_update("Alice", "AAPL", "AAPL", True, 150.0, 10, datetime.now().timestamp())
        self.assertEqual(len(self.gui.trades), 1)
        self.assertEqual(self.gui.trades[0].who, "Alice")
        self.assertEqual(self.gui.trades[0].ticker, "AAPL")

    def test_new_div_update(self):
        self.gui.new_div_update("AAPL", 5.0, datetime.now().timestamp())
        self.assertEqual(len(self.gui.dividend), 1)
        self.assertEqual(self.gui.dividend[0].ticker, "AAPL")
        self.assertEqual(self.gui.dividend[0].amount, 5.0)

    def test_new_trans_update(self):
        self.gui.new_trans_update("Alice", 1000.0, datetime.now().timestamp())
        self.assertEqual(len(self.gui.transaction), 1)
        self.assertEqual(self.gui.transaction[0].who, "Alice")
        self.assertEqual(self.gui.transaction[0].amount, 1000.0)

    def test_new_status_update(self):
        self.gui.new_status_update("Alice", 5000.0, datetime.now().timestamp(), [])
        self.assertEqual(len(self.gui.status), 1)
        self.assertEqual(self.gui.status[0].who, "Alice")
        self.assertEqual(self.gui.status[0].balance, 5000.0)

    @patch('gui.save_user_to_json')
    @patch('gui.save_ticket_to_json')
    @patch('gui.save_trade_to_json')
    @patch('gui.save_dividend_to_json')
    @patch('gui.save_transaction_to_json')
    @patch('gui.save_status_to_json')
    def test_save_to_json(self, mock_save_user, mock_save_ticket, mock_save_trade, mock_save_dividend, mock_save_transaction, mock_save_status):
        self.gui.save_to_json()
        mock_save_user.assert_called_once_with(self.gui.users)
        mock_save_ticket.assert_called_once_with(self.gui.tickets)
        mock_save_trade.assert_called_once_with(self.gui.trades)
        mock_save_dividend.assert_called_once_with(self.gui.dividend)
        mock_save_transaction.assert_called_once_with(self.gui.transaction)
        mock_save_status.assert_called_once_with(self.gui.status)

if __name__ == '__main__':
    unittest.main()