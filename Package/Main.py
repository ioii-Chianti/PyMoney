import sys

from Class.PyCategory import *
from Class.PyRecord import *

# row format: 0-2 (num) 3-5 (|) 6-15 (category) 16-30 (description) 31-35 (amount)

categories = Categories()
records = Records()

while True:
    try:
        print('\nWhat do you want to do?')
        print('   A | add records')
        print('   V | view all records')
        print('   C | show all categories')
        print('   F | find records in specific categories')
        print('   D | delete record')
        print('   E | exit Accounting System')
        command = input('Command: ')
        if command == 'E':
            records.Save()
            print('GoodBye <3')
            break
        if command == 'A':
            print('Add expense or income records:')
            newRecord = input('Format: <category> <description> <amount>, <category> <description> <amount>, ...\n')
            records.Add(newRecord, categories)
        elif command == 'V':
            records.View()
        elif command == 'C':
            categories.View(categories.catalog)
        elif command == 'F':
            if not records.container:   # container is empty
                print('Nothing in your Accounting Book.')
            else:
                try:   # check valid category
                    toFind = input('Which category do you want to find? ')
                    assert categories.isValidCategory(categories.catalog, toFind), f'{toFind} is not a category.'
                except AssertionError as errmsg:
                    sys.stderr.write(f'[Main] Error: {str(errmsg)}\n')
                else:  # find all subcategories then call Find
                    targets = categories.Subcategories(toFind)
                    records.Find(targets)
        elif command == 'D':
            records.Delete()
        else:
            raise Exception('Invalid command.')
    except Exception as errmsg:
        sys.stderr.write(f'[Main] Error: {str(errmsg)}\n')
