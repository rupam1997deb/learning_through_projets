from datetime import datetime
CATEGORY = {
        'I': 'Income',
        'E': 'Expense'
}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime("%d-%m-%Y")
    
    try:
        valid_date = datetime.strptime(date_str, "%d-%m-%Y")
        return valid_date.strftime("%d-%m-%Y")
    except ValueError:
        print("Invalide date format. dd-mm--yyyy")
        return get_date(prompt, allow_default)


def get_amount():
    try: 
        amount = float(input("Enter the amount: "))
        if amount<0:
            raise ValueError("Amount must be a non-negative non-zero value")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()
    
def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORY:
        return CATEGORY[category]
    print("Invalid category. Please enter 'I' for income or 'E' for Expense")
    return get_category()

def get_description():
    return input("Enter a description (Optional): ")
 