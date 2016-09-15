#!/usr/bin/python

import cmd
import math
import random

class InterestCalculator(cmd.Cmd):
    # MARK Global Variables
    validArgFlags = ["i", "p", "r", "n", "c"]

    # MARK Convenience Functions
    def arrayContains(self, array, item):
        """
        Check to see if an item exists in an array.

        :param array: Any list of values
        :param item: A value to check if exists in array.
        :return: Boolean, if exists: True, else False
        """
        try:
            array.index(item)
            return True
        except:
            return False

    # MARK Print Functions
    def printNumberOfPeriods(self, argDict):
        """
        Reads the number of periods from the dictionary and prints it.

        :param argDict: {"flag":value}
        """
        print "Number of Periods: " + str(argDict["n"])

    def printInterestRate(self, argDict):
        """
        Reads the interest rate from the dictionary and prints it.

        :param argDict: {"flag":value}
        """
        print "Interest Rate: " + str(argDict["r"]) + "%"

    def printAmountLoaned(self, argDict):
        """
        Reads the amount loaned (principle) from the dictionary and prints it.

        :param argDict: {"flag":value}
        """
        print "Amount Loaned: $" + str(argDict["p"])

    def printAmountOwed(self, argDict):
        """
        Reads the amount owed from the dictionary and prints it.

        :param argDict: {"flag":value}
        """
        print "Amount Owed: $" + str(round(argDict["i"], 2))

    def printAllCompound(self, argDict):
        """
        Calls all of the print functions to print all 4 pro-numerals.
        This is just a convenience method.

        :param argDict: {"flag":value}
        """
        self.printAmountLoaned(argDict)
        self.printInterestRate(argDict)
        self.printNumberOfPeriods(argDict)
        self.printAmountOwed(argDict)

    def printLine(self):
        """
        Prints a line with 50 -s.
        Used for visually separating lines of prints.
        """
        line = ""
        for _ in range(0, 50):
            line += "-"
        print line

    # MARK Calculations
    def getRate(self, argDict):
        """
        Corrects the % inputted by the user to a number usable by the formulas.

        :rtype: float
        :param argDict: {"flag":value}
        :return: The rate to be used in formulas.
        """
        return (argDict["r"] / 100) + 1

    def calculateInterestRate(self, argDict):
        """
        Calculates the interest rate by reading the other 3 values from the dictionary.

        :rtype: float
        :param argDict: {"flag":value}
        :return: The interest rate as a float
        """
        amountBorrowed = argDict["p"]
        amountOwed = argDict["i"]
        numPeriods = math.floor(argDict["n"])
        return ((math.e ** (math.log(amountOwed / amountBorrowed) / numPeriods)) - 1) * 100

    def calculateNumberOfPeriods(self, argDict):
        """
        Calculates the interest rate by reading the other 3 values from the dictionary.

        :rtype: float
        :param argDict: {"flag":value}
        :return: The interest rate as a float
        """
        amountBorrowed = argDict["p"]
        rate = self.getRate(argDict)
        amountOwed = argDict["i"]
        return math.ceil(math.log(amountOwed / amountBorrowed) / math.log(
            rate))  # Round up to the nearest whole as cannot have half periods

    def calculateAmountBorrowed(self, argDict):
        """
        Calculates the interest rate by reading the other 3 values from the dictionary.

        :rtype: float
        :param argDict: {"flag":value}
        :return: The interest rate as a float
        """
        amountOwed = argDict["i"]
        rate = self.getRate(argDict)
        numPeriods = math.floor(argDict["n"])
        return amountOwed * (rate ** -numPeriods)

    def calculateAmountOwed(self, argDict):
        """
        Calculates the interest rate by reading the other 3 values from the dictionary.

        :rtype: float
        :param argDict: {"flag":value}
        :return: The interest rate as a float
        """
        amountBorrowed = argDict["p"]
        rate = self.getRate(argDict)
        numPeriods = math.floor(argDict["n"])
        return amountBorrowed * (rate ** numPeriods)

    # MARK Parsing Input
    def adjustDateFormat(self, value, currentFormat, targetFormat):
        """
        Converts a given time unit to another one, and rounds down. i.e. 7 days = 1 week

        :rtype: float
        :param value: The number of units to be converted to another unit.
        :param currentFormat: The unit of the value being passed in. i.e. D, W, M
        :param targetFormat: The date unit which we want the value to be changed to. i.e. D, W, M
        :return: A floored adjusted date, ie 8 days -> 1 week, as compounding only occurs every full number.
        """

        adjustmentValues = {
            "s": 60.0,
            "m": 60.0,
            "h": 24.0,
            "D": 7.0,
            "W": 2.0,
            "F": 30.0 / 14.0,
            "M": 3.0,
            "Q": 4.0,
            "Y": 1.0,
        }
        keys = "s m h D W F M Q Y".split(" ")
        currentIndex = keys.index(currentFormat)
        targetIndex = keys.index(targetFormat)
        adjustedValue = float(value)
        if currentIndex < targetIndex:
            for i in range(currentIndex, targetIndex):
                adjustedValue /= adjustmentValues[keys[i]]
        elif currentIndex > targetIndex:
            for i in range(currentIndex, targetIndex, -1):
                adjustedValue *= adjustmentValues[keys[i - 1]]

        return math.floor(adjustedValue)

    def argDictFromInput(self, input):
        """
        Parses the argument string from the command to a dictionary and also checks for any abnormalities.
        Also converts the time units if need be.

        :rtype: Dictionary
        :param input: The string argument from the command.
        :return: {"flag":value}
        """

        args = input.replace(" ", "").split("-")

        # A coathanger fix to stitch back together arguments that have a hyphen which is meant to be a negative sign
        for i in range(0, len(args)):
            try:
                int(args[i][0])
                args[i - 1] = args[i - 1] + "-" + args[i]
                del args[i]
            except:
                pass

        dict = {}

        shouldAdjust = None
        adjustTo = None

        for arg in args:
            if arg != "":
                try:
                    if arg[0] == "n":
                        try:
                            dict[arg[0]] = float(arg[1:])
                        except:
                            dict[arg[0]] = float(arg[1:-1])
                            shouldAdjust = arg[-1:]
                    elif arg[0] == "c":
                        adjustTo = arg[1:]
                    elif self.arrayContains(self.validArgFlags, arg[0]):
                        dict[arg[0]] = float(arg[1:])
                    else:
                        print "Invalid Argument Flag: " + arg[0]
                        return None
                except:
                    print arg[1:] + " is not a valid number."
                    return None

        # If the number of arguments is not right
        if len(dict) != 3:
            print "Invalid amount of arguments."
            return None

        # Check for any negative argument values.
        for key, value in dict.iteritems():
            if key != "c":
                if value < 0:
                    print "Cannot have value for argument " + key + " be less than 0."
                    return None

        # If amount owed is less that principle
        if self.isOwedgtPrinciple(dict):
            print "Principle cannot be greater than amount owed."
            return None

        # Adjusting the time format if required
        if shouldAdjust != None and adjustTo != None:
            try:
                dict["n"] = self.adjustDateFormat(dict["n"], shouldAdjust, adjustTo)
            except:
                print "Invalid time flag, refer to 'help' for all of the valid time flags."
                return None
        elif shouldAdjust != None and adjustTo == None:
            pass  # No need to adjust, assuming the user was being verbose
        elif shouldAdjust == None and adjustTo != None:
            print "Period time format not specified. Add either a d,m,q,y after the number to specify."
            return None

        return dict

    def isOwedgtPrinciple(self, argDict):
        """
        Just moving the kind of ugly try, except block out of an

        :param argDict: {"flag":value}
        :return: Boolean
        """
        try:
            return argDict["p"] > argDict["i"]
        except:
            return False

    # MARK Commands
    def do_compound(self, line):
        """
        Called when the command 'compound' is entered into the terminal.
        Calls other functions to parse the input, then finds which parameter of the 4 is missing and calculates it.
        Prints all the parameters and the calculated value.

        :param line: The argument string following the command.
        """
        argDict = self.argDictFromInput(line)

        if argDict == None:
            print "Invalid Input"
            return

        if not argDict.has_key("p"):
            print "Calculating Principle..."
            argDict["p"] = self.calculateAmountBorrowed(argDict)

        if not argDict.has_key("r"):
            print "Calculating Rate..."
            argDict["r"] = self.calculateInterestRate(argDict)

        if not argDict.has_key("n"):
            print "Calculating Number of Periods..."
            argDict["n"] = self.calculateNumberOfPeriods(argDict)

        if not argDict.has_key("i"):
            print "Caclulating Amount Owed..."
            argDict["i"] = self.calculateAmountOwed(argDict)

        self.printAllCompound(argDict)

    def do_test(self, arg):
        """
        Called when the command 'test' is typed into the terminal.
        It will generate a random set of numbers and run all of the calculations ofn them and will print them.

        :param arg: The string of arguments after the command. Does not do anything in this function.
        """
        rate = float(random.randrange(1, 100, 1)) / 10
        numPeriods = random.randrange(1, 40, 1)
        principle = float(random.randrange(1000, 100000, 1)) / 100
        argDict = {
            "r": rate,
            "n": numPeriods,
            "p": principle
        }
        owed = self.calculateAmountOwed(argDict)

        print "Starting Test...."
        self.printLine()
        print "Preset Rate: " + str(rate)
        print "Preset Periods: " + str(numPeriods)
        print "Preset Principle: " + str(principle)
        print "Preset Owed: " + str(round(owed, 2))

        command = "p " + str(principle) + " -r " + str(rate) + " -n " + str(numPeriods) + " -i " + str(owed)
        for i in range(0, 4):
            parts = command.split("-")
            parts.remove(parts[i])
            newCommand = ""
            for part in parts:
                newCommand += "-" + part
            self.printLine()
            print "compound " + newCommand
            self.do_compound(newCommand)
        self.printLine()
        print "Now check to see if all of the calculated numbers match or are extremely close to the original."

    def do_help(self, arg):
        """
        Called when the command 'help' is typed into the terminal.

        :param arg: The string of arguments after the command. Does not do anything in this function.
        """
        print "compound -i <float> -p <float> -r <float> -n <float><s,m,h,D,W,F,M,Q,Y> -f <s,m,h,D,W,F,M,Q,Y>"
        print "-i : How much owed at the end."
        print "-p : The principle amount loaned."
        print "-r : The interest rate, in %."
        print "-n : The amount of time."
        print "-c : How often the interest is compounded"
        print "    s : Seconds"
        print "    m : Minutes"
        print "    h : Hours"
        print "    D : Days"
        print "    W : Weeks"
        print "    F : Fortnights"
        print "    M : Months"
        print "    Q : Quarters"
        print "    Y : Years"
        print "Enter 3 of the first 4 flags to find the value of the missing one. -f is optional, if it is not used, this will use the amount of time as the number of periods."
        print "Type quit to exit the program."

    def do_quit(self, args):
        """
        Register the command 'quit' so that it can terminate the command line process.

        :param args: The string of arguments after the command. Does not do anything in this function.
        :return: True to stop the command line app
        """
        return True

    def emptyline(self):
        """
        Overriden to stop the default action of repeating the previous command if there is an empty line.
        """
        pass

    def do_EOF(self, line):
        """
        When there is an end of line character, kill the current command line process.

        :param line: The string of arguments after the command. Does not do anything in this function.
        :return: True
        """
        return True


if __name__ == '__main__':
    print "Type 'help' to show the list of flags and how to use this command line tool."
    InterestCalculator().cmdloop()
