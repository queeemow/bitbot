from urllib.request import urlopen
import json


class BitcoinAPI:

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_jsonparsed_data() -> object:
        URL = ("https://blockchain.info/ticker")

        response = urlopen(URL)
        data = response.read().decode("utf-8")
        return json.loads(data)["USD"]
