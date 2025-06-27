from Presentation.VolunteerPresentation import VolunteerPresentation


def main_menu():
    vp = VolunteerPresentation()
    while True:
        print("\n--- מערכת ניהול מתנדבים ---")
        print("1. יצירת בסיס נתונים מקובץ Excel")
        print("2. חיפוש מתנדבים לפי שם פרטי")
        print("3. הוספת מתנדב חדש")
        print("4. מחיקת מתנדב לפי שם פרטי + שם משפחה")
        print("5. עדכון אימייל למתנדב")
        print("6. עדכון יום קבוע למתנדב")
        print("7. הצגת כל המתנדבים")
        print("8. יציאה")
        choice = input("בחר/י פעולה (1-8): ")

        if choice == "1":
            vp.create_database_from_excel()
        elif choice == "2":
            vp.find_by_first_name()
        elif choice == "4":
            vp.remove_volunteer_by_name()
        elif choice == "5":
            vp.update_email_by_name()
        elif choice == "6":
            vp.update_day_by_name()
        elif choice == "7":
            vp.show_all()
        elif choice == "8":
            print("להתראות!")
            break
        else:
            print("בחירה לא חוקית, נסה שוב.")


if __name__ == "__main__":
    main_menu()
