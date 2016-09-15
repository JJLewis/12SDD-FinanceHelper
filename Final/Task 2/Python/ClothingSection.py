from TkHelper import *
from Section import *
from GridLocation import *

class ClothingDeductionSection(Section):

    def onChangeDoOwnLaundry(self):
        self.doesLaundryAtHome = not self.doesLaundryAtHome
        self.toggleField(self.doesLaundryAtHome, self.workLaundry, self.workLaundryLabel)
        self.toggleField(self.doesLaundryAtHome, self.combinedLaundry, self.combinedLaundryLabel)

    def onChangePaidForLaundry(self):
        self.doesLaundryOutside = not self.doesLaundryOutside
        self.toggleField(self.doesLaundryOutside, self.totalLaundryExpenses, self.totalLaundryExpensesLabel)

    def __init__(self, controller):
        super(self.__class__, self).__init__(controller, "Clothing Deductions")

        helper = TkHelper()

        # Create the UI Elements
        helper.createCheckBox(self, "Do you do the laundry yourself?", True, GridLocation(0, 1),
                              self.onChangeDoOwnLaundry)
        (self.workLaundryLabel, self.workLaundry) = helper.createNumericalField(self, "Number of work laundry only runs:",
                                                                               (0, 999), GridLocation(0, 2), "Home work laundry")
        (self.combinedLaundryLabel, self.combinedLaundry) = helper.createNumericalField(self,
                                                                               "Number of mixed (work & personal) laundry runs:",
                                                                               (0, 999), GridLocation(0, 3),
                                                                               "Home combined laundry")
        helper.createCheckBox(self, "Have you paid for any work related laundry?", False, GridLocation(0, 4),
                              self.onChangePaidForLaundry)
        (self.totalLaundryExpensesLabel, self.totalLaundryExpenses) = helper.createNumericalField(self,
                                                                                         "Total external laundry expenses:",
                                                                                                  (0, 9999999), GridLocation(0, 5), "External laundry expenses")
        helper.createListBox(self, "Did you buy any of the following?", [
            "Compulsory Work Uniform",
            "Non-compulsory Work Uniform",
            "Occupation Specific Clothing",
            "Protective Clothing"
        ], GridLocation(0, 6))

        # Apply any rules such as requiring ints or floats and also if fields are required or hidden
        self.doesLaundryAtHome = True
        self.doesLaundryOutside = False

        self.toggleField(self.doesLaundryOutside, self.totalLaundryExpenses, self.totalLaundryExpensesLabel)

        self.requiredInt.append(self.workLaundry)
        self.requiredInt.append(self.combinedLaundry)
        self.requiredFloat.append(self.totalLaundryExpenses)