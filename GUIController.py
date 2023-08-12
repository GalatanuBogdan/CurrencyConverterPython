import string
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Label, Entry, OptionMenu


class GUIController:
    __instance = None

    @staticmethod
    def get_gui_controller():
        if GUIController.__instance is None:
            GUIController()
        return GUIController.__instance

    def __init__(self):
        if GUIController.__instance is not None:
            raise Exception("GUIController: Singleton cannot be instantiated more than once!")

        self._mainWindow = tk.Tk()
        self._mainWindow.geometry("450x180")
        self._mainWindow.title('Currency Converter')
        self._mainWindow.iconbitmap('icon.ico')

        self._titleText = tk.StringVar()
        self._titleText = ""
        self._title = Label(self._mainWindow, text=self._titleText, font=("Arial", 20))
        self._title.grid(row=0, padx=(50, 0), pady=30)

        self._amountEntryValue = tk.StringVar()
        self._amountEntryValue.set("1")
        self._amountEntry = Entry(self._mainWindow)
        self._amountEntry.configure(textvariable=self._amountEntryValue)
        self._amountEntry.grid(row=1, column=0, sticky='WE', padx=(20, 10), pady=(0, 10))

        self._inputDropdownValue = tk.StringVar()
        self._inputDropdownValue.set("")
        self._inputDropdown = OptionMenu(self._mainWindow, self._inputDropdownValue)
        self._inputDropdown.grid(row=1, column=1, sticky='WE', padx=(0, 20), pady=(0, 10))
        self._inputDropdown['direction'] = 'above'

        self._outputEntryValue = tk.StringVar()
        self._outputEntry = Entry(self._mainWindow)
        self._outputEntry.configure(textvariable=self._outputEntryValue)
        self._outputEntry.grid(row=2, column=0, sticky='WE', padx=(20, 10), pady=(0, 20))
        self._outputEntry.config(state="disabled")

        self._outputDropdownValue = tk.StringVar()
        self._outputDropdownValue.set("")
        self._outputDropdown = OptionMenu(self._mainWindow, self._outputDropdownValue)
        self._outputDropdown.grid(row=2, column=1, sticky='WE', padx=(0, 20), pady=(0, 20))

        GUIController.__instance = self

    def make_entry_input_valid(self):
        supported_chars = "0123456789."

        validInput = ""
        # remove all invalid characters from entryInput
        for char in self.get_input_value():
            if char in supported_chars:
                validInput += char

                # avoid adding multiple '.'
                if char == '.':
                    supported_chars = supported_chars.replace('.', '')

        self._amountEntryValue.set(validInput)

    def update_title(self, fromCurrencyName: string, toCurrencyName: string):
        self._titleText = "Convert from {} to {}".format(fromCurrencyName, toCurrencyName)
        self._title.config(text=self._titleText)

    def update_input_entry_text(self, value: string, updateCallback):
        self._amountEntryValue.set(value)
        self._amountEntryValue.trace('w', updateCallback)
        self._amountEntryValue.trace('r', updateCallback)
        self._amountEntryValue.trace('u', updateCallback)

    @staticmethod
    def __update_option_menu(optionMenu: OptionMenu, newSelectedValue: string, currentSelectedValue: tk.StringVar,
                             newOptions: list, updateCallback):
        menu = optionMenu["menu"]
        menu.delete(0, "end")

        for value in newOptions:
            menu.add_command(label=value, command=lambda x=value: currentSelectedValue.set(x))

        currentSelectedValue.set(newSelectedValue)
        currentSelectedValue.trace('w', updateCallback)

    def update_input_dropdown(self, fromCurrency: string, currencies: list, updateCallback):
        self.__update_option_menu(self._inputDropdown, fromCurrency, self._inputDropdownValue, currencies,
                                  updateCallback)

    def update_output_dropdown(self, toCurrency: string, currencies: list, updateCallback):
        self.__update_option_menu(self._outputDropdown, toCurrency, self._outputDropdownValue, currencies,
                                  updateCallback)

    def get_from_currency(self):
        return self._inputDropdownValue.get()

    def get_to_currency(self):
        return self._outputDropdownValue.get()

    def get_input_value(self):
        return self._amountEntryValue.get()

    def update_output_entry_text(self, value: string):
        self._outputEntryValue.set(value)

    def begin_play(self):
        self._mainWindow.geometry("450x180")
        self._mainWindow.resizable(False, False)
        self._mainWindow.mainloop()

    def show_error_message(self, title: str, textMessage: str):
        self._mainWindow.geometry("0x0")
        messagebox.showerror(title, textMessage)
        sys.exit()
