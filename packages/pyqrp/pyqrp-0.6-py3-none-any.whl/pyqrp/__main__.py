import pyautogui
from pathlib import Path
from pyqrp import qrxls, qrautomata
from typing import Union

data = None

if file_path := pyautogui.prompt(text="Please enter the full path to your file."):
    file_path = Path(file_path) if Path(file_path).exists() and Path(file_path).is_file() else file_path
    while isinstance(file_path, str):
        file_path = pyautogui.prompt(text="Error: Please enter the full path to your file.", default=file_path)
        file_path = Path(file_path) if Path(file_path).exists() and Path(file_path).is_file() else file_path

    if isinstance(file_path, Path):
        data: Union[qrxls.QRXls, qrxls.QRXlsx, None] = \
            qrxls.QRXls(file_path=file_path) if file_path.__str__().split(".")[-1] == "xls" else \
            qrxls.QRXlsx(file_path=file_path) if file_path.__str__().split(".")[-1] == "xlsx" else \
            None

        if data:
            qrautomata.automata(input_data=data)

exit(0)
