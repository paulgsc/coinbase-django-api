class BrokerageAccount:

    def __init__(self, starting_balance):
        self.balance = starting_balance
        self.positions = {}  # Symbol: {shares, average_price}

    def buy(self, symbol, quantity, price):
        if price <= 0 or quantity <= 0:
            raise ValueError("Price and quantity must be positive.")
        if self.balance < price * quantity:
            raise ValueError("Insufficient funds for purchase.")

        self.balance -= price * quantity
        if symbol not in self.positions:
            self.positions[symbol] = {
                "shares": quantity,
                "average_price": price
            }
        else:
            average_price = (self.positions[symbol]["average_price"] * self.positions[symbol]["shares"] + price * quantity) / (self.positions[symbol]["shares"] + quantity)
            self.positions[symbol]["shares"] += quantity
            self.positions[symbol]["average_price"] = average_price

    def sell(self, symbol, quantity, price):
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if symbol not in self.positions or self.positions[symbol]["shares"] < quantity:
            raise ValueError("Insufficient shares to sell.")

        self.balance += price * quantity
        self.positions[symbol]["shares"] -= quantity
        if self.positions[symbol]["shares"] == 0:
            del self.positions[symbol]

    def get_position(self, symbol):
        return self.positions.get(symbol)

    def get_total_equity(self):
        total = self.balance
        for symbol, position in self.positions.items():
            current_price = ...  # Implement logic to fetch current price
            total += position["shares"] * current_price
        return total

    def get_profit_loss(self, symbol):
        position = self.positions.get(symbol)
        if not position:
            return 0
        current_price = ...  # Implement logic to fetch current price
        total_cost = position["shares"] * position["average_price"]
        return (current_price - position["average_price"]) * position["shares"]

    def get_portfolio_profit_loss(self):
        total_profit_loss = 0
        for symbol, position in self.positions.items():
            total_profit_loss += self.get_profit_loss(symbol)
        return total_profit_loss


