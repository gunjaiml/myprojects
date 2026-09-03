import random

def get_market_data(symbol:str):
    
    price = round(random.uniform(200,250),2)
    
    return {
        "symbol":symbol.upper(),
        "price":price,
        "previous_close":round(price - random.uniform(-5,5),2),
        "volume":random.randint(1_000_000,50_000_000)
    }