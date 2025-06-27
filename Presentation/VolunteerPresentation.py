# --- class to handle Volunteers-related presentation ---
from Data.DBManager import DBManager
from Domain.Volunteer import Volunteer
from tabulate import tabulate   # ---> to nicely print the table of volunteers


class VolunteerPresentation:
    def __init__(self):
        self.db_manager = DBManager()

    def create_database_from_excel(self):
        print("בחרת ליצור בסיס נתונים לפי קובץ אקסל. הזן את השם של הקובץ, ובסופו .xlsx:")
        excel_file = input()
        self.db_manager.fill_db_from_excel(excel_file)

    def find_by_first_name(self):
        name = input("הזן שם פרטי לחיפוש: ")
        results = self.db_manager.find_by_first_name(name)
        for v in results:
            print(f"{v.get_f_name()} {v.get_l_name()}, יום קבוע: {v.get_day()}, אימייל: {v.get_email()}")

    def remove_volunteer_by_name(self):
        f_name = input("שם פרטי של המתנדב למחיקה: ")
        l_name = input("שם משפחה של המתנדב למחיקה: ")
        volunteer = Volunteer(f_name=f_name, l_name=l_name, day=None, email=None)
        self.db_manager.remove_volunteer(volunteer)
        print("המתנדב הוסר (אם נמצא).")

    def update_email_by_name(self):
        f_name = input("שם פרטי של המתנדב: ")
        l_name = input("שם משפחה של המתנדב: ")
        if not self.db_manager.volunteer_exists(f_name, l_name):
            print("אין מתנדב/ת עם השם שהוזן, נסו שנית.")
        else:
            new_email = input("אימייל חדש: ")
            volunteer = Volunteer(f_name=f_name, l_name=l_name, day=None, email=None)
            self.db_manager.update_email(volunteer, new_email)
            print("האימייל עודכן.")
            # --- שינוי קל בבדיקה המיידית ---
            results = self.db_manager.find_by_first_name(f_name)
            for v in results:
                print(f"--- (כל התוצאות לשם {f_name}): {v.get_f_name()} {v.get_l_name()}, אימייל: {v.get_email()}")
                if v.get_l_name() == l_name:
                    print(f"--- נמצא מתאים: {v.get_f_name()} {v.get_l_name()}, אימייל: {v.get_email()}")

    def update_day_by_name(self):
        f_name = input("שם פרטי של המתנדב: ")
        l_name = input("שם משפחה של המתנדב: ")
        new_day = input("יום קבוע חדש: ")
        volunteer = Volunteer(f_name=f_name, l_name=l_name, day=None, email=None)
        self.db_manager.update_day(volunteer, new_day)
        print("היום הקבוע עודכן (אם נמצא).")
        # --- הוספה של הדפסה מיידית לאחר העדכון ---
        results = self.db_manager.find_by_first_name(f_name)
        for v in results:
            print(f"--- (כל התוצאות לשם {f_name}): {v.get_f_name()} {v.get_l_name()}, יום קבוע: {v.get_day()}")
            if v.get_l_name() == l_name:
                print(f"--- נמצא מתאים: {v.get_f_name()} {v.get_l_name()}, יום קבוע: {v.get_day()}")

    def show_all(self):
        print("\n--- מנסה להציג את כל המתנדבים ---")
        try:
            df = self.db_manager.get_all_volunteers()
            if df.empty:
                print("אין מתנדבים בבסיס הנתונים.")
            else:
                print("\n--- כל המתנדבים (מהדאטה בייס) ---")
                print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        except Exception as e:
            print(f"⚠️ אירעה שגיאה בעת הצגת המתנדבים: {e}")
