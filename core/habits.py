import json
import os
from datetime import date, timedelta

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

def delete_habit(name):
    habits=load()
    habits=[h for h in habits if h["name"]!=name]
    save(habits)

def mark_habit_done(name):
    habits=load()
    today=str(date.today())
    for h in habits:
        if h["name"]==name:
            if today not in h["history"]:
                h["history"].append(today)
    save(habits)

def unmark_habit_done(name):
    habits=load()
    today=str(date.today())
    for h in habits:
        if h["name"]==name:
            if today in h["history"]:
                h["history"].remove(today)
    save(habits)

def get_last_7_days(habit):
    history=habit["history"]
    today=date.today()
    result=[]
    for i in range(6,-1,-1):
        day=str(today-timedelta(days=i))
        result.append(day in history)
    return result