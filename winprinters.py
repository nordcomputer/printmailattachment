import win32api
import win32print
from glob import glob

# A List containing the system printers
all_printers = [printer[2] for printer in win32print.EnumPrinters(3)]

# Ask the user to select a printer
print("Printer:\n"+"\n".join([f"{n} {p}" for n, p in enumerate(all_printers)])+"\n")

# set the default printer
# win32print.SetDefaultPrinter(all_printers[printer_num])

# for f in glob(pdf_dir, recursive=True):
#     win32api.ShellExecute(0, "print", f, None,  ".",  0)
# pdf_file_name = "C:/Users/nn/sample.pdf"
# win32api.ShellExecute(0, "print", pdf_file_name, None, ".", 0)

input("press any key to exit")