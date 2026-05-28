import pandas as pd
from datetime import datetime
import os
import json

DB_CSV = "records.csv"

class DataManager:
    def __init__(self, path=DB_CSV):
        self.path = path
        if not os.path.exists(self.path):
            pd.DataFrame(columns=["timestamp","score","angles","messages"]).to_csv(self.path,index=False)

    def save_record(self, score, angles, messages):
        if os.path.exists(self.path):
            df = pd.read_csv(self.path)
        else:
            df = pd.DataFrame(columns=["timestamp","score","angles","messages"])
        rec = {
            "timestamp": datetime.now().isoformat(),
            "score": score,
            "angles": json.dumps(angles),
            "messages": ";".join(messages) if isinstance(messages, (list,tuple)) else str(messages)
        }
        df = pd.concat([df, pd.DataFrame([rec])], ignore_index=True)
        df.to_csv(self.path, index=False)

    def load_records(self):
        if os.path.exists(self.path):
            df = pd.read_csv(self.path)
            df["angles_parsed"] = df["angles"].apply(lambda s: json.loads(s) if pd.notna(s) and s!="" else {})
            return df
        return pd.DataFrame()
