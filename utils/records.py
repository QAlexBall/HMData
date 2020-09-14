import csv
import os, time
from openpyxl import load_workbook, Workbook

def create_excel():
    excel = Workbook()
    path = os.path.dirname(os.path.abspath('.')) + '\\HMData\\data\\'
    t = time.strftime('%Y%m%d', time.localtime(time.time()))
    excel_path = path + t + '.xlsx'
    print(excel_path)
    excel.save(excel_path)
    return excel, excel_path


def create_csv():
    path = os.path.dirname(os.path.abspath('.')) + '\\HMData\\data\\'
    t = time.strftime('%Y%m%d', time.localtime(time.time()))
    excel_path = path + t + '.csv'
    with open(excel_path, 'w') as f:
        pass
    return excel_path    
    

if __name__ == "__main__":
    create_csv()