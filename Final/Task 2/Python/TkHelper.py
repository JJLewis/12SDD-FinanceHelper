from Tkinter import *
from GridLocation import *
import tkMessageBox

class TkHelper(object):

    _wraplength = 350

    def showAlert(self, message):
        """
        Show a new window as an alert.

        :param message: The message in the label to be shown
        """
        tkMessageBox.showinfo("Error", message)

    def createHeading(self, parent, title, location=GridLocation(0, 0)):
        """
        Creates and adds a heading label to the top of a frame

        :param parent: A class containing the parent frame of the header label as a variable 'frame'
        :param title: The header text
        :param location: The GridLocation to place the header if it should not be at the top by default
        :return: The created label instance
        """
        label = Label(parent.frame, text=title)
        label.pack(side=LEFT)
        label.grid(row=location.row, column=location.column)
        return label

    def createField(self, parent, name, location, key=None):
        """
        Creates and adds a textfield and a label

        :param parent: A class containing the parent frame of the textfield as a variable 'frame'
        :param name: The name of the field, will be used as a key if key is not explicitly assigned
        :param location: The GridLocation to place the textfield
        :param key: An optional shorter key if the name is too long or inappropriate to use
        :return: (instance of label, instance of the textfield)
        """
        label = self.createLabel(parent, name, location)

        field = Entry(parent.frame)
        field.grid(row=location.row, column=location.column + 1)

        if key == None:
            parent.widgetsDict[name] = field
        else:
            parent.widgetsDict[key] = field

        return (label, field)

    def createLabel(self, parent, title, location):
        """
        Creates a label and adds it to the parent's frame

        :param parent: A class containing the parent frame of the label as a variable 'frame'
        :param title: The context of the label
        :param location: The GridLocation to place the location
        :return: An instance of the label that was created
        """
        label = Label(parent.frame, text=title, wraplength=self._wraplength, anchor=W, justify=RIGHT)
        label.grid(row=location.row, column=location.column)
        return label

    def createNumericalField(self, parent, name, bounds, location, key=None):
        """
        Creates and adds a spinbox and a label

        :param parent: A class containing the parent frame of the spinbox as a variable 'frame'
        :param name: The name of the field, will be used as a key if key is not explicitly assigned
        :param location: The GridLocation to place the textfield
        :param key: An optional shorter key if the name is too long or inappropriate to use
        :return: (instance of label, instance of the spinbox)
        """
        label = self.createLabel(parent, name, location)

        field = Spinbox(parent.frame, from_=bounds[0], to=bounds[1], width=18)
        field.grid(row=location.row, column=location.column + 1)

        if key == None:
            parent.widgetsDict[name] = field
        else:
            parent.widgetsDict[key] = field

        return label, field

    def createDropdown(self, parent, name, options, location):
        """
        Creates and adds a dropdown menu and a label to a frame

        :param parent: A class containing the parent frame of the dropdown menu as a variable 'frame'
        :param name: THe name of the dropdown menu, it is also
        :param options: An array of strings which will become shown as options in the dropdown menu
        :param location: The GridLocation to place the dropdown menu
        :return: (instance of the label, a string variable bound to the value of the selected item in the dropdown menu.
        """
        label = self.createLabel(parent, name, location)

        value = StringVar(parent.frame)
        value.set(options[0])
        dropdown = apply(OptionMenu, (parent.frame, value) + tuple(options))
        dropdown.grid(row=location.row, column=location.column + 1)

        parent.widgetsDict[name] = dropdown

        return label, value

    def createCheckBox(self, parent, name, default, location, onChange):
        """
        Creates and adds a checkbox to a frame

        :param parent: A class containing the parent frame of the checkbox as a variable 'frame'
        :param name: The label text for the checkbox
        :param default: The default value of the checkbox, True for ticked and vice versa.
        :param location: The GridLocation to place the checkbox
        :param onChange: The function to be called when the value of the checkbox changes.
        :return: An instance of the checkbox which was added to the frame
        """
        checkBox = Checkbutton(parent.frame, text=name, command=onChange, wraplength=self._wraplength)
        checkBox.grid(row=location.row, column=location.column, columnspan=2)
        if default:
            checkBox.select()
        return checkBox

    def createButton(self, parent, title, action, location):
        """
        Creates and adds a button to a frame

        :param parent: A class containing the parent frame of the button as a variable 'frame'
        :param title: The title of the button
        :param action: The function ot be called when the value of the checkbox changes.
        :param location: The GridLocation to place the button
        :return: An instance of the button that was added to the frame
        """
        button = Button(parent.frame, text=title, command=action)
        button.grid(row=location.row, column=location.column)
        return button

    def createListBox(self, parent, title, options, location):
        """
        Creates and adds a listbox to a frame

        :param parent: A class containing the parent frame of the listbox as a variable 'frame'
        :param title: The heading/title of the list box
        :param options: An array of strings to be the available options to pick from
        :param location: The GridLocation to place the listbox
        :return: Instance of the listbox
        """
        label = self.createLabel(parent, title, location)

        list = Listbox(parent.frame, selectmode=MULTIPLE, height=len(options))
        for i in range(0, len(options)):
            list.insert(i, options[i])

        list.grid(row=location.row, column=location.column + 1)

        parent.widgetsDict[title] = list

        return list