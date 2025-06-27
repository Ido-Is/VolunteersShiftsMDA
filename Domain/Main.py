import random
from datetime import datetime, timedelta
from Scheduler import find_best_assignment  # נניח שהקוד הקודם בקובץ shift_scheduler.py

names = [
    "יוסי", "דני", "רחל", "אורי", "נעמה", "טל", "שירה", "ליאור", "עדי", "עמית",
    "אור", "דניאל", "תמר", "ניצן", "מיקה"
]
days = ["א", "ב", "ג", "ד", "ה", "ו"]
shift_types = ["אטן", "לבן"]


# יצירת רשימת מתנדבים רנדומלית
def generate_random_volunteers(n):
    volunteers = []
    used_names = set()

    for _ in range(n):
        name = random.choice([n for n in names if n not in used_names])
        used_names.add(name)
        fixed_day = random.choice(days)
        available_days = random.sample(days, random.randint(1, 4))
        shift_type = random.choice(shift_types)
        friend = None
        last_shift = datetime.now() - timedelta(days=random.randint(1, 60))

        volunteers.append({
            "name": name,
            "fixed_day": fixed_day,
            "available_days": available_days,
            "shift_type": shift_type,
            "friend": friend,  # נשים חברים לאחר מכן
            "last_shift": last_shift
        })

    # באופן רנדומלי, נוסיף בקשת חבר
    for v in volunteers:
        if random.random() < 0.3:  # 30% מהמתנדבים ירצו חבר
            friend = random.choice([x["name"] for x in volunteers if x["name"] != v["name"]])
            v["friend"] = friend

    return volunteers


# הדפסת השיבוץ
def print_assignment(assignment):
    if not assignment:
        print("לא נמצא שיבוץ חוקי.")
        return
    print("\nשיבוץ משמרות:")
    for shift, assigned in sorted(assignment.items()):
        if not assigned or assigned == (None, None):
            print(f"{shift}: ---")
        elif isinstance(assigned, tuple):
            a, b = assigned
            a_str = a if a else "—"
            b_str = b if b else "—"
            print(f"{shift}: {a_str} + {b_str}")
        else:
            print(f"{shift}: {assigned if assigned else '—'}")


# הרצה
if __name__ == "__main__":
    volunteers = generate_random_volunteers(12)
    best_assignment = find_best_assignment(volunteers)
    print_assignment(best_assignment)
