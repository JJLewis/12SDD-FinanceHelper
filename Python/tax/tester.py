def calculateTaxable(income):
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

dataSet = [100,18200,18201,19000,37000,37001,38000,80000,80001,81000,180000,180001,200000]

for data in dataSet:
    print calculateTaxable(data)