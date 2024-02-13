from sqlalchemy.types import FLOAT, SMALLINT, INT, TIMESTAMP

columns__dict = {
    'Open time': TIMESTAMP,  # 0
    'Open': FLOAT,  # 1
    'High': FLOAT,  # 2
    'Low': FLOAT,  # 3
    'Close': FLOAT,  # 4
    'Volume': FLOAT,  # 5
    'Close time': TIMESTAMP,  # 6
    'Quote asset volume': FLOAT,  # 7
    'Number of trades': INT,  # 8
    'Taker buy base asset volume': FLOAT,  # 9
    'Taker buy quote asset volume': FLOAT,  # 10
    'Ignore': SMALLINT  # 11
}

columns__list = list(columns__dict.keys())
