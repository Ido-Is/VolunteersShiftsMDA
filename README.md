# VolunteersShiftsMDA
An intelligent, constraint-based scheduling system, designed to assign volunteers to weekly shifts, taking into account their preferences and availability. 
## Features

#) Automatically assigns volunteers to shifts based on their **preferred days** and **preferred shift type**  
#) Supports **fixed days** for volunteers, while allowing flexibility in case of missing volunteers  
#) Guarantees volunteers who wish to serve with a specific friend are scheduled together (or not at all)  
#) Prioritizes volunteers who have waited the longest since their last shift, for fair rotation  
#) Handles **partial solutions** gracefully (missing volunteers or completely empty days)  
#) Imports volunteer data directly from an **Excel spreadsheet** exported from Google Forms  
#) Easily extendable for future enhancements like GUIs, email notifications, or web dashboards

---

## How It Works

#) Each day has exactly three volunteer spots:
  - **1 volunteer** for Shift A
  - **2 volunteers** for Shift B
     
#) The algorithm:
  - Considers volunteer fixed days as the highest priority
  - Honors each volunteer's preferred shift type
  - Fulfills friend-pair requests where possible
  - In case of multiple volunteers competing for the same spot, assigns the volunteer whose last shift was furthest in the past
  - Allows incomplete shifts or empty days if there are no candidates

#) Constraints are modeled and solved using a **constraint satisfaction problem (CSP)** approach.

---

## Technologies Used

| Technology         | Purpose                                      |
|--------------------|----------------------------------------------|
| **Python 3**       | Main programming language                    |
| **python-constraint** | Constraint satisfaction problem solver  |
| **pandas**         | Efficient data handling and manipulation     |
| **openpyxl**       | Reading/writing Excel files                  |

---
