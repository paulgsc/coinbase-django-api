
from django.test import TestCase
from tradingbot.utlis.utlis import DollarGainStrategy

from django.test import TestCase

class DollarGainStrategyTestCase(TestCase):
    def setUp(self):
        # Initialize the DollarGainStrategy with test parameters
        self.min_funds_exposure = 100
        self.min_gain_dollars = 10
        self.price_change_threshold = 0.05  # 5%
        self.strategy = DollarGainStrategy(
            min_funds_exposure=self.min_funds_exposure,
            min_gain_dollars=self.min_gain_dollars,
            price_change_threshold=self.price_change_threshold
        )

        # Generate 15 random spot prices
        self.spot_prices = [100, 105, 98, 110, 115, 120, 105, 100, 95, 85, 90, 88, 92, 98, 105]

    def test_dollar_gain_strategy(self):
        # Simulate the DollarGainStrategy using the spot prices
        for spot_price in self.spot_prices:
            self.strategy.poll_spot_price(spot_price)

        # Set expected values (for demonstration purposes, replace with actual values)
        expected_balance = 1000.0
        expected_net_gains_losses = 50.0
        expected_total_traded_amount = 2000.0
        expected_total_trades = 10

        # Check the balance, net gains/losses, total traded amount, and total trades
        self.assertEqual(self.strategy.get_balance(), expected_balance)
        self.assertEqual(self.strategy.get_net_gains_losses(), expected_net_gains_losses)
        self.assertEqual(self.strategy.get_total_traded_amount(), expected_total_traded_amount)
        self.assertEqual(self.strategy.get_total_trades(), expected_total_trades)
