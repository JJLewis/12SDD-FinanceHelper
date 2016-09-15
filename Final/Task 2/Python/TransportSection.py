from TkHelper import *
from Section import *
from GridLocation import *

class TransportDeductionSection(Section):
    def onChangeDriveForWork(self):
        self.showingKms = not self.showingKms
        self.toggleField(self.showingKms, self.kms, self.kmsLabel)

    def onChangePublicTransport(self):
        self.showingPublicCost = not self.showingPublicCost
        self.toggleField(self.showingPublicCost, self.publicCost, self.publicCostLabel)

    def onChangeTravelAllowance(self):
        pass

    def __init__(self, controller):
        super(self.__class__, self).__init__(controller, "Transport Deductions")

        helper = TkHelper()

        # Create the UI Elements
        helper.createCheckBox(self,
                              "Do you drive a car for work? (Not including home to work and vice versa unless home is a base of employment or you are carrying bulky items that cannot be left at the work place.",
                              False, GridLocation(0, 1), self.onChangeDriveForWork)
        (self.kmsLabel, self.kms) = helper.createNumericalField(self, "How many kms total?", (0, 9999999999999999),GridLocation(0, 2))
        helper.createCheckBox(self, "Do you use public transport for work?", False, GridLocation(0, 3),
                              self.onChangePublicTransport)
        (self.publicCostLabel, self.publicCost) = helper.createNumericalField(self, "Total cost of public transport: $",
                                                                              (0, 9999999999999999), GridLocation(0, 4), "public transport")
        (self.otherExpensesLabel, self.otherExpenses) = helper.createNumericalField(self,
                                                                           "Total of any other transport related expenses. (Bridges and road tolls, parking fees and short term car hire, meals, accomodation and inicidental expences you incur while away overnight for work.",
                                                                                    (0, 9999999999999999), GridLocation(0, 5),
                                                                           "Other Transport Expenses")

        # Apply any rules such as requiring ints or floats and also if fields are required or hidden
        self.showingKms = False
        self.showingPublicCost = False

        self.toggleField(self.showingKms, self.kms, self.kmsLabel)
        self.toggleField(self.showingPublicCost, self.publicCost, self.publicCostLabel)

        self.notRequiredFields.append(self.otherExpenses)

        self.requiredInt.append(self.kms)
        self.requiredFloat.append(self.publicCost)
        self.requiredFloat.append(self.otherExpenses)