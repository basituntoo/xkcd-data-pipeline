import requests
import psycopg2
from datetime import date

DB_CONFIG = {
    "host": "ep-nameless-feather-ahkjabx1-pooler.c-3.us-east-1.aws.neon.tech",
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_plR5sMbJ0jKE",
    "sslmode": "require"
}

LATEST_URL = "https://xkcd.com/info.0.json"
COMIC_URL = "https://xkcd.com/{}/info.0.json"


def get_latest_comic_id():
    return requests.get(LATEST_URL).json()["num"]


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # 1. Ensure ingestion state exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ingestion_state (
            source_name TEXT PRIMARY KEY,
            last_fetched_id INT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        INSERT INTO ingestion_state (source_name, last_fetched_id)
        VALUES ('xkcd', 0)
        ON CONFLICT (source_name) DO NOTHING
    """)

    conn.commit()

    # 2. Read last fetched comic
    cur.execute("""
        SELECT last_fetched_id
        FROM ingestion_state
        WHERE source_name = 'xkcd'
    """)
    last_id = cur.fetchone()[0]

    latest_id = get_latest_comic_id()

    # 3. Fetch only missing comics
    for comic_id in range(last_id + 1, latest_id + 1):
        response = requests.get(COMIC_URL.format(comic_id))

        if response.status_code != 200:
            print(f"Skipping comic {comic_id} (HTTP {response.status_code})")
            continue

        try:
            data = response.json()
        except ValueError:
         print(f"Skipping comic {comic_id} (invalid JSON)")
         continue


        publish_date = date(
            int(data["year"]),
            int(data["month"]),
            int(data["day"])
        )

        cur.execute("""
            INSERT INTO stg_xkcd_comics (
                comic_id, title, publish_date, img_url, alt_text
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (comic_id) DO NOTHING
        """, (
            data["num"],
            data["title"],
            publish_date,
            data["img"],
            data["alt"]
        ))

        cur.execute("""
            UPDATE ingestion_state
            SET last_fetched_id = %s, updated_at = CURRENT_TIMESTAMP
            WHERE source_name = 'xkcd'
        """, (comic_id,))

        conn.commit()
        print(f"Ingested comic {comic_id}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
