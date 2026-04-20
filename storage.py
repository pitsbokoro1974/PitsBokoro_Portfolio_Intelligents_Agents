import pandas as pd
import sqlite3
import json


class StorageAgent:
    def __init__(self, output_prefix="papers"):
        # Base filename used for all saved outputs (csv, json, db)
        self.base_filename = output_prefix

    def _prepare_dataframe(self, papers):
        # Convert list of dictionaries (papers) into a pandas DataFrame
        df = pd.DataFrame(papers)

        # If no data, just return empty DataFrame
        if df.empty:
            return df

        # Loop through each column in the DataFrame
        for col in df.columns:
            # Convert lists/dictionaries into JSON strings
            # This is important because CSV/SQLite can't directly store complex objects
            df[col] = df[col].apply(
                lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x
            )

        return df

    def save(self, papers):
        # If input list is empty, stop early
        if not papers:
            print("[Storage] No data to save.")
            return

        # Convert raw data into a clean DataFrame
        df = self._prepare_dataframe(papers)

        # If something went wrong and DataFrame is empty, stop
        if df.empty:
            print("[Storage] DataFrame is empty after processing.")
            return

        # ---------- Save as CSV ----------
        csv_file = f"{self.base_filename}.csv"
        df.to_csv(csv_file, index=False)  # index=False avoids adding row numbers
        print(f"[Storage] Overwrote CSV: {csv_file}")

        # ---------- Save as JSON ----------
        json_file = f"{self.base_filename}.json"
        # orient="records" → list of dictionaries
        # indent=2 → pretty formatting
        df.to_json(json_file, orient="records", indent=2)
        print(f"[Storage] Overwrote JSON: {json_file}")

        # ---------- Save as SQLite database ----------
        db_file = f"{self.base_filename}.db"

        # Create (or connect to) SQLite database file
        conn = sqlite3.connect(db_file)

        # Write DataFrame to SQL table named "papers"
        # if_exists="replace" → overwrite table if it already exists
        df.to_sql("papers", conn, if_exists="replace", index=False)

        # Always close connection to avoid corruption/locks
        conn.close()

        print(f"[Storage] Overwrote SQLite DB: {db_file}")