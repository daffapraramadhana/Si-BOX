import os, sys
import win32print

p = win32print.OpenPrinter('POS-X Thermal Printer')
h = "hello world!"

job = win32print.StartDocPrinter (p, 1, ("test of raw data", None, "RAW")) 
win32print.StartPagePrinter (p) 
win32print.WritePrinter (p,  h.encode('utf-8')) 
win32print.EndPagePrinter (p)