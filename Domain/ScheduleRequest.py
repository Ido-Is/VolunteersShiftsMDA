# --- represents a volunteer who sent a request for a shift ---
class ScheduleRequest:
    # --- constructor ---
    def __init__(self, volunteer, shift1, shift2, shift3):
        self.volunteer = volunteer
        self.shift1 = shift1
        self.shift2 = shift2
        self.shift3 = shift3

    def get_volunteer(self):
        return self.volunteer

    def get_shift1(self):
        return self.shift1

    def get_shift2(self):
        return self.shift2

    def get_shift3(self):
        return self.shift3