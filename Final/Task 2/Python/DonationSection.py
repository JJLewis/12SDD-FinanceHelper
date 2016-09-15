from TkHelper import *
from Section import *
from GridLocation import *

class DonationDeductionSection(Section):
    def onChangeDonated(self):
        """
        Called when the "has donated > $2" is checked or unchecked
        """
        self.hasDonated = not self.hasDonated
        self.toggleField(self.hasDonated, self.donated, self.donatedLabel)

    def __init__(self, controller):
        super(self.__class__, self).__init__(controller, "Donation Deductions")

        helper = TkHelper()

        # Create the UI Elements
        helper.createCheckBox(self, "Have you donated $2 or more to an approved organisation?", False,
                              GridLocation(0, 1), self.onChangeDonated)
        (self.donatedLabel, self.donated) = helper.createNumericalField(self, "How much have you donated in total? $",
                                                                        (2, 99999999999999),GridLocation(0, 2), "donated")

        # Apply any rules such as requiring ints or floats and also if fields are required or hidden
        self.hasDonated = False

        self.toggleField(self.hasDonated, self.donated, self.donatedLabel)

        self.requiredFloat.append(self.donated)