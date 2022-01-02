How to run local:

```
pip install -r requirements.txt
```

```
python -m dataflow --input_topic projects/dfk-reports/subscriptions/Serendale_AuctionCreated_Dataflow --table_name auctions --postgres_user postgres --postgres_password PASSWORD --postgres_db dfk-reports --postgres_host 35.193.143.140
```

How to run in Dataflow:

```
python -m dataflow --input_topic projects/dfk-reports/subscriptions/Serendale_AuctionCreated_Dataflow --table_name auctions --postgres_user postgres --postgres_password PASSWORD --postgres_db dfk-reports --postgres_host 35.193.143.140 --region us-central1 --temp_location gs://serendale_auction_created_dataflow/tmp/ --project dfk-reports --runner DataflowRunner --setup_file ./setup.py --worker_machine_type e2-small --job_name auction-created-events-to-postgres
```
