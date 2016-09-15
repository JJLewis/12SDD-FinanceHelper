class GridLocation:
    """
    This is just a container to have slightly cleaner code for the TKHelper
    I would have used a struct if Python had them... but no. so it's a class
    """
    row = 0
    column = 0

    def __init__(self, x, y):
        self.column = x
        self.row = y