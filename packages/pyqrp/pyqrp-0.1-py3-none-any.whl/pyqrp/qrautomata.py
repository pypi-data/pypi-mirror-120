"""
qrautomata.py - Part of PyQRP

:author: George <drpresq@gmail.com>
:description: PyQRP Automata Module - Handles Automated entry of Data into Pilot PoS
:license: GPL3
:donation:
    BTC - 15wRP3NGm2zQwsC36gYAMf8ZaBNuDP6BiR
    LTC - LQANeFg6qhEUCftCGpXTdgCKnPkBMR5Ems
"""

import pyautogui
import sys
import time
from subprocess import Popen
from typing import Union
from pyqrp import qrxls


class WarningWindow:

    def __init__(self, delay: int) -> None:
        message: str = "Click in the first data field! Executing in {} seconds!"
        pyautogui.alert(text=message.format(delay),
                        title="PyQrp: WARNING!",
                        timeout=delay*1000)


def automata(input_data: Union[qrxls.QRXls, qrxls.QRXlsx]) -> None:
    delay: int = 10

    # Display the warning window
    warning_box: Popen = Popen([sys.executable,
                                "-c",
                                f"from pyqrp.qrautomata import WarningWindow; win = WarningWindow({delay})"])

    # Iterates through Workbooks (books) in QRXl(x)s Object
    # book.keys(["name", "index", "data"])
    time.sleep(delay)
    for book in input_data:
        # Iterates through rows in books
        # row.keys(["PREP ITEM", "F/STOCK"])
        for row in book[list(book.keys())[2]]:
            # Writes the data from the second column then presses enter
            pyautogui.write(str(row[list(row.keys())[1]]))
            pyautogui.press('enter')

    warning_box.terminate()
