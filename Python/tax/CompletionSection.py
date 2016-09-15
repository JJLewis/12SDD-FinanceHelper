from Section import *
from TkHelper import *

class CompletedSection(Section):

    def calculateTaxable(self, income):
        if income <= 18200:
            return 0
        if 18201 <= income <= 37000:
            return (income - 18200) * 0.19
        if 37001 <= income <= 80000:
            return ((income - 37000) * 0.325) + 3572
        if 80001 <= income <= 180000:
            return ((income - 80000) * 0.37) + 17547
        if income >= 180001:
            return ((income - 180000) * 0.47) + 54547

    def doPersonal(self):
        self.statements.append("First Name: " + self.allData["fname"])
        self.statements.append("Last Name: " + self.allData["lname"])
        self.statements.append("Phone Number: " + self.allData["phone"])
        self.statements.append("Bank Account Number: " + self.allData["bank"])
        self.statements.append("Medicare Number: " + self.allData["medi"])

    def doAddress(self):
        self.statements.append("Street Address 1: " + self.allData["str1"])
        self.statements.append("Street Address 2: " + self.allData["str2"])
        self.statements.append("Suburb: " + self.allData["Suburb"])
        self.statements.append("Post Code: " + self.allData["post"])
        self.statements.append("State: " + self.allData["State"])

    def doTransit(self):
        try:
            kms = int(self.allData["How many kms total?"])
            self.totalDeductible += kms * 0.66
            del self.allData["How many kms total?"]
            self.statements.append("Total deductible from driving for work: $" + str(kms * 0.66))
        except:
            pass

        self.statements.append("Claimable from Public Transport Costs: $" + self.allData["public transport"])
        try:
            self.totalDeductible += float(self.allData["public transport"])
        except:
            pass

        self.statements.append("Claimable from Other Expenses: $" + self.allData["Other Transport Expenses"])
        try:
            self.totalDeductible += float(self.allData["Other Transport Expenses"])
        except:
            pass


    def doUniform(self):

        selectedValues = self.allData["Did you buy any of the following?"]
        del self.allData["Did you buy any of the following?"]
        boughtClothingCodes = ""
        codes = {
            "Compulsory Work Uniform": "C",
            "Non-compulsory Work Uniform": "N",
            "Occupation Specific Clothing": "S",
            "Protective Clothing": "P",
        }
        for value in selectedValues:
            key = codes.keys()[value]
            boughtClothingCodes += codes[key] + ", "
        self.statements.append("Clothing letters for items bought: " + boughtClothingCodes[:-2])

        try:
            numWorkOnly = int(self.allData["Home work laundry"])
            self.totalDeductible += numWorkOnly
            del self.allData["Home work laundry"]
            numComb = int(self.allData["Home combined laundry"])
            self.totalDeductible += numComb * 0.5
            del self.allData["Home combined laundry"]
            self.statements.append("Total deductible from laundry: $" + str(numWorkOnly + (numComb * 0.5)))
        except:
            pass

        self.statements.append("Claimable from external laundry: $" + self.allData["External laundry expenses"])
        try:
            self.totalDeductible += float(self.allData["External laundry expenses"])
        except:
            print "Failed to add total external laundry expenses into total deductible!!!"

    def doDonations(self):
        self.statements.append("Claimable from donations: $" + self.allData["donated"])
        try:
            self.totalDeductible += float(self.allData["donated"])
        except:
            pass

    def doTotalClaimable(self):
        totalIncome = float(self.allData["income"])
        taxableIncome = totalIncome - self.totalDeductible
        if taxableIncome < 0:
            helper = TkHelper()
            helper.showAlert("You have more deductions than your income.")
        self.statements.append("Total Income: $" + str(totalIncome))
        self.statements.append("Total Amount Deductible: $" + str(self.totalDeductible))
        self.statements.append("Taxable Income: $" + str(taxableIncome))
        self.statements.append("Tax Payable: $" + str(self.calculateTaxable(taxableIncome)))
        self.statements.append("Medicare Levy: $" + str(taxableIncome * 0.02))

    def addLine(self):
        line = ''
        for _ in range (0, 20):
            line += "-"
        self.statements.append(line)

    def processData(self):
        self.statements = []
        self.totalDeductible = 0.0

        print self.allData

        self.doPersonal()
        self.addLine()

        self.doAddress()
        self.addLine()

        self.doTransit()
        self.addLine()

        self.doUniform()
        self.addLine()

        self.doDonations()
        self.addLine()

        self.doTotalClaimable()

        print self.statements

        helper = TkHelper()
        for i in range(0, len(self.statements)):
            helper.createLabel(self, self.statements[i], GridLocation(0, i))

    def __init__(self, controller, dataDict):
        super(self.__class__, self).__init__(controller, "Receipt")
        self.allData = dataDict
        self.processData()
