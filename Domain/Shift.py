# --- represents a shift: day, type, friend ---
class Shift:
    # --- constructor ---
    def __init__(self, day, type, friend):
        self.day = day
        self.type = type
        self.friend = friend    # ---> Volunteer object

    def get_day(self):
        return self.day

    def get_type(self):
        return self.type

    def get_friend(self):
        return self.friend