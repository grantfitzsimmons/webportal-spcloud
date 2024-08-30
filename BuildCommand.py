import datetime
import os
import platform

def get_user_input():
    # Collect user inputs
    database_name = input("Enter the database name: ")
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    mapping_name = input("Enter the mapping name: ")
    
    action = input("Enter the action (Update, ExportForWebPortal, or ExportToTabDelim): ")
    
    # Generate log file name with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"{database_name}_{timestamp}.log"
    
    # Specify the logs directory
    logs_directory = "logs"
    
    # Ensure the logs directory exists
    os.makedirs(logs_directory, exist_ok=True)
    
    # Update log file path
    log_file_path = os.path.join(logs_directory, log_file)
    
    host_name = input("Enter the host name (or leave blank for localhost): ")
    
    # Generate output name with timestamp
    output_name = f"{database_name}_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
    
    # Auto-detect the operating system
    os_name = platform.system().lower()
    
    # Determine the command based on the operating system
    if os_name == "windows":
        command_prefix = "ExpCmdLine"
    elif os_name == "linux":
        command_prefix = "./ExpCmdLine.sh"
    elif os_name == "darwin": #macOS
        command_prefix = "./ExpCmdLine"
    else:
        print("Unsupported operating system detected.")
        return None  # Exit the function if the OS is unsupported
    
    # Construct command with quotes around username, password, and mapping_name
    command = f"{command_prefix} -u \"{username}\" -p \"{password}\" -d {database_name} -m \"{mapping_name}\" -a {action}"
    
    command += f" -l {log_file_path}"  # Use the log file path
    
    if host_name:
        command += f" -h {host_name}"
    else:
        command += " -h localhost"
    
    command += f" -o {output_name} -w ./specify"
    
    return command

if __name__ == "__main__":
    cmd = get_user_input()
    if cmd:  # Only print the command if it's valid
        print("\nGenerated Command:")
        print(cmd)
