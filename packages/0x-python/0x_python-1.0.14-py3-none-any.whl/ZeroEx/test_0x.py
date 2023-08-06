from ZeroEx import ZeroEx

client = ZeroEx()

# /swap/v1/tokens
tokens = client.get_tokens()
print(tokens)

# /swap/v1/price
price = client.get_price(1, "BTC", "ETH")
print(price)

# /swap/v1/prices
prices = client.get_prices()
print(prices)