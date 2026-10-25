
from datetime import datetime
import json
import os
import random


class Expense:
    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

    def display(self):
        print(
            f"₹{self.amount:.2f} | {self.category} | "
            f"{self.description} | {self.date}"
        )


class PersonalExpense(Expense):
    def __init__(self, amount, category, description):
        super().__init__(amount, category, description)


class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    self.expenses = json.load(file)
            except (json.JSONDecodeError, OSError):
                print("Could not read saved expenses. Starting with an empty list.")
                self.expenses = []

    def save_expenses(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.expenses, file, indent=4)
        except OSError as error:
            print("Could not save expenses:", error)

    def add_expense(self):
        try:
            amount = float(input("Enter amount (₹): "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            category = input("Enter category (Food/Travel/Study/Other): ").strip()
            description = input("Enter description: ").strip()

            if not category or not description:
                print("Category and description cannot be empty.")
                return

            expense = PersonalExpense(amount, category, description)
            self.expenses.append(expense.to_dict())
            self.save_expenses()
            print("Expense added successfully!")

        except ValueError:
            print("Please enter a valid number for the amount.")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded yet.")
            return

        print("\n--- All Expenses ---")
        for item in self.expenses:
            print(
                f"₹{item['amount']:.2f} | {item['category']} | "
                f"{item['description']} | {item['date']}"
            )

    def show_summary(self):
        total = sum(item["amount"] for item in self.expenses)
        print(f"\nTotal expenses: ₹{total:.2f}")

        category_totals = {}
        for item in self.expenses:
            category = item["category"]
            category_totals[category] = (
                category_totals.get(category, 0) + item["amount"]
            )

        if category_totals:
            print("\n--- Category Summary ---")
            for category, amount in category_totals.items():
                print(f"{category}: ₹{amount:.2f}")

    def run(self):
        while True:
            print("\n===== PERSONAL EXPENSE TRACKER =====")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Show Summary")
            print("4. Exit")

            choice = input("Choose an option (1-4): ").strip()

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.show_summary()
            elif choice == "4":
                print("Thank you for using Personal Expense Tracker!")
                break
            else:
                print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
