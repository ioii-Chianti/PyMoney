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
            isValidCategory(self, Cate, toCheck),
            __Flatten(self, data)
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
            if type(recData) == list:
                for i, data in enumerate(recData):
                    yield from SubcategoriesGen(data, toFind, found)
                    if data == toFind and i + 1 < len(recData) and type(recData[i + 1]) == list:
                        yield from SubcategoriesGen(recData[i + 1], toFind, True)
            else:
                if recData == toFind or found:
                    yield recData
        return [sub for sub in SubcategoriesGen(self.catalog, toFind)]

    def isValidCategory(self, Cate, toCheck):
        return toCheck in self.Subcategories(toCheck)

    def __Flatten(self, recData):
        ''' return a flat list that contains all element in the nested list recData
            for example, flatten([1, 2, [3, [4], 5]]) returns [1, 2, 3, 4, 5]
            
            Parameters:
                recData : list
                    The nested list.
            Returns:
                retList : list
                    A flat list.
        '''
        if type(recData) == list:
            retList = []
            for element in recData:
                retList.extend(self.__Flatten(element))
            return retList   # final return
        else:   # base case, recData is a str
            return [recData]   # use [recData] instead of recData since the extend method needs list type 