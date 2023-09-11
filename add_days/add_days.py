# the user enters a day and a number of days and the program 
# adds the days and returns the date

from datetime import date, timedelta

def main():
    user_date = get_user_Date()
    print(user_date.strftime("%A, %d %B %Y"))
    print(f"The date will be {(user_date + get_days_no()).strftime('%A, %d %B %Y')}.")

def get_user_Date():
    # Returns the date ans an instanciated object user_date
    while True:
        try:
            u_d = list(map(int, input("Enter a date (YYYY-MM-DD): ").split("-")))
            user_date = date(u_d[0], u_d[1], u_d[2])
            return user_date
        except ValueError:
            print("What the fuck?")

def get_days_no():
    # Gets the value of the days to add and returns the instanciated object
    while True:
        try:
            return timedelta(days=int(input("Enter no. of days to add: ")))
        except ValueError:
            print("Enter a number")

if __name__ == "__main__":
    main()
