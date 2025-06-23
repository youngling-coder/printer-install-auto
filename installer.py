import subprocess
from colorama import Fore, Style
from custom_inputs import get_yn_confirmation


class Installer:
    def __init__(self, printer):
        self.__printer = printer

    def run(self, port_name=None):

        action_confirmed = get_yn_confirmation("Procceed with installation? [Y/n]: ")

        is_printer_available = self.__printer.is_available()

        if not is_printer_available:
            print(f"{Style.BRIGHT + Fore.RED}❌ Printer is unavailable!")
            return

        if action_confirmed:
            if not port_name:
                port_name = f"IP_{self.__printer.ip}"

            # Step 1: Create TCP/IP port
            port_command = (
                f'cscript "C:\\Windows\\System32\\Printing_Admin_Scripts\\de-DE\\prnport.vbs" '
                f"-a -r {port_name} -h {self.__printer.ip} -o raw -n 9100"
            )
            self.__run_command(port_command)

            # Step 2: Add driver using INF
            driver_command = (
                f'pnputil /add-driver "{self.__printer.driver_inf_path}" /install'
            )
            self.__run_command(driver_command)

            # Step 3: Install printer
            install_command = (
                f'rundll32 printui.dll,PrintUIEntry /if /b "{self.__printer.name}" /r "{port_name}" '
                f'/f "{self.__printer.driver_inf_path}" /m "{self.__printer.driver_name}" /z'
            )
            self.__run_command(install_command)

            print(f"✅ Printer '{self.__printer.name}' installed successfully!")

    @staticmethod
    def __run_command(command):
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error:", result.stderr)
        else:
            print("Success:", result.stdout)
