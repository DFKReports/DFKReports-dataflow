How to run local:

```
pip install -r requirements.txt
```

```
python -m dataflow --input_topic projects/dfk-reports/subscriptions/Serendale_AuctionSuccessful_Dataflow_test --events_table_name events --auctions_table_name auctions --postgres_user postgres --postgres_password PASSWORD --postgres_db dfk-reports --postgres_host 35.193.143.140
```

How to run in Dataflow:

```
python -m dataflow --input_topic projects/dfk-reports/subscriptions/Serendale_AuctionSuccessful_Dataflow_test --events_table_name events --auctions_table_name auctions --postgres_user postgres --postgres_password PASSWORD --postgres_db dfk-reports --postgres_host 35.193.143.140 --region us-central1 --temp_location gs://serendale_auction_successful_dataflow/tmp/ --project dfk-reports --runner DataflowRunner --setup_file ./setup.py --worker_machine_type e2-small --job_name auction-successful-events-to-postgres
```
