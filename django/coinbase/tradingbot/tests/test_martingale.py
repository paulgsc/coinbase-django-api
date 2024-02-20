from random import uniform
from django.test import TestCase
from tradingbot.utlis.utlis import DollarGainStrategy

class TestDollarGainStrategy(TestCase):
    def setUp(self):
        # Initial conditions
        self.min_funds_exposure = 10
        self.min_gain_dollars = 1
        self.price_change_threshold = 0.05
        self.strategy = DollarGainStrategy(self.min_funds_exposure, self.min_gain_dollars, self.price_change_threshold)
        self.initial_spot_price = 100  # Initial spot price

    def simulate_spot_price_constant(self, num_iterations):
        # Simulate spot price remaining constant
        for _ in range(num_iterations):
            self.strategy.decide_action(self.initial_spot_price)

    def simulate_spot_price_increase_constant_amount(self, num_iterations):
        # Simulate spot price increasing steadily
        spot_price = 0
        for i in range(num_iterations):
            spot_price += self.min_funds_exposure  # Increasing spot price
            self.strategy.decide_action(spot_price)

    def simulate_spot_price_decrease(self, num_iterations):
        # Simulate spot price decreasing steadily
        for i in range(num_iterations):
            spot_price = self.initial_spot_price - i  # Decreasing spot price
            self.strategy.decide_action(spot_price)

    def simulate_spot_price_fluctuation(self, num_iterations):
        # Simulate spot price fluctuating randomly
        for _ in range(num_iterations):
            random_spot_price = uniform(90, 110)  # Random spot price between 90 and 110
            self.strategy.decide_action(random_spot_price)

    def test_constant_spot_price(self):
        num_iterations = 10
        self.simulate_spot_price_constant(num_iterations)

        # Expected values for constant spot price
        expected_balance = -20
        expected_net_gains_losses = 0
        expected_total_traded_amount = 20
        expected_total_trades = 1

        self.assertEqual(self.strategy.get_balance(), expected_balance)
        self.assertEqual(self.strategy.get_net_gains_losses(), expected_net_gains_losses)
        self.assertEqual(self.strategy.get_total_traded_amount(), expected_total_traded_amount)
        self.assertEqual(self.strategy.get_total_trades(), expected_total_trades)

    def test_constant_price_increase(self):
        num_iterations = 10
        self.simulate_spot_price_increase_constant_amount(num_iterations)

        # Expected values for constant spot price
        expected_balance = 20
        expected_net_gains_losses = 90
        expected_total_traded_amount = 200
        expected_total_trades = 10

        self.assertEqual(self.strategy.get_balance(), expected_balance)
        self.assertEqual(self.strategy.get_net_gains_losses(), expected_net_gains_losses)
        self.assertEqual(self.strategy.get_total_traded_amount(), expected_total_traded_amount)
        self.assertEqual(self.strategy.get_total_trades(), expected_total_trades)

    


