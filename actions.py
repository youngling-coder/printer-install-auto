import subprocess
from custom_inputs import get_yn_confirmation


def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
    else:
        print("Success:", result.stdout)


def install_printer(
    ip_address, printer_name, driver_inf_path, driver_name, port_name=None
):

    proceed_installation = get_yn_confirmation("Procceed with installation? [Y/n]: ")

    if proceed_installation:
        if not port_name:
            port_name = f"IP_{ip_address}"

        # Step 1: Create TCP/IP port
        port_command = (
            f'cscript "C:\\Windows\\System32\\Printing_Admin_Scripts\\de-DE\\prnport.vbs" '
            f"-a -r {port_name} -h {ip_address} -o raw -n 9100"
        )
        run_command(port_command)

        # Step 2: Add driver using INF
        driver_command = f'pnputil /add-driver "{driver_inf_path}" /install'
        run_command(driver_command)

        # Step 3: Install printer
        install_command = (
            f'rundll32 printui.dll,PrintUIEntry /if /b "{printer_name}" /r "{port_name}" '
            f'/f "{driver_inf_path}" /m "{driver_name}" /z'
        )
        run_command(install_command)

        print(f"✅ Printer '{printer_name}' installed successfully!")
