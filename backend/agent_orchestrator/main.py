from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import clickhouse_connect


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


from orchestrator import run_agent


app = FastAPI(title="SyncRights Agent Orchestrator")


# ==================================================
# P2 CLICKHOUSE LOGGING
# Existing P2 functionality
# ==================================================

def get_clickhouse_client():
    try:
        client = clickhouse_connect.get_client(

            # IMPORTANT:
            # No https:// here
            host="w2u7lzcs7w.ap-south-1.aws.clickhouse.cloud",

            port=8443,

            username="default",

            password="L22_NWwBqIL3V",

            secure=True
        )

        # Create P2 table if it does not exist
        client.command("""
            CREATE TABLE IF NOT EXISTS syncrights_events (
                timestamp DateTime DEFAULT now(),
                version_id String,
                license_status String
            )
            ENGINE = MergeTree()
            ORDER BY timestamp
        """)

        return client

    except Exception as e:
        print(f"P2 ClickHouse connection failed: {e}")
        return None


def log_p2_version_event(
    version_id: str,
    license_status: str
):
    try:

        client = get_clickhouse_client()

        if client is None:
            print("P2 logging skipped: ClickHouse unavailable.")
            return

        data = [[
            version_id,
            license_status
        ]]

        client.insert(
            "syncrights_events",
            data,
            column_names=[
                "version_id",
                "license_status"
            ]
        )

        print(
            f"✅ P2 Data Logged to ClickHouse: "
            f"Version {version_id} | Status: {license_status}"
        )

    except Exception as e:
        print(f"❌ P2 ClickHouse logging failed: {e}")


# ==================================================
# P1 CLICKHOUSE CONNECTION
# Uses P1's own ClickHouse account from .env
# ==================================================

def get_p1_clickhouse_client():

    try:

        client = clickhouse_connect.get_client(

            host=os.getenv("CLICKHOUSE_HOST"),

            port=int(
                os.getenv("CLICKHOUSE_PORT", "8443")
            ),

            username=os.getenv(
                "CLICKHOUSE_USERNAME",
                "default"
            ),

            password=os.getenv(
                "CLICKHOUSE_PASSWORD"
            ),

            database=os.getenv(
                "CLICKHOUSE_DATABASE",
                "syncrights"
            ),

            secure=True
        )


        # ------------------------------------------
        # Ensure P1 events table exists
        # ------------------------------------------

        client.command("""
            CREATE TABLE IF NOT EXISTS events
            (
                timestamp DateTime DEFAULT now(),

                event_type String,

                query_text String,

                track_id String,

                title String,

                artist String,

                version_id String,

                agent_id String,

                conflict_reason String DEFAULT '',

                has_conflict UInt8 DEFAULT 0
            )
            ENGINE = MergeTree()
            ORDER BY timestamp
        """)


        return client


    except Exception as e:

        print(
            f"P1 ClickHouse connection failed: {e}"
        )

        return None


# ==================================================
# P1 EVENT LOGGER
# Logs Catalog Agent identity information
# ==================================================

def log_p1_track_event(

    query_text: str,

    track_id: str,

    title: str = "",

    artist: str = "",

    version_id: str = ""

):

    try:

        client = get_p1_clickhouse_client()


        if client is None:

            print(
                "P1 logging skipped: "
                "ClickHouse unavailable."
            )

            return


        # Data being inserted into P1 ClickHouse

        data = [[

            "query",

            query_text,

            track_id,

            title,

            artist,

            version_id,

            "p1_catalog_agent"

        ]]


        client.insert(

            "events",

            data,

            column_names=[

                "event_type",

                "query_text",

                "track_id",

                "title",

                "artist",

                "version_id",

                "agent_id"

            ]

        )


        print(

            f"✅ P1 EVENT LOGGED: "
            f"{track_id} | "
            f"{title} | "
            f"{artist} | "
            f"{version_id}"

        )


    except Exception as e:

        # Logging failure should NEVER break
        # the actual user request

        print(
            f"❌ P1 ClickHouse logging failed: {e}"
        )


# ==================================================
# P1 CATALOG IDENTITY EXTRACTION
# Extract real catalog data from orchestrator trace
# ==================================================

def extract_catalog_identity(result: dict):

    """
    Extracts real P1 catalog identity information
    from the search_catalog result stored inside
    the orchestrator trace.
    """


    for step in result.get("trace", []):


        # Only look at the catalog search step

        if step.get("tool") != "search_catalog":

            continue


        tool_result = step.get("result", {})


        matches = tool_result.get("matches", [])


        if not matches:

            continue


        # Use top catalog match

        match = matches[0]


        return {

            "track_id": match.get(
                "track_id",
                ""
            ),

            "version_id": match.get(
                "version_id",
                ""
            ),

            "title": match.get(
                "title",
                ""
            ),

            "artist": match.get(
                "artist",
                ""
            )

        }


    # No catalog match found

    return None


# ==================================================
# CORS
# ==================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


# ==================================================
# REQUEST MODEL
# ==================================================

class QueryRequest(BaseModel):

    question: str


# ==================================================
# HEALTH ENDPOINT
# ==================================================

@app.get("/health")

def health():

    return {

        "status": "ok",

        "agent": "orchestrator"

    }


# ==================================================
# MAIN ORCHESTRATOR ENDPOINT
# ==================================================

@app.post("/agent/query")

def query(

    req: QueryRequest,

    background_tasks: BackgroundTasks

):

    try:


        # ==========================================
        # RUN COMPLETE AGENT PIPELINE
        # ==========================================

        result = run_agent(req.question)


        # ==========================================
        # P2 DAY 13 LOGGING
        # EXISTING FUNCTIONALITY
        # ==========================================

        extracted_version = "ver_001_c"

        extracted_status = "Active"


        background_tasks.add_task(

            log_p2_version_event,

            extracted_version,

            extracted_status

        )


        # ==========================================
        # P1 DAY 13 LOGGING
        # ==========================================


        # Extract real track identity from
        # search_catalog result

        catalog_identity = extract_catalog_identity(
            result
        )


        if catalog_identity:


            background_tasks.add_task(

                log_p1_track_event,


                query_text=req.question,


                track_id=catalog_identity.get(

                    "track_id",

                    ""

                ),


                title=catalog_identity.get(

                    "title",

                    ""

                ),


                artist=catalog_identity.get(

                    "artist",

                    ""

                ),


                version_id=catalog_identity.get(

                    "version_id",

                    ""

                )

            )


        else:


            print(

                "P1 logging skipped: "
                "No catalog identity found for this query."

            )


        # ==========================================
        # RETURN NORMAL RESPONSE
        # Logging never affects frontend response
        # ==========================================

        return result


    except Exception as e:


        return {

            "error": f"agent_run_failed: {e}",

            "answer": None,

            "trace": []

        }