import pandas as pandas

# --- creates a list of ScheduleRequest from xlsx file ---
class ScheduleRequestListCreator:
    # --- constructor ---
    def __init__(self, requests_list):
        self.requests_list = requests_list

    def __read_xlsx(self, path):
        lst = []
        file = pandas.read_excel(path)
        for row in file.iloc[1:].iterrows():      # ---> skipping first line of headers
            f_name = row['שם פרטי']
            l_name = row['שם משפחה']
            day_type_1 = row['משמרת ראשונה']
            friend1 = row['חבר/ה למשמרת הראשונה - שם מלא']
            day_type_2 = row['משמרת שנייה']
            friend2 = row['חבר/ה למשמרת השנייה - שם מלא']
            day_type_3 = row['משמרת שלישית']
            friend3 = row['חבר/ה למשמרת השלישית - שם מלא']

            # המשך: להמיר לאובייקטים