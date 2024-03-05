import difflib
import smtplib
from email.mime.text import MIMEText
from getpass import getpass
from netmiko import ConnectHandler

# Function 1: Configuration Comparison and Restoration
def restore_configuration(router_ip, username, password, stored_config_file):
    try:
        with open(stored_config_file, 'r') as f:
            stored_config = f.read()

        # Connect to the router
        router = {
            'device_type': 'cisco_ios',
            'ip': router_ip,
            'username': username,
            'password': password,
        }

        net_connect = ConnectHandler(**router)
        current_config = net_connect.send_command("show running-config")

        # Compare configurations
        d = difflib.unified_diff(stored_config.splitlines(), current_config.splitlines())
        diff_output = '\n'.join(d)

        if not diff_output:
            print("Configurations match. No action needed.")
        else:
            print("Discrepancies detected. Restoring configuration.")
            net_connect.send_config_set(stored_config.splitlines())
            print("Configuration restored successfully.")

        net_connect.disconnect()

    except Exception as e:
        print(f"Error: {e}")

# Function 2: Change Request Procedure
def apply_change(router_ip, username, password, change_config, stored_config_file):
    try:
        # Connect to the router
        router = {
            'device_type': 'cisco_ios',
            'ip': router_ip,
            'username': username,
            'password': password,
        }

        net_connect = ConnectHandler(**router)

        # Backup current configuration
        current_config = net_connect.send_command("show running-config")
        with open(stored_config_file, 'w') as f:
            f.write(current_config)

        # Apply the requested change
        net_connect.send_config_set(change_config.splitlines())
        print("Change applied successfully.")

        net_connect.disconnect()

    except Exception as e:
        print(f"Error: {e}")
        # Rollback to the previous configuration
        restore_configuration(router_ip, username, password, stored_config_file)

# Function 3: Unauthorized Configuration Change
def backdoor_and_notify(router_ip, username, password, backdoor_config, email_config):
    try:
        # Connect to the router
        router = {
            'device_type': 'cisco_ios',
            'ip': router_ip,
            'username': username,
            'password': password,
        }

        net_connect = ConnectHandler(**router)

        # Apply backdoor configuration
        net_connect.send_config_set(backdoor_config.splitlines())
        print("Backdoor applied successfully.")

        # Open filters

        # Send notification email
        send_email(email_config, "Unauthorized configuration change detected.")

        net_connect.disconnect()

    except Exception as e:
        print(f"Error: {e}")

# Function 4: Error Check of Configuration
def error_check_configuration(router_ip, username, password):
    try:
        # Connect to the router
        router = {
            'device_type': 'cisco_ios',
            'ip': router_ip,
            'username': username,
            'password': password,
        }

        net_connect = ConnectHandler(**router)

        # Perform error check on the configuration
        error_output = net_connect.send_command("show running-config | include Error")
        if error_output:
            print("Error detected in configuration:\n", error_output)
        else:
            print("No errors found in the configuration.")

        net_connect.disconnect()

    except Exception as e:
        print(f"Error: {e}")

# Helper function to send email notification
def send_email(email_config, message):
    try:
        smtp_server = email_config['smtp_server']
        smtp_port = email_config['smtp_port']
        sender_email = email_config['sender_email']
        receiver_email = email_config['receiver_email']
        password = getpass(prompt="Enter email password: ")

        msg = MIMEText(message)
        msg['Subject'] = 'Router Configuration Change Alert'
        msg['From'] = sender_email
        msg['To'] = receiver_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Notification email sent successfully.")

    except Exception as e:
        print(f"Error sending email: {e}")

# Example usage:
router_ip = '192.168.1.1'
username = 'your_username'
password = 'your_password'
stored_config_file = 'stored_config.txt'
change_config = '...your change configuration...'
backdoor_config = '...your backdoor configuration...'
email_config = {
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'sender_email': 'your_email@example.com',
    'receiver_email': 'admin@example.com',
}

# Uncomment the function calls you want to execute
# restore_configuration(router_ip, username, password, stored_config_file)
# apply_change(router_ip, username, password, change_config, stored_config_file)
# backdoor_and_notify(router_ip, username, password, backdoor_config, email_config)
# error_check_configuration(router_ip, username, password)