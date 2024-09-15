import pandas as pd
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description

class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = '%d-%m-%Y'

    @classmethod
    def initialize_csv(cls):
        try:
            load_csv = pd.read_csv(cls.CSV_FILE)
            
        except FileNotFoundError :
            df = pd.DataFrame(columns = cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
                'date': date,
                'amount': amount,
                'category': category,
                'description': description,
        }
        with open(cls.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print('Entry added Successfully')

    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'], format=cls.DATE_FORMAT)
        
        start_date = datetime.strptime(start_date, cls.DATE_FORMAT)
        end_date = datetime.strptime(end_date, cls.DATE_FORMAT)

        # mask = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('\nNo transaction found in the given date of range')
        else:
            print(f'\nTransactions from {start_date.strftime(cls.DATE_FORMAT)} to {end_date.strftime(cls.DATE_FORMAT)}\n--------------------------------------------')
            formatter = {'date': lambda x: x.strftime(cls.DATE_FORMAT) }
            print(filtered_df.to_string(index=False, formatters=formatter),'\n--------------------------------------------')

            total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
            total_expense = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()
            print("\nSummary:")
            print(f'Total Income: ${total_income:.2f}')
            print(f'Total Expense: ${total_expense:.2f}')
            print(f'Net Savings: ${total_income-total_expense:.2f}\n--------------------------------------------')
            
        return filtered_df
        

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or Press enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)
    
# def plot_transactions(df):
#     df['income'] = df.apply(lambda x: x['amount'] if x['category'] == 'Income' else 0, axis=1)
#     df['expense'] = df.apply(lambda x: x['amount'] if x['category'] == 'Expense' else 0, axis=1)

#     ax = df.plot(x='date', y='income', marker='o', label='Income')
#     ax = df.plot(x='date', y='expense', marker='s', ax=ax, secondary_y=True, label='Expense')

#     ax.grid()
#     plt.show()

def plot_transactions(df):
    # Create 'income' and 'expense' columns based on 'category'
    df['income'] = df.apply(lambda x: x['amount'] if x['category'] == 'Income' else 0, axis=1)
    df['expense'] = df.apply(lambda x: x['amount'] if x['category'] == 'Expense' else 0, axis=1)

    # Create figure and axis
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot income on the primary axis
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Income ($)', color=color)
    ax1.plot(df['date'], df['income'], marker='o', color=color, label='Income', linestyle='-', linewidth=2, markersize=8)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create secondary axis for expense
    ax2 = ax1.twinx()  # Instantiate a second y-axis that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Expense ($)', color=color)
    ax2.plot(df['date'], df['expense'], marker='s', color=color, label='Expense', linestyle='--', linewidth=2, markersize=8)
    ax2.tick_params(axis='y', labelcolor=color)

    # Title and grid
    plt.title('Income and Expense Over Time', fontsize=16, fontweight='bold')
    ax1.grid(True, linestyle='--', linewidth=0.5)

    # Formatting the x-axis with proper date format
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m-%Y'))
    fig.autofmt_xdate()  # Auto formats the dates for better readability

    # Add legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Display the plot
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()



def main():
    while True:
        print('1. Add a new transaction')
        print('2. View transactions and summary within a date range')
        print('3. Exit')
        choice = input('Enter your choice (1-3): ')

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transaction(start_date, end_date)
            if input("Do you want to to see a plot? (y/n)") =="y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting....")
            break
        else:
            print("Invalid choice. Enter 1,2 or 3.")


if __name__ == "__main__":
    main()