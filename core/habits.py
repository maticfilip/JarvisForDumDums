import json
import os
from datetime import date

HFILE="data\habits.json"

def load():
    if not os.path.exists(HFILE):
        return []
    else:
        with open(HFILE,"r") as f:
            content=f.read().strip()
            if not content:
                return []
            return json.loads(content)
        
def save(habits):
    os.makedirs("data", exist_ok=True)
    with open(HFILE,"w") as f:
        json.dump(habits, f, indent=2)

def add_habit(name):
    habits=load()
    habits.append({
        "name":name,
        "created":str(date.today()),
        "history":[]
    })
    save(habits)

def get_habits():
    return load()