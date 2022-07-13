import usb

def is_printer(dev):
    if dev.bDeviceClass == 7:
        return True
    for cfg in dev:
        if usb.util.find_descriptor(cfg, bInterfaceClass=7) is not None:
            return True

for printer in usb.core.find(find_all=True, custom_match = is_printer):
    print('Decimal VendorID=' + str(printer.idVendor) + ' & ProductID=' + str(printer.idProduct) + '\n')
    print('Hexadecimal VendorID=' + hex(printer.idVendor) + ' & ProductID=' + hex(printer.idProduct) + '\n\n')