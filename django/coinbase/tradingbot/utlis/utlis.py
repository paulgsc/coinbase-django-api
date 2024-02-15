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
        self.min_funds_exposure = min_funds_exposure  # Minimum funds exposure
        self.min_gain_dollars = min_gain_dollars  # Minimum gain in dollars
        self.price_change_threshold = price_change_threshold  # Price change threshold
        self.balance = 0  # Current balance
        self.total_trades = 0  # Total number of trades executed
        self.total_traded_amount = 0  # Total amount traded
        self.net_gains_losses = 0  # Net gains or losses
        self.cost_basis = 0  # Current cost basis

    def poll_spot_price(self, spot_price):
        # Calculate the potential gain or loss based on the current spot price and cost basis
        potential_gain_loss = spot_price - self.cost_basis

        if potential_gain_loss >= self.min_gain_dollars:
            # Close the excess balance over the required minimum funds exposure
            self.balance += potential_gain_loss - self.min_funds_exposure
            self.net_gains_losses += potential_gain_loss - self.min_funds_exposure
            # Update the cost basis to the current spot price
            self.cost_basis = spot_price
        elif potential_gain_loss < 0:
            # Buy enough funds such that a move up of 5% would yield a gain of 1 dollar
            amount_to_buy = self.min_gain_dollars / self.price_change_threshold
            self.balance -= amount_to_buy
            self.total_traded_amount += amount_to_buy
            self.net_gains_losses -= amount_to_buy
            # Update the cost basis to the current spot price
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
