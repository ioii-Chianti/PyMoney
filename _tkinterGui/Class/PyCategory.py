from Class.PyRecord import *

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
    
    # 沒有用 XD
    def View(self):
        def recView(recData, level=-1):
            ''' Recursively print out all categories with indentations
                
                Parameters:
                    recData : list/str
                    level : int
                        Decide how many space to print
            '''
            if recData is None:
                return
            if type(recData) == str:
                yield (f"{'   ' * level}- {recData}\n")
            else:
                for element in recData:
                    recView(element, level + 1)
        string = ''.join([ret for ret in recView(self.__catalog)])
        return string

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
        ''' Check if toCheck exists in catalog '''
        return toCheck in self.Subcategories(toCheck)