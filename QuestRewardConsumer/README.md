How to run local:

```
pip install -r requirements.txt
```

```
python -m dataflow --input_topic projects/dfk-reports/subscriptions/Serendale_AuctionSuccessful_Dataflow_test --events_table_name events --postgres_user postgres --postgres_password PASSWORD --postgres_db dfk-reports --postgres_host 35.193.143.140
```

How to run in Dataflow:

```
python -m dataflow --input_topic projects/dfk-reports/subscriptions/Serendale_QuestReward_Dataflow_test --events_table_name events --postgres_user postgres --postgres_password PASSWORD --postgres_db dfk-reports --postgres_host 35.193.143.140 --region us-central1 --temp_location gs://serendale_quest_reward_dataflow/tmp/ --project dfk-reports --runner DataflowRunner --setup_file ./setup.py --job_name quest-reward-events-to-postgres --max_num_workers 5 --worker_machine_type e2-small
```
