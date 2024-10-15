import os
import time
from netmiko import ConnectHandler

# Create a backup directory
BACKUP_DIR = "Huawei_Backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Function to extract sysname from the full configuration
def extract_sysname(config_output):
    for line in config_output.splitlines():
        if "sysname" in line:
            return line.split()[-1].strip()
    return "unknown_device"

# Function to backup a single device
def backup_device(device_info, failed_log):
    try:
        # Establish an SSH connection
        connection = ConnectHandler(**device_info, global_delay_factor=4, banner_timeout=200)

        # Disable paging
        connection.send_command("screen-length 0 temporary")

        # Fetch and save the configuration
        config = connection.send_command_timing("display current-configuration", delay_factor=4, max_loops=5000)
        hostname = extract_sysname(config)
        save_output = connection.send_command_timing("save", delay_factor=4)



                # Dynamic handling for saving configuration across different switches
        save_prompts = [
             "Are you sure to continue?[Y/N]",  # Common prompt on some Huawei devices
            "This will overwrite the previous configuration. Are you sure?",  # Example of another possible prompt
            "Confirm to save the configuration? [Y/N]",  # Another common variant
            '''The current configuration (excluding the configurations of unregistered boards or cards) will be written to flash:/vrpcfg.zip.
             Are you sure to continue? [Y/N]''',
             "Warning: The current configuration will be written to the device. Continue? [Y/N]:"
            ]
        for prompt in save_prompts:
            if prompt in save_output:
             save_output += connection.send_command_timing("y", delay_factor=4)
            if "Success" not in save_output:
             raise Exception("Failed to save configuration.")

        # Close the connection
        connection.disconnect()

        # Save the configuration to a file
        backup_filename = os.path.join(BACKUP_DIR, f"{hostname}_backup_{time.strftime('%Y%m%d_%H%M%S')}.txt")
        with open(backup_filename, "w") as backup_file:
            backup_file.write(config)

        print(f"Backup completed for {hostname}. File saved as {backup_filename}")

    except Exception as e:
        # Log the failure
        failed_log.write(f"{device_info['host']} - {str(e)}\n")
        print(f"Failed to backup {device_info['host']}: {str(e)}")

# Main function to read IP list and perform backups
def main():
    # Define login credentials
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Absolute path for the IP list file
    ip_list = r"device_ips.txt"

    if not os.path.exists(ip_list):
        print(f"IP list file {ip_list} not found.")
        return

    # Open a log file for failed backups
    with open(os.path.join(BACKUP_DIR, "failed_backups.txt"), "w") as failed_log:

        with open(ip_list, "r") as file:
            devices = file.readlines()

        for ip in devices:
            ip = ip.strip()
            if ip:
                # Device information
                device_info = {
                    'device_type': 'huawei',
                    'host': ip,
                    'username': username,
                    'password': password,
                    'secret': password,  # Enable password if required (default same as login password)
                    'session_log': os.path.join(BACKUP_DIR, f"session_log_{ip}.txt")
                }

                # Perform the backup
                backup_device(device_info, failed_log)

if __name__ == "__main__":
    main()