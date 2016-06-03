#!/usr/bin/python

import cmd
import math
import random

class InterestCalculator(cmd.Cmd):

	def getRate(self, argDict):
		return (argDict["r"] / 100) + 1

	def interestRate(self, argDict):
		amountBorrowed = argDict["p"]
		amountOwed = argDict["i"]
		numPeriods = argDict["n"]
		return ((math.e ** (math.log(amountOwed / amountBorrowed) / numPeriods)) - 1) * 100

	def numPeriods(self, argDict):
		amountBorrowed = argDict["p"]
		rate = self.getRate(argDict)
		amountOwed = argDict["i"]
		return math.log(amountOwed / amountBorrowed) / math.log(rate)

	def amountBorrowed(self, argDict):
		amountOwed = argDict["i"]
		rate = self.getRate(argDict)
		numPeriods = argDict["n"]
		return amountOwed * (rate ** -numPeriods)

	def amountOwed(self, argDict):
		amountBorrowed = argDict["p"]
		rate = self.getRate(argDict)
		numPeriods = argDict["n"]
		return amountBorrowed * (rate ** numPeriods)

	def argDictFromInput(self, input):
		args = input.replace(" ", "").split("-")

		dict = {}
		for arg in args:
			if arg != "":
				try:
					dict[arg[0]] = float(arg[1:])
				except:
					print arg[1:] + " is not a valid number."
					return None

		if len(dict) != 3:
			print "Invalid amount of arguments."
			return None

		return dict

	def printNumberOfPeriods(self, argDict):
		print "Number of Periods: " + str(argDict["n"])

	def printInterestRate(self, argDict):
		print "Interest Rate: " + str(argDict["r"]) + "%"

	def printAmountLoaned(self, argDict):
		print "Amount Loaned: $" + str(argDict["p"])

	def printAmountOwed(self, argDict):
		print "Amount Owed: $" + str(round(argDict["i"], 2))

	def checkIfArgFlagsAreValid(self, argDict):
		validArgFlags = ["i", "p", "r", "n"]
		for key in argDict.keys():
			try:
				validArgFlags.index(key)
			except:
				return key
		return None

	def do_compound(self, line):
		argDict = self.argDictFromInput(line)

		if argDict == None:
			print "Invalid Input"
			return

		invalid = self.checkIfArgFlagsAreValid(argDict)
		if invalid != None:
			print "Invalid Argument Flag: -" + invalid
			return

		if not argDict.has_key("p"):
			print "Calculating Principle..."
			argDict["p"] = self.amountBorrowed(argDict)

		if not argDict.has_key("r"):
			print "Calculating Rate..."
			argDict["r"] = self.interestRate(argDict)

		if not argDict.has_key("n"):
			print "Calculating Number of Periods..."
			argDict["n"] = self.numPeriods(argDict)

		if not argDict.has_key("i"):
			print "Caclulating Amount Owed..."
			argDict["i"] = self.amountOwed(argDict)

		self.printAllCompound(argDict)

	def printAllCompound(self, argDict):
		self.printAmountLoaned(argDict)
		self.printInterestRate(argDict)
		self.printNumberOfPeriods(argDict)
		self.printAmountOwed(argDict)

	def printLine(self):
		line = ""
		for _ in range(0, 50):
			line += "-"
		print line

	def do_test(self, arg):
		rate = float(random.randrange(1, 100, 1)) / 10
		numPeriods = random.randrange(1, 40, 1)
		principle = float(random.randrange(1000, 100000, 1)) / 100
		argDict = {
			"r":rate,
			"n":numPeriods,
			"p":principle
		}
		owed = self.amountOwed(argDict)

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
		print "compound -i <float> -p <float> -r <float> -n <float>"
		print "-i : How much owed at the end."
		print "-p : The principle amount loaned."
		print "-r : The interest rate, in %."
		print "-n : The number of periods,"
		print "Enter 3 of the 4 flags to find the value of the missing one."

	def do_EOF(self, line):
		return True

if __name__ == '__main__':
	InterestCalculator().cmdloop()