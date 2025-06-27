# --- controlling the database ---
from Domain.Volunteer import Volunteer
import pandas as pandas
from sqlalchemy import create_engine, text    # ---> to create engine that connects between the code and the database


class DBManager:
    # --- constructor ---
    def __init__(self):
        # --- creating an engine to connect to SQLite DB ---
        self.engine = create_engine('sqlite:///volunteers.db')   # ---> create volunteers.db if not exist, and connect

    # --- function to fill DB with Excel data ---
    def fill_db_from_excel(self, excel_file):
        data_frame = pandas.read_excel(excel_file)  # ---> reading the file and saving it as DataFrame (table)
        volunteers = []  # ---> here will be a list of all volunteers
        # --- creating Volunteer instances and adding each one to the list ---
        for index, row in data_frame.iterrows():
            volunteers.append(Volunteer(f_name=row['שם פרטי'], l_name=row['שם משפחה'],
                                        day=row['יום קבוע'], email=row['אימייל']))
        # --- parsing the list of instances to dictionary (to allow creation of DataFrame ---
        # --- saving it as a DataFrame to send to SQLite ---
        data_frame_sql = pandas.DataFrame([v.__dict__ for v in volunteers])
        # --- sending the DataFrame of Volunteers to SQLite as a table ---
        data_frame_sql.to_sql('volunteers', con=self.engine, if_exists='replace', index=False)

    # --- adding a new volunteer ---
    def add_volunteer(self, volunteer):
        with self.engine.connect() as conn:
            query = text("""
                   INSERT INTO volunteers (f_name, l_name, day, email)
                   VALUES (:f_name, :l_name, :day, :email)
               """)
            conn.execute(query, {
                "f_name": volunteer.get_f_name(),
                "l_name": volunteer.get_l_name(),
                "day": volunteer.get_day(),
                "email": volunteer.get_email()
            })
            conn.commit()  # ---> הוספת commit

    # --- removing volunteer by first and last name ---
    def remove_volunteer(self, volunteer):
        with self.engine.connect() as conn:
            query = text("DELETE FROM volunteers WHERE f_name = :f_name AND l_name = :l_name")
            result = conn.execute(query, {
                "f_name": volunteer.get_f_name(),
                "l_name": volunteer.get_l_name()
            })
            if result.rowcount > 0:
                print("✅ המתנדב הוסר בהצלחה.")
                conn.commit()  # ---> הוספת commit
            else:
                print("⚠️ לא נמצא מתנדב למחיקה.")

        # --- updating volunteer's email by first and last name ---
    def update_email(self, volunteer, new_email):
        with self.engine.connect() as conn:
            # עדכון האימייל במסד הנתונים
            result = conn.execute(
                text("UPDATE volunteers SET email = :email WHERE f_name = :f_name AND l_name = :l_name"),
                {
                    "email": new_email,
                    "f_name": volunteer.get_f_name(),
                    "l_name": volunteer.get_l_name()
                }
            )

            # אם עדכון בוצע
            if result.rowcount > 0:
                print("✅ האימייל עודכן בהצלחה.")
                conn.commit()  # ---> כבר קיים commit
            else:
                print("⚠️ לא נמצא מתנדב לעדכון.")

    # --- updating volunteer's day by first and last name ---
    def update_day(self, volunteer, new_day):
        with self.engine.connect() as conn:
            result = conn.execute(
                text("UPDATE volunteers SET day = :day WHERE f_name = :f_name AND l_name = :l_name"),
                {
                    "day": new_day,
                    "f_name": volunteer.get_f_name(),
                    "l_name": volunteer.get_l_name()
                }
            )
            if result.rowcount > 0:
                print("✅ היום הקבוע עודכן בהצלחה.")
                conn.commit()  # ---> הוספת commit
            else:
                print("⚠️ לא נמצא מתנדב לעדכון יום קבוע.")

    # --- returning a list of all matches for name of Volunteer ---
    def find_by_first_name(self, first_name):
        query = "SELECT * FROM volunteers WHERE f_name = :first_name"
        df = pandas.read_sql_query(query, self.engine, params={"first_name": first_name})
        volunteers = [
            Volunteer(f_name=row['f_name'], l_name=row['l_name'],
                      day=row['day'], email=row['email'])
            for _, row in df.iterrows()
        ]
        return volunteers

    # --- getting a table of all volunteers ---
    def get_all_volunteers(self):
        query = "SELECT * FROM volunteers"
        data_frame = pandas.read_sql(query, con=self.engine)
        return data_frame

    # --- check if volunteer exists by first name and last name ---
    def volunteer_exists(self, f_name, l_name):
        query = text("""
            SELECT COUNT(*) as count
            FROM volunteers
            WHERE f_name = :f_name AND l_name = :l_name
        """)
        with self.engine.connect() as conn:
            result = conn.execute(query, {"f_name": f_name, "l_name": l_name})
            count = result.scalar()
            return count > 0
