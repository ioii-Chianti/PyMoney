def Subcategories(self, recData, toFind):
    ''' Find a non-nested list containing the specified category and all the subcategories under it (if any).
    
        Parameters:
            recData : list
                The list structure of all category to traverse recursively.
            toFind : str
                The target category to find.
        Returns:
            1. the flatten format of the target category and its subcategories.
            2. the base case, str.
            3. empty list [] if there is no such specified category.
    '''
    if type(recData) == list:
        for data in recData:
            ret = self.Subcategories(data, toFind)
            # if the str data matches toFind then make a list included itself and its subcate
            if ret == True:
                index = recData.index(data)
                # if any subcategory exists
                if index + 1 < len(recData) and type(recData[index + 1]) == list:
                    return self.__Flatten(recData[index:index + 2])   # final return
                else:   # no subcate just itself
                    return [data]
            if ret != []:
                return ret   # traseback ?
    return True if recData == toFind else []   # base case


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