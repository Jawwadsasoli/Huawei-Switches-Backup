# Huawei Device Backup Script

This Python script automates the process of backing up the configuration of Huawei network devices. It establishes an SSH connection to each device, retrieves the current configuration, and saves it to a backup file in a specified directory. Failed backups are logged in a separate file for troubleshooting.

## Features

- Backs up the configuration of Huawei network devices via SSH.
- Automatically extracts the device's sysname to name the backup file.
- Handles dynamic prompts during the saving process on different switches.
- Logs failed backup attempts for review.

## Prerequisites

To use this script, ensure you have the following installed:

- Python 3.x
- `netmiko` Python library (for SSH connections)

You can install `netmiko` using pip:

```bash
pip install netmiko

**Setup**
Create a file named device_ips.txt in the script's directory. This file should contain a list of IP addresses (one per line) of the Huawei devices you want to back up.

**Example device_ips.txt:**

Copy code
192.168.1.1
192.168.1.2
192.168.1.3

Run the script by executing it in your terminal or command prompt.

**Usage**
Clone the repository or download the script.

**Run the script:**
bash
python backup_script.py
The script will prompt you for your Huawei device login credentials (username and password). Once entered, the script will attempt to back up each device listed in the device_ips.txt file.

Backup files will be saved in the Huawei_Backups/ directory with the format:

sysname_backup_YYYYMMDD_HHMMSS.txt
Failed backups will be logged in Huawei_Backups/failed_backups.txt.

**Example Output**

Backup completed for Device1. File saved as Huawei_Backups/Device1_backup_20231015_134500.txt
Failed to backup 192.168.1.2: Authentication failure
Notes
Ensure the devices listed in device_ips.txt are accessible over SSH.
The script handles multiple save prompts that may appear on different Huawei devices.
Session logs for each device are saved in the Huawei_Backups folder for debugging purposes.
Troubleshooting
If a device backup fails, the error message will be logged in failed_backups.txt. Check this log for details and investigate connectivity or authentication issues with the device.

**License**
This project is licensed under the MIT License.

This `README.md` file explains how to set up, use, and troubleshoot your backup script. You can modi
