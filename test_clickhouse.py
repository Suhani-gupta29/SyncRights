import os
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()

try:

    client = clickhouse_connect.get_client(
        host=os.getenv("CLICKHOUSE_HOST"),
        port=int(os.getenv("CLICKHOUSE_PORT", "8443")),
        username=os.getenv("CLICKHOUSE_USERNAME"),
        password=os.getenv("CLICKHOUSE_PASSWORD"),
        database=os.getenv("CLICKHOUSE_DATABASE"),
        secure=True
    )

    result = client.query("SELECT 1")

    print("SUCCESS!")
    print(result.result_rows)

except Exception as e:
    print("CONNECTION FAILED")
    print(e)