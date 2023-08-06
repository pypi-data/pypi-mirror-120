import pywhatkit
import pyfiglet
import time
import sys
from colorama import Fore,Style

def info():
    print(Fore.YELLOW + "----------------------------------------------------------------------------------------------------------------------------------------"+Style.RESET_ALL)
    message = "Welcome to pyHand python package developed by Sujith Sourya Yedida ! Please go through the following information of this python package"

    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)

    print(Fore.YELLOW + "\n----------------------------------------------------------------------------------------------------------------------------------------")

    print(Style.RESET_ALL)

    time.sleep(2)

    print("pyHand : This is a package developed by Sujith Sourya Yedida which is used to convert text to handwritten ")

    print()
    print("-----------------------------------------------------------------------------")
    print("Name : " + Fore.RED + "pyHand" + Style.RESET_ALL)
    print("Version : " + Fore.RED + "1.0.1" + Style.RESET_ALL)
    print("Developer : " + Fore.RED + "Sujith Sourya Yedida" + Style.RESET_ALL)
    print("Producer : " + Fore.RED + "TS³" + Style.RESET_ALL)
    print("-----------------------------------------------------------------------------")
    print()
    print("-----------------------------------------------------------------------------------------------------")
    print(Fore.YELLOW + "* pyHand MANUEL developed by Sujith Sourya Yedida *" + Style.RESET_ALL)
    print("To install this package we need to " + Fore.RED + "pip install pyHand" + Style.RESET_ALL)
    print()
    print("We need to import this package : "  + Fore.RED + "import pyHand" + Style.RESET_ALL)
    print("To get the information, we need to use the following command : " + Fore.RED + "pyHand.info()" + Style.RESET_ALL)
    print("To convert text to handwritten , we need use the following command : " + Fore.RED + "pyHand.write('Sample Text')" + Style.RESET_ALL)
    print()
    print("Then you can choose the name for you file ")
    print("Then you can find the handwritten text on your desktop screen with name that you have given above.")
    print("-----------------------------------------------------------------------------------------------------")
    print()
    print(Fore.YELLOW + "@SujithSouryaYedida" + Style.RESET_ALL)
    print()

def write(a):

    logo = pyfiglet.figlet_format('pyHand')
    print(logo)
    print()

    file_name = input("File name : ")

    print(Fore.YELLOW + "\nMaking the hand written text ......." + Style.RESET_ALL)
    pywhatkit.text_to_handwriting(a,f"C:\\Users\\Lenovo\\Desktop\\{file_name}.png",rgb=[0,255,0])

    success = f"\n* Please find your handwritten text in the desktop with name {file_name}.png file *\n"

    for char in success:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)

    print()
    print(Fore.YELLOW + "@SujithSouryaYedida" + Style.RESET_ALL)
    print()