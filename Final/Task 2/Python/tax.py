import Tkinter
from AllSections import *

class Tax(object):

    def doCompletion(self):

        # Extract all of the data from the widgets in the sections and place them into a dictionary
        allDataDict = {}
        for section in self.sectionOrder:
            allDataDict.update(section.extractedDataDict())

        # Hide he last section and show the completion section
        self.sectionOrder[self.currentSection].hide()
        self.completionSection = CompletedSection(self, allDataDict)
        self.nextButton.grid_remove()

    def nextSection(self):
        helper = TkHelper()

        # If the next section exists
        if self.currentSection + 1 < len(self.sectionOrder):

            # Check all required fields are complete and that all the data types are valid
            if self.sectionOrder[self.currentSection].isSectionComplete():
                if self.sectionOrder[self.currentSection].validateDataTypes():
                    self.sectionOrder[self.currentSection].hide()
                    self.currentSection += 1
                    self.sectionOrder[self.currentSection].show()

                    # If the next section is the last
                    if self.currentSection + 1 == len(self.sectionOrder):
                        self.nextButton.grid_remove()
                        self.nextButton.grid_forget()
                        self.nextButton = Button(self.root, text="Complete Form", command=self.doCompletion)
                        self.nextButton.grid()
                else:
                    helper.showAlert("Invalid Data Types.")
            else:
                helper.showAlert("Section is incomplete.")

    def __init__(self):

        self.root = Tkinter.Tk()
        self.root.resizable(0, 0) # Disable the user window resizing

        # Instantiate all of the Sections
        personalInfo = PersonalInfoSection(self)
        address = AddressSection(self)
        clothing = ClothingDeductionSection(self)
        transport = TransportDeductionSection(self)
        donations = DonationDeductionSection(self)

        # For keeping track of the current section as the user works through them
        self.currentSection = 0
        self.sectionOrder = [
            personalInfo,
            address,
            clothing,
            transport,
            donations
        ]

        self.nextButton = Button(self.root, text="Next Section", command=self.nextSection)
        self.nextButton.grid(column=0)

        # Hide all of the sections that do not need to be seen
        address.hide()
        clothing.hide()
        transport.hide()
        donations.hide()

        self.root.mainloop()

if __name__ == "__main__":
    Tax()
