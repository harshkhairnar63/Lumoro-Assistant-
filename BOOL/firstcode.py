class ExpenseTracker:
    def __init__(self):
        self.expenses = {}

    def add_expense(self, date, category, amount, description):
        if date not in self.expenses:
            self.expenses[date] = []
        self.expenses[date].append({
            'category': category,
            'amount': amount,
            'description': description
        })

    def view_expenses(self, date=None):
        if date:
            if date in self.expenses:
                for expense in self.expenses[date]:
                    print(f"Category: {expense['category']}, Amount: {expense['amount']}, Description: {expense['description']}")
            else:
            	print("No expenses found for this date.")
        else:
            for date, expenses in self.expenses.items():
                print(f"Expenses for {date}:")
                for expense in expenses:
                    print(f"Category: {expense['category']}, Amount: {expense['amount']}, Description: {expense['description']}")

    def delete_expense(self, date, category):
        if date in self.expenses:
            self.expenses[date] = [expense for expense in self.expenses[date] if expense['category'] != category]
            if not self.expenses[date]:
                del self.expenses[date]
        else:
            print("No expenses found for this date.")

    def total_expenses(self, date=None):
        total = 0
        if date:
            if date in self.expenses:
                for expense in self.expenses[date]:
                    total += expense['amount']
                return total
            else:
                return 0
        else:
            for expenses in self.expenses.values():
                for expense in expenses:
                    total += expense['amount']
            return total


def main():
    tracker = ExpenseTracker()
    while True:
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Total Expenses")
        print("5. Quit")
        choice = input("Choose an option: ")
        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")
            tracker.add_expense(date, category, amount, description)
        elif choice == "2":
            date = input("Enter date (YYYY-MM-DD) or leave blank for all dates: ")
            if date:
                tracker.view_expenses(date)
            else:
                tracker.view_expenses()
        elif choice == "3":
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            tracker.delete_expense(date, category)
        elif choice == "4":
            date = input("Enter date (YYYY-MM-DD) or leave blank for total expenses: ")
            if date:
                print(f"Total expenses for {date}: {tracker.total_expenses(date)}")
            else:
                print(f"Total expenses: {tracker.total_expenses()}")
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()