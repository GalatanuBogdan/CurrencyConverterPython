from CurrenciesController import CurrencyController
from GUIController import GUIController


class CurrencyConverterApp:
    _begin_from_currency = "USD"
    _begin_to_currency = "RON"

    def __init__(self):
        guiController = GUIController.get_gui_controller()

        currenciesController = CurrencyController.get_currency_controller()

        currenciesController.update_currencies_rates()

        bnrCurrencies = currenciesController.get_currency_rates()

        guiController.update_input_entry_text("1", CurrencyConverterApp.validate_and_convert_amount)

        guiController.update_title(self._begin_from_currency, self._begin_to_currency)
        guiController.update_input_dropdown(self._begin_from_currency, list(bnrCurrencies.keys()),
                                            CurrencyConverterApp.validate_and_convert_amount)
        guiController.update_output_dropdown(self._begin_to_currency, list(bnrCurrencies.keys()),
                                             CurrencyConverterApp.validate_and_convert_amount)

        CurrencyConverterApp.validate_and_convert_amount()

        guiController.begin_play()

    @staticmethod
    def validate_and_convert_amount(*args):
        currenciesController = CurrencyController.get_currency_controller()
        guiController = GUIController.get_gui_controller()

        if currenciesController.should_sync_rates():
            currenciesController.update_currencies_rates()

        guiController.make_entry_input_valid()

        entryInputValue = guiController.get_input_value()

        if len(entryInputValue) == 0:
            entryInputValue = "0"

        if len(entryInputValue) == 1 and entryInputValue[0] == '.':
            entryInputValue = "0"

        convertedAmount = currenciesController.convert_amount(float(entryInputValue),
                                                              guiController.get_from_currency(),
                                                              guiController.get_to_currency())
        guiController.update_output_entry_text(str(convertedAmount))
        guiController.update_title(guiController.get_from_currency(), guiController.get_to_currency())
