import sys
from Class.PyCategory import *


class Record:
    ''' Represent a single record.

        Attributes:
            __category : str
            __description : str
            __amount : int
        Methods:
            __init__(self, category, description, amount),
            category(self),
            description(self),
            amount(self)
    '''
    def __init__(self, category, description, amount):
        ''' constructor: save params as private attributes of self '''
        self.__category = category
        self.__description = description
        self.__amount = amount

    def __repr__(self):
        return f"{self.__class__.__name__}([{self.__category}] {self.__description} ${self.__amount})"
    
    @property
    def category(self):
        return self.__category
    @property
    def description(self):
        return self.__description
    @property
    def amount(self):
        return self.__amount

class Records:
    ''' Maintain a list of all the 'Record's and the initial amount of money.
        
        Attributes:
            __wallet : int
            __container : list<Record>
        Methods:
            __init__(self),
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
                    sys.stderr.write('[init Create] Error: Input should be an integer.\n')
                else:
                    self.__wallet = newWallet
                    self.__container = []
                    break
        else:   # read file if it exists
            for line in fh.readlines():
                try:
                    if line[2].isdigit():   # find item No.
                        newCategory = ''.join([ch for i, ch in enumerate(line) if 6 <= i <= 15 and ch != ' '])   # find categorty of item and convert to str
                        newItem = ''.join([ch for i, ch in enumerate(line) if 16 <= i <= 30 and ch != ' '])   # find description of item and convert to str
                        newMoney = int(''.join([ch for i, ch in enumerate(line) if 31 <= i <= 35 and ch != ' ']))   # find amount of item and convert to int
                        self.__container.append(Record(newCategory, newItem, newMoney))   # append as Record object
                    elif line[:9] == 'Balance: ':   # find current wallent
                        self.__wallet = int(''.join([ch for i, ch in enumerate(line) if 9 <= i]))
                except Exception as errmsg:   # catch any kind of errors
                    sys.stderr.write(f'[init Read] Error: {str(errmsg)}\n')
            print(f'Welcome back <3 You have {self.__wallet} dollars.')
    
    @property
    def container(self):
        ret = [record for record in self.__container]
        return ret
    
    def Add(self, newRecord, categories):
        ''' Add any number of records with informations, category, description, amount.
            
            Parameters:
                Records : list
                    The global container contains all records.
            Returns:
                Records : list
                    The updated version of Records.
        '''
        try:
            # format normalization
            newRecord = newRecord.split(', ')
            for data in newRecord:
                assert len(data.split()) == 3, "Multiple data should be separated by ', ' and no spaces in descripton."
                curC, curD, curA = data.split()[0], data.split()[1], int(data.split()[2])
                assert categories.isValidCategory(categories.catalog, curC), f'{curC} is not a category.'
                assert len(curD) < 16, 'Description should be less than 16 characters.'
                
                # if info. are valid then update attributes
                self.__container.append(Record(curC, curD, curA))
                self.__wallet += curA
        except ValueError:
            sys.stderr.write('[Add] Error: Money should be an integer.\n')
        except AssertionError as errmsg:
            sys.stderr.write(f'[Add] Error: {str(errmsg)}\n')
        else:
            self.View()
    
    def View(self):
        ''' Print out all records with informations '''
        try:
            if not self.__container:
                print('Nothing in your Accounting Book.')
            else:
                print("Here's your expense and income records.")
                print('No.   Category  Item          Amount')
                print('------------------------------------')
                for No, data in enumerate(self.__container, 1):
                    print(f'{No:>3d} | {data.category:<10s}{data.description:<15s}{data.amount:>5d}')
                print('------------------------------------')
            print(f'You have {self.__wallet} dollars.')
        except Exception as errmsg:   # catch any kind of errors
            sys.stderr.write(f'[View] Error: {str(errmsg)}\n')
    
    def Delete(self):
        ''' Delete a specific record by its No.
        Parameters:
            Records : list
                The global container contains all records.
        '''
        if not self.__container:
            print('Nothing to delete.')
        else:
            print('No.   Category  Item          Amount')
            print('------------------------------------')
            for No, data in enumerate(self.__container, 1):
                print(f'{No:>3d} | {data.category:<10s}{data.description:<15s}{data.amount:>5d}')
            print('------------------------------------')
            while True:
                try:
                    No = int(input('Enter No. you want to delete: '))
                    assert 1 <= No <= len(self.__container)
                except ValueError:
                    sys.stderr.write(f'[Delete] Error: Input should be an integer.\n')
                except AssertionError:   # out of range
                    sys.stderr.write(f'[Delete] Error: Input should be within 1 to {len(self.__container)}\n')
                else:   # uplate current datas
                    self.__wallet -= self.__container[No-1].amount
                    del self.__container[No-1]
                    self.View()
                    break

    def Find(self, SubsList):
        toPrint = [record for record in self.__container if record.category in SubsList]
        if not toPrint:   # the list 'toPrint' is empty
            print(f'There is no record in {SubsList[0]}.')
        else:   # similar to View()
            total = 0
            print('No.   Category  Item          Amount')
            print('------------------------------------')
            for No, data in enumerate(toPrint, 1):
                print(f'{No:>3d} | {data.category:<10s}{data.description:<15s}{data.amount:>5d}')
                total += data.amount
            print('------------------------------------')
            print(f'The total amount above is {total} dollars.')

    def Save(self):
        try:
            with open('AccountingBook.txt', 'w') as fh:
                if not self.__container:
                    fh.write('Nothing in your Accounting Book.\n')
                else:
                    fh.write('No.   Category  Item          Amount\n')
                    fh.write('------------------------------------\n')
                    for No, data in enumerate(self.__container, 1):
                        fh.write(f'{No:>3d} | {data.category:<10s}{data.description:<15s}{data.amount:>5d}\n')
                    fh.write('------------------------------------\n')
                fh.write(f'Balance: {self.__wallet}\n')
        except Exception as errmsg:
            sys.stderr.write(f'[Save] Error: {str(errmsg)}\n')
