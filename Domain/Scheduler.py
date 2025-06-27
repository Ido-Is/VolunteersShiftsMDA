# --- performs all logic of scheduling for a certain week ---
from constraint import Problem  # ---> to declare on variables, domains and constraints
from itertools import combinations  # ---> to create couples
from datetime import datetime   # ---> to hold the date of last shift


# --- auxiliary: returns a volunteer by a name ---
def get_volunteer_by_name(volunteers, name):
    for v in volunteers:
        if v["name"] == name:
            return v
    return None


# --- friend constraint: if a volunteer asked for a friend, they'll be together ---
def enforce_friend_constraints(volunteers,  solution):
    for v in volunteers:
        friend = v["friend"]
        if not friend:
            continue    # ---> skipping if there's no friend request

        # --- preparing to save each one's shift ---
        v_found = None
        f_found = None
        # --- searching for shifts ---
        for shift, assigned in solution.items():
            if assigned is None:
                continue    # ---> skipping empty shifts
            # --- checking if each was assigned to this shift as a couple or alone ---
            if isinstance(assigned, tuple):     # ---> if they're together
                if v["name"] in assigned:
                    v_found = shift
                    if friend in assigned:
                        f_found = shift
                elif isinstance(assigned, str):  # ---> if they're alone
                    if v["name"] == assigned:
                        v_found = shift
                    if friend == assigned:
                        f_found = shift
        # --- checking if they're together ---
        if v_found != f_found:
            return False    # ---> solution isn't valid
    return True     # ---> all friends are together


# --- returning the last shit's date by volunteer's name ---
def get_last_shift(volunteers, name):
    return get_volunteer_by_name(volunteers, name)["last shift"]


# --- choosing the volunteer with the oldest date of shift ---
# --- returns a score to a solution ---
def competitive_sort_key(volunteers, solution):
    used = set()
    for val in solution.values():
        if isinstance(val, tuple):
            used.update(v for v in val if v)  # מתנדבים לא None
        elif isinstance(val, str):
            if val:
                used.add(val)
    if not used:
        return float("inf")  # אין מתנדבים – פתרון הכי גרוע
    total_score = 0
    for name in used:
        volunteer = get_volunteer_by_name(volunteers, name)
        if volunteer and volunteer["last_shift"]:
            total_score += volunteer["last_shift"].timestamp()
        else:
            total_score += datetime.max.timestamp()  # אם לא קיים תאריך – גרוע מאוד
    return total_score / len(used)



# --- main function to find the best assignment ---
def find_best_assignment(volunteers):
    days = ["א", "ב", "ג", "ד", "ה", "ו"]
    shift_types = ["אטן", "לבן"]
    problem = Problem()     # ---> a CSP problem object (assignment with constraints)

    # --- for each type of shift in each day of the week ---
    for day in days:
        for shift_type in shift_types:
            shift_name = f"{day}_{shift_type}"

            # --- handling אטן sifts ---
            if shift_type == "אטן":
                # --- list of volunteers that fits this shift in this day ---
                candidates = [
                    v["name"]
                    for v in volunteers
                    if v["shift_type"] == "א" and day in v["available_days"]
                ]
                # --- list of volunteers that this is their fixed day ---
                fixed = [v for v in volunteers if v["name"] in candidates and v["fixed_day"] == day]
                # --- list of available volunteers that this isn't their fixed day ---
                others = [v for v in volunteers if v["name"] in candidates and v["fixed_day"] != day]
                ordered = [v["name"] for v in sorted(fixed, key=lambda x: x["last_shift"])] + \
                    [v["name"] for v in sorted(others, key=lambda x: x["last_shift"])]
                domain = ordered + [None]   # ---> option for an empty day
                ordered.append(None)  # ---> allowing an empty shift
                problem.addVariable(shift_name, domain)

            # --- handling לבן shifts ---
            else:
                candidates = [
                    v["name"]
                    for v in volunteers
                    if v["shift_type"] == "לבן" and day in v["available_days"]
                ]
                valid_pairs = []

                # זוגות חוקיים (כולל התאמת חברים ותיעדוף תאריך ישן יותר)
                for pair in combinations(candidates, 2):
                    v1 = get_volunteer_by_name(volunteers, pair[0])
                    v2 = get_volunteer_by_name(volunteers, pair[1])
                    if v1["friend"] and v1["friend"] != v2["name"]:
                        continue
                    if v2["friend"] and v2["friend"] != v1["name"]:
                        continue
                    valid_pairs.append(pair if v1["last_shift"] <= v2["last_shift"] else (pair[1], pair[0]))

                # הוספת אופציה לשיבוץ חלקי או ריק
                valid_pairs.append((None, None))
                for single in candidates:
                    valid_pairs.append((single, None))
                    valid_pairs.append((None, single))

                problem.addVariable(shift_name, valid_pairs)

    all_solutions = problem.getSolutions()
    valid_solutions = [s for s in all_solutions if enforce_friend_constraints(volunteers, s)]

    if not valid_solutions:
        return None
    best = min(valid_solutions, key=lambda s: competitive_sort_key(volunteers, s))
    return best
