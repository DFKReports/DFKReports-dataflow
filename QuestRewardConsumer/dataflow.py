import argparse
import requests
import json
from datetime import datetime
import psycopg2
import psycopg2.extras as extras

from apache_beam import (
    DoFn,
    io,
    ParDo,
    Pipeline,
)
from apache_beam.options.pipeline_options import PipelineOptions
from web3 import Web3
from web3.logs import IGNORE

from constants import (
    ONE_MAINNET,
    ABI,
    GRAPHQL_QUERY,
    GRAPH_URL,
    JEWEL_CONTRACT,
)


class WriteToPostgres(DoFn):
    def __init__(
        self,
        postgres_user,
        postgres_password,
        postgres_db,
        postgres_host,
    ):
        self.postgres_user = postgres_user
        self.postgres_password = postgres_password
        self.postgres_db = postgres_db
        self.postgres_host = postgres_host

    def process(self, events):
        if events:
            conn = psycopg2.connect(
                f"dbname={self.postgres_db} user={self.postgres_user} host={self.postgres_host} password={self.postgres_password}"
            )
            print("Writing to db...")

            cur = conn.cursor()

            columns = events[0].keys()
            query = "INSERT INTO {} ({}) VALUES %s".format(
                events_table_name, ",".join(columns)
            )

            values = [[value for value in event.values()] for event in events]

            extras.execute_values(cur, query, values)
            conn.commit()
            cur.close()
            conn.close()


class fetch_transaction_receipt(DoFn):
    def __init__(
        self,
        web3,
    ):
        self.web3 = web3

    def process(self, element):
        events = []
        data = json.loads(element)
        if tx_hash := data.get("hash"):
            transaction_receipt = self.web3.eth.get_transaction_receipt(tx_hash)
            gas_price = self.web3.eth.gas_price
            gas_used = transaction_receipt["gasUsed"]

            myContract = self.web3.eth.contract(address=transaction_receipt.to, abi=ABI)

            quest_reward_events = (
                myContract.events.QuestReward().processReceipt(
                    transaction_receipt, errors=IGNORE
                )
            )


            for event in quest_reward_events:
                if hasattr(event, "args"):
                    print(f"Processing quest {event.args.questId}...")
                    quantity = event.args.itemQuantity
                    if event.args.rewardItem == JEWEL_CONTRACT:
                        quantity = Web3.fromWei(event.args.itemQuantity, "ether" )
                    events.append(
                        {
                            "event_type": 1,
                            "from_wallet": None,
                            "to_wallet": event.args.player,
                            "epoch_timestamp": int(
                                datetime.fromtimestamp(
                                    int(data.get("timestamp"), 16)
                                ).strftime("%s")
                            ),
                            "quantity": quantity,
                            "contract_hash": event.args.rewardItem,
                            "price_unit_dollar": 0,
                            "transaction_hash": tx_hash,
                            "transaction_gasfee": (gas_price * gas_used) / (10 ** 18),
                            "hero_id": event.args.heroId,
                            "quest_id": event.args.questId
                        },
                    )
                else:
                    print("No quest reward found.")
        return [events]


class add_usdPrice(DoFn):
    def get_usd_price_for_contractHash(self, hash, epoch_date):
        epoch_yesterday = epoch_date - 86400
        query = GRAPHQL_QUERY % {
            "hash": hash,
            "date_lte": epoch_date,
            "date_gte": epoch_yesterday,
        }
        result = requests.post(GRAPH_URL, json={"query": query})
        data = result.json()
        if (tokendata := data.get("data").get("token")) and tokendata.get(
            "tokenDayData"
        ):
            usdprice_str = tokendata.get("tokenDayData")[0].get("priceUSD")
            return round(float(usdprice_str), 3)
        return 0

    def process(self, events):
        if len(events) > 0:
            for event in events:
                event["price_unit_dollar"] = (
                    self.get_usd_price_for_contractHash(
                        hash=event["contract_hash"].lower(),
                        epoch_date=events[0]["epoch_timestamp"],
                    )
                )

        yield events


def run(
    input_subscription,
    postgres_user,
    postgres_password,
    postgres_db,
    postgres_host,
    web3,
    pipeline_args=None,
):
    pipeline_options = PipelineOptions(
        pipeline_args, streaming=True, save_main_session=True
    )

    with Pipeline(options=pipeline_options) as pipeline:
        (
            pipeline
            | "Read from Pub/Sub Topic"
            >> io.ReadFromPubSub(subscription=input_subscription)
            | "Fetch Transaction Receipt"
            >> ParDo(
                fetch_transaction_receipt(
                    web3,
                )
            )
            | "Add usdPrice" >> ParDo(add_usdPrice())
            | "Write to MYSQL"
            >> ParDo(
                WriteToPostgres(
                    postgres_user,
                    postgres_password,
                    postgres_db,
                    postgres_host,
                )
            )
        )


if __name__ == "__main__":
    w3 = Web3(Web3.HTTPProvider(ONE_MAINNET))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_topic",
        help="The Cloud Pub/Sub topic to read from."
        '"projects/<PROJECT_ID>/topics/<TOPIC_ID>".',
    )

    parser.add_argument(
        "--events_table_name",
        help="The table where to write to.",
    )

    parser.add_argument(
        "--postgres_user",
        help="The postgres user..",
    )

    parser.add_argument(
        "--postgres_password",
        help="The password of the Postgres server.",
    )

    parser.add_argument(
        "--postgres_db",
        help="The database of the Postgres table.",
    )

    parser.add_argument(
        "--postgres_host",
        help="The Postgres host address.",
    )

    known_args, pipeline_args = parser.parse_known_args()

    events_table_name = known_args.events_table_name

    run(
        known_args.input_topic,
        known_args.postgres_user,
        known_args.postgres_password,
        known_args.postgres_db,
        known_args.postgres_host,
        w3,
        pipeline_args,
    )
