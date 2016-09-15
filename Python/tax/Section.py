from Tkinter import *

class Section(object):

    def contains(self, arr, value):
        """
        Check if an item exists in an array

        :param arr: The array
        :param value: The value to check if exists in array
        :return: True if it exists and false if it doesn't
        """
        try:
            arr.index(value)
        except:
            return False
        return True

    def validateDataTypes(self):
        """
        Iterates over the arrays containing the fields that require integer and float data types
        Does a type conversion and if it fails and the try, except fails,
        It will know that the data entered was not of the right type

        :return: True if all is correct, False if any one is wrong
        """
        try:
            for check in self.requiredInt:
                if not self.contains(self.notRequiredFields, check):
                    int(check.get())
            for check in self.requiredFloat:
                if not self.contains(self.notRequiredFields, check):
                    float(check.get())
        except:
            return False
        return True

    def isSectionComplete(self):
        """
        Checks if this section is complete
        Done by iterating over every widget and getting its value
        Since the only fields that need checking are textfields, will only check with those
        Also takes into account widgets that are not required and ignores them

        :return: True if it is complete, False if not
        """
        for _, widget in self.widgetsDict.iteritems():
            if not self.contains(self.notRequiredFields, widget):
                if isinstance(widget, Entry):
                    if widget.get().strip() == "":
                        return False
        return True

    def extractedDataDict(self):
        """
        Steps through every item in the widgetsDict and maps the keys to the widget's value
        This function is overridden by the Address Section as Optionmenus are handled a bit differently.

        :return: A dictionary with the same keys but the values of the widgets rather than the widgets
        """
        dataDict = {}
        for key, value in self.widgetsDict.iteritems():
            if isinstance(value, Entry) or isinstance(value, Spinbox):
                dataDict[key] = value.get()
            elif isinstance(value, Listbox):
                dataDict[key] = value.curselection()
        return dataDict

    def toggleField(self, show, field, label):
        """
        A convenience function to get rid of repetitive show and hide code associated with checkboxes

        :param show: Whether or not the field and label should be shown
        :param field: The field to be shown or hidden and added; The field to be added to the notRequired list
        :param label: The label to be shown or hidden
        """
        if show:
            field.grid()
            label.grid()
            self.notRequiredFields.remove(field)
        else:
            field.grid_remove()
            label.grid_remove()
            self.notRequiredFields.append(field)

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()

    def __init__(self, controller, heading):
        self.controller = controller
        self.frame = LabelFrame(controller.root, text=heading, font="Helvetica 20 bold")
        self.frame.grid()
        self.widgetsDict = {}
        self.notRequiredFields = []
        self.requiredInt = []
        self.requiredFloat = []
        self.requiredCheck = [self.requiredInt, self.requiredFloat]