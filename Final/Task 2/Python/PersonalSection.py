from TkHelper import *
from Section import *
from GridLocation import *

class PersonalInfoSection(Section):
    def __init__(self, controller):
        super(self.__class__, self).__init__(controller, "Your Information")
        helper = TkHelper()

        # Create the UI Elements
        helper.createField(self, "First Name", GridLocation(0, 1), "fname")
        helper.createField(self, "Last Name", GridLocation(0, 2), "lname")
        label, incomeField = helper.createNumericalField(self, "Total Income", (0, 999999999999999999), GridLocation(0, 3), "income")
        helper.createField(self, "Phone Number", GridLocation(0, 4), "phone")
        helper.createField(self, "Bank Account Number", GridLocation(0, 5), "bank")
        helper.createField(self, "Medicare Number", GridLocation(0, 6), "medi")

        # Apply any rules such as requiring ints or floats and also if fields are required or hidden
        self.requiredFloat.append(incomeField)