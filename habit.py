import json 
from datetime import datetime, timedelta

# file to store habit data

DATA_FILE = "habit_data.json"

def load_data():
  """ Load habit data from a JSON file"""

  try:
    with open(DATA_FILE, 'r') as file:
      return json.load(file)
  except FileNotFoundError:
    return {}
  
def save_data(data):
  """Save habit data to a JSON file."""
  with open(DATA_FILE, 'w') as file:
    json.dump(data, file, indent=4)

def add_habit(data):
  """Add new habit."""
  name = input("Enter the habit name: ")
  category = input("Enter the category for this habit (e.g., health, productivty): ")
  habit = {
    "category": category,
    "dates": [], # list of dates the habit was completed
  }

  data[name] = habit
  save_data(data)
  print(f"Habit '{name}' added successfully!")

def mark_habit(data):
  """Mark a habit as completed for today."""
  name = input("Enter the habit name to mark as completed: ")
  if name not in data:
    print("Habit not found. Please add the habit first.")
    return
  
  today = datetime.now().strftime("%Y-%m-%d")
  if today not in data[name]["dates"]:
    print("Habit already marked as completed for today.")
  else:
    data[name]["dates"].append(today)
    save_data(data)
    print(f"Habit '{name}' marked as completed for {today}")

def view_habits(data):
  """View all habits and their status."""
  if not data:
    print("No habits found. Please add some habits first.")


  print("\nHabits: ")
  for name, details in data.items():
    print(f"Name: {name}")
    print(f"Category: {details['category']}")
    print(f"completion Dates: {', '.join(details['dates'])}")
    print("-" * 30)


def calculate_streak(dates):
  """Calulate the current and longest streak for a habit"""
  if not dates:
    return 0,0 
  
  dates = sorted(datetime.strptime(date, "%Y-%m-%d") for date in dates)
  current_streak = 1
  longest_streak = 1
  last_date = dates[0]


  for date in dates[1:]:
    if date == last_date + timedelta(days=1):
      current_streak += 1
      longest_streak = max(longest_streak, current_streak)
    else:
      current_streak = 1
    last_date = date
  # check if the current streak is active
  today = datetime.now()
  if today - last_date > timedelta(days=1):
    current_streak = 0

  return current_streak, longest_streak

def view_streaks(data):
  """View streaks for all habits."""
  if not data:
    print("No habits  found. Please add some habits first")
    return
  
  print("\nHabit Streaks:")
  for name, details in data.items():
    current_streak, longest_streak = calculate_streak(details["dates"])
    print(f"Name: {name}")
    print(f"Current Streak: {current_streak} days")
    print(f"Longest Streak: {longest_streak} days")
    print("-"*30)

def main():
  """Main function to run the habit tracker."""

  print("Welcome to the habit Tracker!")
  data = load_data()

  while True:
    print("\nMenu: ")
    print("1. Add Habit")
    print("2. Mark Habit as Completed")
    print("3. View All Habits")
    print("4. View Streaks")
    print("5. Exit")


    choice = input("Enter your choice: ")
    
    if choice == "1":
      add_habit(data)
    elif choice == "2":
      mark_habit(data)
    elif choice == "3":
      view_habits(data)
    elif choice == "4":
      view_streaks(data)
    elif choice == "5":
      print("Goodbye!")
      break
    else:
      print("Invalid choice. Please try again.")


if __name__ == "__main__":
  main()