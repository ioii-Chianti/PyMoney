import sys
# row format: 0-2 (num) 3-5 (|) 6-15 (category) 16-30 (description) 31-35 (amount)


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
    def __init__(self, category, description, amount):
        ''' constructor: save params as private attributes '''
        self.__category = category
        self.__description = description
        self.__amount = amount

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__category}: {self.__description} $ {self.__amount})"
    
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
                        newCategory = ''.join([ch for i, ch in enumerate(line) if 6 <= i <= 15 and ch != ' '])   # find categorty of item and convert to str
                        newItem = ''.join([ch for i, ch in enumerate(line) if 16 <= i <= 30 and ch != ' '])   # find description of item and convert to str
                        newMoney = int(''.join([ch for i, ch in enumerate(line) if 31 <= i <= 35 and ch != ' ']))   # find amount of item and convert to int
                        self.__container.append(Record(newCategory, newItem, newMoney))   # append as Record object
                    elif line[:9] == 'Balance: ':   # find current wallent
                        self.__wallet = int(''.join([ch for i, ch in enumerate(line) if 9 <= i]))
                except Exception as errmsg:   # catch any kind of errors
                    sys.stderr.write(f'# INITERROR: {str(errmsg)} #\n')
            print(f'Welcome back <3 You have {self.__wallet} dollars..')
    
    @property
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
            newRecord = newRecord.split(', ')
            for data in newRecord:
                assert len(data.split()) == 3, "Multiple data should be separated by ', ' and no spaces in descripton"
                curC, curD, curA = data.split()[0], data.split()[1], int(data.split()[2])
                assert categories.isValidCategory(curC), f'{curC} is not a category'
                assert len(curD) < 16, 'Description should be less than 16 characters'
                
                # if info. are all valid after the checkings above, then update attributes
                self.__container.append(Record(curC, curD, curA))
                self.__wallet += curA
        except ValueError:
            sys.stderr.write('# ADDERROR: Money should be an integer #\n')
        except AssertionError as errmsg:
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
                print('No.   Category  Item          Amount')
                print('------------------------------------')
                for No, data in enumerate(self.__container, 1):
                    print(f'{No:>3d} | {data.category:<10s}{data.description:<15s}{data.amount:>5d}')
                print('------------------------------------')
            print(f'You have {self.__wallet} dollars.')
        except Exception as errmsg:   # catch any kind of errors
            sys.stderr.write(f'# VIEWERROR: {str(errmsg)} #\n')
    
    def Delete(self):
        ''' Delete a specific record by its No. '''
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
            sys.stderr.write(f'# SAVEERROR: {str(errmsg)} #\n')


class Categories:
    ''' Maintain the category list and provide some methods.
        
        Attributes:
            __catalog : list<list/str>
        Methods:
            __init__(self),
            catalog(self),
            View(self, data, level=-1),
            Subcategories(self, toFind),
                SubcategoriesGen(recData, toFind, found=False)
            isValidCategory(self, toCheck),
    '''
    def __init__(self):
        '''  constructor: setting the list structure of categories. '''
        self.__catalog = ['expense', \
                            ['food', ['meal', 'snack', 'drink'], \
                            'transportation', ['bus', 'railway'], \
                            'entertainment', ['movie', 'shop', 'game'], \
                            'housing', ['medical', 'pet', 'bill']], \
                        'income', \
                            ['salary', 'bonus']]

    @property
    def catalog(self):
        return self.__catalog
    
    def View(self, recData, level=-1):
        ''' Recursively print out all categories with indentations
            
            Parameters:
                TODO 完成 doc
        '''
        if type(recData) == str:
            print(f"{'   ' * level}{'-' if level % 2 else '+'} {recData}")
        else:
            for element in recData:
                self.View(element, level + 1)

    def Subcategories(self, toFind):
        ''' Find a non-nested list containing the specified category and all the subcategories under it (if any). '''
        def SubcategoriesGen(recData, toFind, found=False):
            # when the list is end, then do nothing
            if type(recData) == list:
                for i, data in enumerate(recData):
                    yield from SubcategoriesGen(data, toFind, found)
                    if data == toFind and i + 1 < len(recData) and type(recData[i + 1]) == list:
                        # the list containing toFind's subcategories
                        yield from SubcategoriesGen(recData[i + 1], toFind, True)
            # return toFind or toFind's sub
            elif recData == toFind or found:
                yield recData
           
        return [sub for sub in SubcategoriesGen(self.catalog, toFind)]

    def isValidCategory(self, toCheck):
        return toCheck in self.Subcategories(toCheck)


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
                    assert categories.isValidCategory(toFind), f'{toFind} is not a category'
                except AssertionError as errmsg:
                    sys.stderr.write(f'# MAINERROR: {str(errmsg)} #\n')
                else:  # find all subcategories then call Find
                    targets = categories.Subcategories(toFind)
                    records.Find(targets)
        elif command == 'D':
            records.Delete()
        else:
            raise Exception('Invalid command')
    except Exception as errmsg:
        sys.stderr.write(f'# MAINERROR: {str(errmsg)} #\n')