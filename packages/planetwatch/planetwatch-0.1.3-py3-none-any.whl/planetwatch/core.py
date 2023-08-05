import attr
import click
import pandas as pd
import requests
from pycoingecko import CoinGeckoAPI


@attr.s
class Wallet(object):
    wallet_address = attr.ib()

    def wallet_tests(self):
        wallet_length = len(self.wallet_address)
        if wallet_length != 58:
            raise ValueError(
                f"Wallet address is not value, lengh {wallet_length}: is not 58"
            )

    def get_non_zero_transactions(self):
        response = requests.get(
            f"https://algoexplorerapi.io/idx2/v2/transactions?address={self.wallet_address}&asset-id=27165954&currency-greater-than=0"
        ).json()
        result = []
        for transaction in response["transactions"]:
            data = {}
            data["amount"] = (
                transaction["asset-transfer-transaction"]["amount"] / 1000000
            )
            if (
                transaction["sender"]
                == "ZW3ISEHZUHPO7OZGMKLKIIMKVICOUDRCERI454I3DB2BH52HGLSO67W754"
            ):
                reward = True
            else:
                reward = False

            data["reward"] = reward
            data["timestamp"] = transaction["round-time"]
            result.append(data)

        result = pd.DataFrame(result)
        result["date"] = pd.to_datetime(result.timestamp, unit="s").dt.date
        return result

    def get_prices(self, currency="usd"):
        cg = CoinGeckoAPI()
        prices = cg.get_coin_market_chart_by_id(
            id="planetwatch", vs_currency=currency, days=89
        )["prices"]
        prices = pd.DataFrame(
            prices, columns=["timestamp", f"purchase_price_{currency}"]
        )
        data = pd.to_datetime(prices.timestamp, unit="ms")
        prices["date"] = data.dt.date
        prices["hour"] = data.dt.hour
        return prices[prices.hour == 12]

    @classmethod
    def get_current_price(cls):
        cg = CoinGeckoAPI()
        current_prices = cg.get_price(ids="planetwatch", vs_currencies=["usd", "eur"])[
            "planetwatch"
        ]
        return current_prices

    def get_cost(self, currency):
        transactions = self.get_non_zero_transactions()
        prices = self.get_prices(currency=currency)
        results = transactions[["amount", "date"]][transactions.reward == True].merge(
            prices[[f"purchase_price_{currency}", "date"]]
        )
        current_price = Wallet.get_current_price()[currency]
        results[f"current_value_{currency}"] = (
            Wallet.get_current_price()[currency] * results["amount"]
        )
        results[f"purchase_value_{currency}"] = (
            results[f"purchase_price_{currency}"] * results["amount"]
        )
        results[f"gain_{currency}"] = (
            results[f"current_value_{currency}"] - results[f"purchase_value_{currency}"]
        )
        return results, current_price


@click.command()
@click.option(
    "--wallet", help="Planet Wallet, or list of comma separated wallets", required=True
)
@click.option("--currency", default="usd", help="Currency to convert planets into.")
@click.option(
    "--csv", is_flag=True, help="Export csv of all transactions for given wallet"
)
def cli(currency, csv, wallet):
    wallets = wallet.split(",")
    for w in wallets:

        planet_wallet = Wallet(wallet_address=w)
        results, current_price = planet_wallet.get_cost(currency)
        print("\n")
        print(f"###### For wallet {w}")
        print(f"The current price in {currency} is : {current_price}")
        print(
            results.sum()[
                [
                    "amount",
                    f"current_value_{currency}",
                    f"purchase_value_{currency}",
                    f"gain_{currency}",
                ]
            ].to_string()
        )

        if len(wallets) == 1:
            n = 10
        else:
            n = 5

        print(results.head(n).to_string())

        if csv:
            results.to_csv(f"{w}.csv", index=False)
