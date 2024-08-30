import datetime

def get_user_input():
    # Collect user inputs
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    database_name = input("Enter the database name: ")
    mapping_name = input("Enter the mapping name: ")
    
    action = input("Enter the action (Update, ExportForWebPortal, or ExportToTabDelim): ")
    
    # Generate log file name with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"{database_name}_{timestamp}.log"
    
    host_name = input("Enter the host name (or leave blank for localhost): ")
    
    # Generate output name with timestamp
    output_name = f"{database_name}_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
    
    # Construct command
    command = f"ExpCmdLine -u {username} -p {password} -d {database_name} -m {mapping_name} -a {action}"
    
    command += f" -l {log_file}"
    
    if host_name:
        command += f" -h {host_name}"
    else:
        command += " -h localhost"
    
    command += f" -o {output_name} -w ./specify"
    
    return command

if __name__ == "__main__":
    cmd = get_user_input()
    print("\nGenerated Command:")
    print(cmd)
