# --- class representing a volunteer ---
class Volunteer:
    # --- constructor ---
    def __init__(self, f_name, l_name, day, email):
        self.f_name = f_name
        self.l_name = l_name
        self.day = day
        self.email = email

    # --- getters ---
    def get_f_name(self):
        return self.f_name

    def get_l_name(self):
        return self.l_name

    def get_day(self):
        return self.day

    def get_email(self):
        return self.email

    # --- setters ---
    def set_day(self, new_day):
        self.day = new_day

    def set_email(self, new_email):
        self.email = new_email

    # --- print ---
    def print(self):
        print("פרטי מתנדב/ת: \n")
        print("שם מלא: " + self.f_name + " " + self.l_name + "\n")
        print("יום קבוע: " + self.day + "\n")
        print("אימייל: " + self.email + "\n")
