import string
from datetime import datetime
import pytz
import requests
from GUIController import GUIController


class CurrencyController:
    __instance = None

    _bnr_server_update_rates_hour = 13
    _last_server_sync_time = None

    @staticmethod
    def get_currency_controller():
        if CurrencyController.__instance is None:
            CurrencyController()
        return CurrencyController.__instance

    def __init__(self):
        if CurrencyController.__instance is not None:
            raise Exception("CurrencyController: Singleton cannot be instantiated more than once!")
        else:
            self._mCurrencyRates = dict()
            CurrencyController.__instance = self

    def get_currency_rates(self) -> dict:
        return self._mCurrencyRates

    def should_sync_rates(self):
        if self._last_server_sync_time is None:
            return True  # rates was never updated

        # get Bucharest time
        current_bucharest_time = datetime.now(pytz.timezone('Europe/Bucharest'))

        last_sync_was_done_today = current_bucharest_time.day == self._last_server_sync_time.day

        bnr_uploaded_new_rates = current_bucharest_time.hour >= self._bnr_server_update_rates_hour

        saved_rates_are_behind = self._last_server_sync_time.hour < self._bnr_server_update_rates_hour

        last_sync_was_done_today_but_with_old_rates = last_sync_was_done_today and bnr_uploaded_new_rates and saved_rates_are_behind

        if last_sync_was_done_today_but_with_old_rates:
            return True

        lastSyncWasDoneInAPreviousDay = current_bucharest_time.year > self._last_server_sync_time.year or current_bucharest_time.month > self._last_server_sync_time.month or current_bucharest_time.day > self._last_server_sync_time.day

        if lastSyncWasDoneInAPreviousDay and bnr_uploaded_new_rates:
            return True

        return False

    def update_currencies_rates(self):
        url = "https://www.bnr.ro/nbrfxrates.xml"

        payload = {}
        headers = {
            'Cookie': 'TS01cc05a4=0187e48c1b62584c7501d9c3c5b698af0932675a597bbae5c3271cbb7da06be624d6602a8b5d797c161b47287a901787dacd097b40'
        }

        guiController = GUIController.get_gui_controller()
        response = None

        try:
            response = requests.request("GET", url, headers=headers, data=payload)
        except requests.exceptions.Timeout:
            guiController.show_error_message("Network Problem", "Connection timeout! Try again later!")
        except requests.exceptions.TooManyRedirects:
            guiController.show_error_message("Network Problem", "Too many redirects! Try again later!")
        except requests.exceptions.ConnectionError:
            guiController.show_error_message("Network Problem", "Please Check your internet connection and try again!")
        except requests.exceptions.RequestException as e:
            guiController.show_error_message("Network Problem", "Unknown Error! Contact support!")
            raise SystemExit(e)

        self._mCurrencyRates = dict()

        import xml.etree.ElementTree
        tree = xml.etree.ElementTree.fromstring(response.text)
        for elem in tree.iter():
            if "currency" in elem.attrib:
                if "multiplier" in elem.attrib:
                    self._mCurrencyRates[elem.attrib["currency"]] = float(elem.text) * float(elem.attrib["multiplier"])
                else:
                    self._mCurrencyRates[elem.attrib["currency"]] = float(elem.text)

        # separately add RON
        self._mCurrencyRates["RON"] = 1

        self._last_server_sync_time = datetime.now(pytz.timezone('Europe/Bucharest'))

    def convert_amount(self, amount: float, fromCurrencyName: string, toCurrencyName: string):

        fromCurrencyRonAmount = self._mCurrencyRates[fromCurrencyName]
        toCurrencyRonAmount = self._mCurrencyRates[toCurrencyName]

        return fromCurrencyRonAmount / toCurrencyRonAmount * amount
