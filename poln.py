# Import necessary modules
import os
import datetime
import openpyxl
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Constants
NONE_REPLACEMENT_VALUE = '&#8203; ' * 9  # 9 symbols of zero width for replacing empty cells
TABLE_COLUMN_WIDTH_DEFAULT = 14  # Default table column width
NUM_COLS_DEFAULT_VALUE = 10  # Default number of columns

# Formats for upper part of the table
up_formats = [
    {"row_num": 3, "col_width": 3, "num_cols": NUM_COLS_DEFAULT_VALUE}
]

# Formats for lower part of the table
row_formats = [{"row_num": i, "col_width": i, "num_cols": NUM_COLS_DEFAULT_VALUE} for i in range(4, 25)]

def get_today_date() -> datetime.date:
    """Returns today's date"""
    return datetime.date.today()

def load_excel_workbook(file_path: str) -> openpyxl.Workbook:
    """Loads an Excel workbook from a file"""
    try:
        return openpyxl.load_workbook(file_path)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_table_row(row: tuple, col_width: int, num_cols: int) -> list:
    """Generates a list of words from a table row"""
    formatted_row = [str(cell) if cell is not None else NONE_REPLACEMENT_VALUE for cell in row]
    if num_cols:
        return formatted_row
    else:
        return formatted_row[:3]

def generate_table_header() -> str:
    """Generates the table header"""
    header = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
  <style>
  /* Set white background color for body */
   body {
      background-color: rgb(0, 0, 0);
      margin: 0; /* Remove default margins */
    }
    /* Create grid container with black background */
    #grid-container {
      display: grid;
      grid-template-columns: repeat(10, 1fr); /* Set number and width of columns */
      grid-template-rows: repeat(25, auto); /* Set row height based on content */
      grid-gap: 5px; /* Set gap between grid cells */
      background-color: rgb(14, 11, 11); /* Set grid container background color */
      width: 100%; /* Set grid container width */
      height: 100vh; /* Set grid container height to fill entire screen */
    }
    /* Style grid cells */
    #grid-container > div {
      background-color: rgb(255, 255, 255); /* Set grid cell background color */
      color: rgb(0, 0, 0); /* Set grid cell text color */
      display: flex; /* Enable flexbox layout */
      align-items: center; /* Center text vertically */
      justify-content: center; /* Center text horizontally */
      font-size: 18px; /* Set font size */
      padding: 0px; /* Remove internal padding */
    }
    .menu-button {
      display: inline-block;
      margin: 20px;
      padding: 10px 20px;
      color: black; /* Set button text color */
      text-decoration: none;
      border-radius: 5px;
      border: none; /* Remove borders */
      /* Add animation properties */
      background-image: linear-gradient(yellow);
      background-size: 800% 800%;
      animation: gradient 8s ease infinite alternate; /* Add alternate */
    }
    .container {
      width: 80%;
      margin: auto;
      text-align: center;
    }
  </style>
</head>
<body> 
<div class="container">
<!-- Кнопка "назад" -->
<button onclick="window.location.href='index.html';" class="menu-button">Назад</button>
</div>
<div id="grid-container">\n'''
    try:
        return header
    except Exception as e:
        print(f"Error: {e}")
        return ""

def is_row_all_none(row: tuple) -> bool:
    """Проверяет, состоит ли вся строка только из значений None"""
    return all(cell is None for cell in row)

def generate_table_body(workbook: openpyxl.Workbook, row_formats: list) -> str:
    """Генерирует тело таблицы"""
    table_body = ""
    for row_format in row_formats:
        for row in workbook.active.iter_rows(values_only=True, min_row=row_format["row_num"], max_row=row_format["row_num"]):
            if is_row_all_none(row):
                continue  # Пропускаем строку, если она состоит только из значений None
            row_as_list = list(row)
            row_as_list[3] = NONE_REPLACEMENT_VALUE if row_as_list[3] is None else str(row_as_list[3])#
            row = tuple(row_as_list)
            words = generate_table_row(row, row_format["col_width"], row_format.get("num_cols", 0))
            for word in words:
                table_body += f'<div>{word}</div>\n'
    return table_body


def generate_html_file(workbook: openpyxl.Workbook, output_file_path: str) -> None:
    """Генерирует файл HTML из книги Excel"""
    with codecs.open(output_file_path, 'w', 'utf-8') as file:
        file.write(generate_table_header())
        file.write(generate_table_body(workbook, up_formats))
        file.write(generate_table_body(workbook, row_formats))
        file.write("</div></body> </html>\n")

def main() -> None:
    """Основная функция"""
    today = get_today_date()
    print(today)

    workbook_file_path = os.path.join(os.getcwd(), 'files.xlsx')
    output_file_path = os.path.join(os.getcwd(), 'poln.html')

    workbook = load_excel_workbook(workbook_file_path)
    if workbook:
        generate_html_file(workbook, output_file_path)
    else:
        print("Error: Unable to generate HTML file.")

if __name__ == "__main__":
    main()