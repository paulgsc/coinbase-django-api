from cryptography.fernet import Fernet
from django.conf import settings


class CryptoUtils:
    @staticmethod
    def generate_encryption_key():
        return Fernet.generate_key()

    @staticmethod
    def encrypt_data(data, encryption_key):
        cipher_suite = Fernet(encryption_key)
        encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
        return encrypted_data

    @staticmethod
    def decrypt_data(encrypted_data, encryption_key):
        cipher_suite = Fernet(encryption_key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
        return decrypted_data


class DollarGainStrategy:
    def __init__(self, min_funds_exposure, min_gain_dollars, price_change_threshold):
        """
        Initialize the DollarGainStrategy object.

        Args:
        - min_funds_exposure: Minimum funds exposure
        - min_gain_dollars: Minimum gain in dollars
        - price_change_threshold: Price change threshold
        """
        self.min_funds_exposure = min_funds_exposure
        self.min_gain_dollars = min_gain_dollars
        self.price_change_threshold = price_change_threshold
        self.balance = 0
        self.total_trades = 0
        self.total_traded_amount = 0
        self.net_gains_losses = 0
        self.cost_basis = 0

    def open_position(self, spot_price):
        """
        Open a new position at the given spot price.

        Args:
        - spot_price: Current spot price
        """
        self.cost_basis = spot_price

    def decide_action(self, spot_price):
        """
        Decide whether to close the position or buy more based on the spot price.

        Args:
        - spot_price: Current spot price
        """

        if self.cost_basis == 0:
            self._buy_more(spot_price=spot_price)

        else: 
            potential_gain_loss = spot_price - self.cost_basis

            if potential_gain_loss >= self.min_gain_dollars:
                self._close_position(potential_gain_loss, spot_price)
            elif potential_gain_loss < 0:
                self._buy_more(spot_price)

    def _close_position(self, potential_gain_loss, spot_price):
        """
        Close the position if the potential gain exceeds the minimum threshold.

        Args:
        - potential_gain_loss: Potential gain or loss
        - spot_price: Current spot price
        """
        self.balance += potential_gain_loss - self.min_funds_exposure
        self.net_gains_losses += potential_gain_loss - self.min_funds_exposure
        self.cost_basis = spot_price

    def _buy_more(self, spot_price):
        """
        Buy more funds if the potential gain is negative.

        Args:
        - spot_price: Current spot price
        """
        amount_to_buy = self.min_gain_dollars / self.price_change_threshold
        self.balance -= amount_to_buy
        self.total_traded_amount += amount_to_buy
        self.net_gains_losses -= amount_to_buy
        self.cost_basis = spot_price
        self.total_trades += 1

    def get_balance(self):
        return self.balance

    def get_total_trades(self):
        return self.total_trades

    def get_total_traded_amount(self):
        return self.total_traded_amount

    def get_net_gains_losses(self):
        return self.net_gains_losses
