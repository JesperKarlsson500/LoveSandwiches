import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

"""
sales = SHEET.worksheet('sales')
data = sales.get_all_values()
print(data)
"""


def get_sales_data():
    """
    get sales imput figures from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        # runs a while loop, that asks the user for data
        print("please enter sales data from the last market.")
        print("data should be six numbers, seperated by commas")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("input you data here:")
        # print(f"the data provided is {data_str}")

        sales_data = data_str.split(",")
        # It converts the string of data from the user into a list of values
        # ("1", "2", "3", "4", "5", "6")

        if validate_data(sales_data):
            """
            And then we use a single if statement to
            call our validate data function.
            Passing it our sales data list.
            """
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    This function checks for errors.
    If there are no errors, it will return True
    """
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        # values = ["1", "2", "3", "4", "5", "6"]
        [int(value) for value in values]
        """
        for each value in the values list, convert that value into and interger
        """
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    return stock_data


print("Welcome to love sandwiches data automation")
stock_data = main()


def get_stock_value(data):
    """
    retrieve worksheet headings and print them out in a 
    dictionary together with calculated 
    sandwiches to make for tomorrows market
    """
    headings = SHEET.worksheet("stock").get_all_values()[0]

    print("Make the following numbers of sandwiches for the next market:\n")

    return {heading: data for heading, data in zip(headings, data)}


stock_values = get_stock_value(stock_data)
print(stock_values)
