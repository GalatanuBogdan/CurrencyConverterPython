# Currency Converter Application

## Description
This Python application provides a graphical user interface (GUI) for currency conversion. It allows users to convert an amount of money from one currency to another using the official exchange rates fetched from the National Bank of Romania (BNR) API. The application automatically updates the exchange rates from the BNR API to ensure accurate conversions.

## Features
- User-friendly GUI for easy interaction.
- Convert an input amount from one currency to another.
- Automatically fetches the latest exchange rates from the BNR API.
- Supports all currencies available in the BNR API.

## Usage
1. Launch the application.
2. Select the input amount, source, and target currency from the provided dropdown menus.
3. Click the "Convert" button to perform the currency conversion.
4. The converted amount will be displayed on the screen.

## Automatic Updates
- The application periodically checks for updates on the BNR API to ensure accurate exchange rates.
- If an update is detected, the application automatically fetches the latest exchange rates and updates the conversion calculations.
- Users are not required to trigger the update process manually.

## Installation
1. Clone or download this repository.
2. Open a terminal and run the following commands:
   ```bash
   pip install py2exe
   python setup.py py2exe
3. In the dist folder you should find an executable to open


