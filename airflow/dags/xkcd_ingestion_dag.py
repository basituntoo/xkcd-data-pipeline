from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import time
import requests

DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

def poll_for_new_comic(max_wait_minutes=30):
    """
    Poll XKCD API until today's comic is available.
    XKCD publishes on Mon/Wed/Fri but not at fixed time.
    """
    start_time = time.time()

    while (time.time() - start_time) < max_wait_minutes * 60:
        response = requests.get("https://xkcd.com/info.0.json", timeout=10)

        if response.status_code == 200:
            data = response.json()
            comic_date = f"{data['year']}-{data['month']}-{data['day']}"
            today = datetime.utcnow().strftime("%Y-%m-%d")

            if comic_date == today:
                print("New comic detected")
                return

        print("Comic not available yet, retrying in 5 minutes...")
        time.sleep(300)

    print("Max polling time reached, proceeding anyway")

def run_ingestion():
    """
    Run your existing ingestion script
    """
    subprocess.run(
        [
            "python",
            "/opt/airflow/workspaces/xkcd-data-pipeline/ingestion/fetch_xkcd.py"
        ],
        check=True
    )

with DAG(
    dag_id="xkcd_ingestion_pipeline",
    default_args=DEFAULT_ARGS,
    description="XKCD incremental ingestion pipeline",
    schedule="0 9 * * 1,3,5",   # Mon/Wed/Fri at 09:00
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["xkcd", "ingestion"],
) as dag:

    wait_for_comic = PythonOperator(
        task_id="poll_for_new_comic",
        python_callable=poll_for_new_comic,
    )

    ingest_xkcd = PythonOperator(
        task_id="fetch_and_load_xkcd",
        python_callable=run_ingestion,
    )

    wait_for_comic >> ingest_xkcd
