import os
from typing import Any

import gspread
import gspread_formatting
from gspread_formatting import DataValidationRule, BooleanCondition, set_data_validation_for_cell_range
from oauth2client.service_account import ServiceAccountCredentials


def get_sheet(jokers: list[dict[str, Any]], sheet_name: str = "Belatro be ballin"):
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # Get the current directory of your script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to your JSON key file
    json_keyfile_path = os.path.join(current_dir, 'belatro-ballin-b11a916a6442.json')

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(filename=json_keyfile_path, scopes=scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open(sheet_name)

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)

    keys = list(jokers[0].keys())

    keys.append("Gold Sticker")

    # add table-top headers - view total progression
    joker_count = '="Total Jokers " & COUNTIF(F3:F152, TRUE) & "/" & 150'
    percentage = '=ROUND(COUNTIF(F3:F152, TRUE) / COUNTA(F3:F152) * 100, 2) & "%"'
    headers = ['', joker_count, percentage]

    sheet_instance.update("A1:F2", [headers, keys], value_input_option='USER_ENTERED')

    jokers_to_update = []

    for joker in jokers:
        jokers_to_update.append(
            [joker["pos"], joker["name"], '=IMAGE(\"{}\", 3)'.format(joker["image"]), joker["rarity"], joker["cost"],
             False])


    last_joker_index = jokers[-1]["pos"] + 2

    gspread_formatting.set_row_height(sheet_instance, '3:152', 200)
    gspread_formatting.set_column_widths(sheet_instance,
                                         [("A", 75), ("B", 135), ("C", 150), ("D", 100), ("E", 75), ("F", 120)])
    sheet_instance.update(f'A3:F{last_joker_index}', jokers_to_update, value_input_option='USER_ENTERED')
    sheet_instance.set_basic_filter(f"A2:F{last_joker_index}")

    validation_rule = DataValidationRule(
        BooleanCondition('BOOLEAN', ['TRUE', 'FALSE']),
        showCustomUi=True)

    set_data_validation_for_cell_range(sheet_instance, f'F3:F{last_joker_index}', validation_rule)
    sheet_instance.format(f"A2:F{last_joker_index}", {
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE",
        "textFormat": {
            "fontSize": 12,
            "bold": True
        }
    })
