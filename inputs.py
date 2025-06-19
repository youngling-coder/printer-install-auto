from typing import Optional
from colorama import Style, Fore
from utils import help_
from utils import prettified_locations_output, prettified_printer_output
from storage import Storage, Printer, Location
import sys, os


printer_base_data = {
      "ip": "",
      "name": "",
      "driver_inf_path": "",
      "model": ""
    }


def get_generic_input(prompt: str, empty: bool = True) -> str:

    while True:
        value = input(prompt)

        if value.lower() == "exit":
            sys.exit(0)
        
        if not empty and not value.strip():
            continue

        return value

    
def get_yn_confirmation(prompt: str) -> bool:

    confirmation = get_generic_input(Style.BRIGHT + prompt + Style.RESET_ALL)

    return confirmation.lower().startswith("y") or confirmation == ""


def get_ip_input(storage: Storage) -> str:

    while True:

        try:
            value = get_generic_input("Enter printer's IP address: ")

            if not storage.is_ip_valid(value):
                raise ValueError(f"{Style.BRIGHT + Fore.RED}Entered IP is invalid!{Style.RESET_ALL}")
            
            return value
        
        except ValueError as e:
            print(e)
        

def get_integer_input(prompt: str, range_: Optional[range] = None):
     
    while True:
        try:
            value = int(get_generic_input(prompt))

            if range_ and (value not in range_):
                raise IndexError(f"{Style.BRIGHT + Fore.RED}Value is out of range!{Style.RESET_ALL}")
            
            return value
        
        except ValueError:
            print(f"{Style.BRIGHT + Fore.RED}Incompatible value!{Style.RESET_ALL}")
            continue

        except IndexError as e:
            print(e)
            continue


def get_printer_id_input(location: Location):
    for idx, printer in enumerate(location.get_printers()):
        print(prettified_printer_output(idx, printer))

    printer_id = get_integer_input(f"Select printer: ", range_=range(1, len(location.get_printers())+1))
    
    return printer_id


def get_location_id_input(locations: Location) -> int:
    
    print()
    print(prettified_locations_output(locations))

    location = get_integer_input("Enter city number: ", range_=range(1, len(locations)+1))
    print()
    
    return location-1


def get_current_action():
    help_()

    current_action = get_integer_input("Enter action you want to perform: ", range_=range(1, 4))

    return current_action


def get_printer_data(storage: Storage) -> tuple[Printer, Location]:

    while True:
        os.system("cls")

        location = storage.get_location_by_id(get_location_id_input(storage.get_locations()))
        new_printer = printer_base_data.copy()

        new_printer["ip"] = get_ip_input(storage)
        new_printer["name"] = get_generic_input(f"Enter printer's name: ", empty=False)
        new_printer["model"] = get_generic_input(f"Enter printer's model: ", empty=False)
        new_printer["driver_name"] = get_generic_input(f"Enter printer's driver name: ", empty=False)
        new_printer["driver_inf_path"] = get_generic_input(f"Enter printer's driver path: ", empty=False)
        printer = Printer.from_dict(new_printer)

        print()
        print(prettified_printer_output(0, printer))
        print(f"{Style.BRIGHT}Will be added to \"{Fore.CYAN + location.name.capitalize() + Fore.RESET}\"")

        check_data = get_yn_confirmation("Is this correct? [Y/n]: ")

        if check_data:
            break
        
    

    return printer, location