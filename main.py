# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from web_scraper.main import get_data
from spreadsheet.main import get_sheet


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    jokers = get_data()
    get_sheet(jokers=jokers)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
