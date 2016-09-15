from TkHelper import *
from Section import *
from GridLocation import *

class AddressSection(Section):
    def extractedDataDict(self):
        """
        Override the super class's extractedDataDict function to add the OptionMenu functionality

        :return: A dictionary with the same keys but the values of the widgets rather than the widgets
        """
        dataDict = {}
        for key, value in self.widgetsDict.iteritems():
            if isinstance(value, Entry):
                dataDict[key] = value.get()
            elif isinstance(value, Listbox):
                dataDict[key] = value.curselection()
            elif isinstance(value, OptionMenu):
                dataDict[key] = self.stateValue.get()
        return dataDict

    def __init__(self, controller):
        super(self.__class__, self).__init__(controller, "Address Section")

        helper = TkHelper()

        # Create the UI Elements
        helper.createField(self, "Street Address 1", GridLocation(0, 1), "str1")
        _, addr2 = helper.createField(self, "Street Address 2", GridLocation(0, 2), "str2")
        helper.createField(self, "Suburb", GridLocation(0, 3))
        helper.createField(self, "Post Code", GridLocation(0, 4), "post")
        (frame, self.stateValue) = helper.createDropdown(self, "State", ["ACT", "NSW", "QLD", "SA", "WA", "TAS", "VIC"],
                                                         GridLocation(0, 5))

        # Apply any rules such as requiring ints or floats and also if fields are required or hidden
        self.notRequiredFields.append(addr2)