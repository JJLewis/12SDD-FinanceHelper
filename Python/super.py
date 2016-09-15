import argparse

# Create an instance of a argument parser and register the appropriate arguments
parser = argparse.ArgumentParser()
parser.add_argument("-m", type=float, help="The amount of money in the regular instalments.", required=True)
parser.add_argument("-r", type=float, help="The interest rate of you superannuation account.", required=True)
parser.add_argument("-n", type=int, help="The number of periods/installments.", required=True)

args = parser.parse_args()

# Check all arguments to see if they are less than or equal to 0
shouldRun = True
for arg in vars(args):
    value = getattr(args, arg) # The value entered after the flag
    if value <= 0:
        print "Argument '" + arg +"' has a value <= 0. Must be > 0."
        shouldRun = False

# If all the arguments are valid, do the calculations
if shouldRun:
    print "With regular instalments of $" + str(args.m) + " at an interest rate of " + str(args.r) + "% for " + str(args.n) + " periods..."

    # Convert a percentage to decimal form for the equation
    fixedInterestRate = args.r / 100.0

    # Plug all of the numbers into the equation
    amount = args.m * (((1 + fixedInterestRate) ** args.n) - 1) / fixedInterestRate

    print "You have a resulting superannuation of $" + str(round(amount, 2))