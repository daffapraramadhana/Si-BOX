import winreg as reg
import os            
 
def AddToRegistry():
 
    address= os.path.realpath('D:\Si BOX\run.vbs')
     
    # key we want to change is HKEY_CURRENT_USER
    # key value is Software\Microsoft\Windows\CurrentVersion\Run
    key = reg.HKEY_CURRENT_USER
    key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
     
    # open the key to make changes to
    open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)
     
    # modify the opened key
    reg.SetValueEx(open,"sibox",0,reg.REG_SZ,address)
     
    # now close the opened key
    reg.CloseKey(open)
 
# Driver Code
if __name__=="__main__":
    AddToRegistry()