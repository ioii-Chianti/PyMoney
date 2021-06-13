import sys
from datetime import *
from Class.PyCategory import *


class Record:
    ''' Represent a single record.

        Attributes:
            __category : str
            __description : str
            __amount : int
        Methods:
            __init__(self, category, description, amount),
            __repr__(self),
            category(self),
            description(self),
            amount(self)
    '''
    def __init__(self, date, category, description, amount):
        ''' constructor: save params as private attributes '''
        self.__date = date
        self.__category = category
        self.__description = description
        self.__amount = amount

    def __repr__(self):
        return f"{self.__class__.__name__}({self.date} | {self.category}: {self.description} $ {self.amount})"

    @property
    def date(self):
        return self.__date
    @property
    def category(self):
        return self.__category
    @property
    def description(self):
        return self.__description
    @property
    def amount(self):
        return self.__amount

# 012 345 6789012345 67 8901234567 890123456789012 34567
# No.  |  YYYY-MM-DD    CategoryCa DescriptionDesc -1011
class Records:
    ''' Maintain a list of all the 'Record's and the initial amount of money.
        
        Attributes:
            __wallet : int
            __container : list<Record>
        Methods:
            __init__(self),
            container(self),
            Add(self, newRecord, categories),
            View(self),
            Delete(self),
            Find(self, SubsList),
            Save(self)
    '''
    def __init__(self):
        ''' constructor: init attributes by creating a new file or reading an existing file. '''
        self.__wallet = 0
        self.__container = []
        try:
            fh = open('AccountingBook.txt', 'r')
            assert fh.readlines() != ''
            fh.seek(0)   # back to first line after using readlines()
        except (FileNotFoundError, AssertionError):   # create one if file doesn't exist or is empty
            print("Let's create an Accounting Book.")
            while True:
                try:
                    newWallet = int(input('How much money do you have? '))
                except ValueError:
                    sys.stderr.write('# INITERROR: Input should be an integer #\n')
                else:
                    self.__wallet = newWallet
                    self.__container = []
                    break
        else:   # read file if it exists
            for line in fh.readlines():
                try:
                    if line[2].isdigit():   # find item No.
                        newDate = line[6:16]
                        newCategory = ''.join([ch for i, ch in enumerate(line) if 18 <= i <= 27 and ch != ' '])   # find categorty of item and convert to str
                        newItem = ''.join([ch for i, ch in enumerate(line) if 28 <= i <= 42 and ch != ' '])   # find description of item and convert to str
                        newMoney = int(''.join([ch for i, ch in enumerate(line) if 43 <= i <= 47 and ch != ' ']))   # find amount of item and convert to int
                        self.__container.append(Record(newDate, newCategory, newItem, newMoney))   # append as Record object
                    elif line[:9] == 'Balance: ':   # find current wallent
                        self.__wallet = int(''.join([ch for i, ch in enumerate(line) if 9 <= i]))
                except Exception as errmsg:   # catch any kind of errors
                    sys.stderr.write(f'# INITERROR: {str(errmsg)} #\n')
            print(f'Welcome back <3 You have {self.__wallet} dollars..')
            fh.close()
    
    @property   # along with Record's __repr__
    def container(self):
        # a list contains Record objects
        ret = [record for record in self.__container]
        return ret
    
    def Add(self, newRecord, categories):
        ''' Add any number of records with informations, category, description, amount.
            
            Parameters:
                newRecord : str
                    the origin data hasn't been normalized
                categories : Category
                    a Category object
        '''
        try:
            # format normalization
            newRecord = newRecord.split(', ')   # 先把每筆依逗號分開
            for data in newRecord:
                data = data.split()   # 各筆資料再把項目分開
                assert len(data) in {3, 4}, "Multiple data should be separated by ', ' and no spaces in descripton"
                newDate = date.today() if len(data) == 3 else date.fromisoformat(data[0])
                if len(data) == 4:
                    del data[0]   # delete date for unitifying format
                curT = newDate.strftime('%Y-%m-%d')   # convert 'date' type to 'str' type
                curC, curD, curA = data[0], data[1], int(data[2])
                assert categories.isValidCategory(curC), f'{curC} is not a category'
                assert len(curD) < 16, 'Description should be less than 16 characters'
                
                # if info. are all valid after the checkings above, then update attributes
                self.__container.append(Record(curT, curC, curD, curA))
                self.__wallet += curA
        except (ValueError, AssertionError) as errmsg:
            sys.stderr.write(f'# ADDERROR: {str(errmsg)} #\n')
        else:
            self.View()
    
    def View(self):
        ''' Print out all records with informations '''
        try:
            if not self.__container:
                print('Nothing in your Accounting Book.')
            else:
                print("Here's your expense and income records.")
                print('No.   Date        Category  Item          Amount')
                print('------------------------------------------------')
                for No, data in enumerate(self.__container, 1):
                    print(f'{No:>3d} | {data.date:<10s}  {data.category:<10s}{data.description:<15s}{data.amount:>5d}')
                print('------------------------------------------------')
            print(f'You have {self.__wallet} dollars.')
        except Exception as errmsg:   # catch any kind of errors
            sys.stderr.write(f'# VIEWERROR: {str(errmsg)} #\n')
    
    def Delete(self):
        ''' Delete a specific record by its No. '''
        if not self.__container:
            print('Nothing to delete.')
        else:
            print('No.   Date        Category  Item          Amount')
            print('------------------------------------------------')
            for No, data in enumerate(self.__container, 1):
                print(f'{No:>3d} | {data.date:<10s}  {data.category:<10s}{data.description:<15s}{data.amount:>5d}')
            print('------------------------------------------------')
            while True:
                try:
                    No = int(input('Enter No. you want to delete: '))
                    assert 1 <= No <= len(self.__container)
                except ValueError:
                    sys.stderr.write(f'# DELERROR: Input should be an integer #\n')
                except AssertionError:   # out of range
                    sys.stderr.write(f'# DELERROR: Input should be within 1 to {len(self.__container)} #\n')
                else:   # uplate current datas
                    self.__wallet -= self.__container[No-1].amount
                    del self.__container[No-1]
                    self.View()
                    break

    def Find(self, SubsList):
        ''' Print out records whose categort is in Sublist.

            Parameter:
                SubList : List
                    the list contains all target categories
        '''
        toPrint = [record for record in self.__container if record.category in SubsList]
        if not toPrint:   # the list 'toPrint' is empty
            print(f'There is no record in {SubsList[0]}.')
        else:   # similar to View()
            total = 0
            print('No.   Date        Category  Item          Amount')
            print('------------------------------------------------')
            for No, data in enumerate(toPrint, 1):
                print(f'{No:>3d} | {data.date:<10s}  {data.category:<10s}{data.description:<15s}{data.amount:>5d}')
                total += data.amount
            print('------------------------------------------------')
            print(f'The total amount above is {total} dollars.')

    def Save(self):
        ''' Rewrite the file 'AccountingBook.txt' with updated records'''
        try:
            with open('AccountingBook.txt', 'w') as fh:
                if not self.__container:
                    fh.write('Nothing in your Accounting Book.\n')
                else:
                    fh.write('No.   Date        Category  Item          Amount\n')
                    fh.write('------------------------------------------------\n')
                    for No, data in enumerate(self.__container, 1):
                        fh.write(f'{No:>3d} | {data.date:<10s}  {data.category:<10s}{data.description:<15s}{data.amount:>5d}\n')
                    fh.write('------------------------------------------------\n')
                fh.write(f'Balance: {self.__wallet}\n')
        except Exception as errmsg:
            sys.stderr.write(f'# SAVEERROR: {str(errmsg)} #\n')
