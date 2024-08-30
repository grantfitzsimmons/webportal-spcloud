import mariadb
import getpass
import subprocess
import time

def create_ssh_tunnel(ssh_host, ssh_user, ssh_password, ssh_port=22):
    """Create an SSH tunnel to the MySQL server."""
    try:
        # Create the SSH command to establish a tunnel
        ssh_command = [
            "ssh",
            "-N",  # Do not execute a remote command
            f"{ssh_user}@{ssh_host}",
            "-p", str(ssh_port)
        ]

        # Start the SSH tunnel
        print("Establishing SSH tunnel...")
        ssh_process = subprocess.Popen(ssh_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait a moment to ensure the tunnel is established
        time.sleep(2)
        print("SSH tunnel established.")
        return ssh_process
    except Exception as e:
        print(f"Error creating SSH tunnel: {e}")
        return None

def get_database_connection(hostname, username, password, database):
    """Establish a connection to the MariaDB database."""
    try:
        connection = mariadb.connect(
            host=hostname,
            user=username,
            password=password,
            database=database
        )
        print("Successfully connected to the database.")
        return connection
    except mariadb.Error as e:
        print(f"Error: {e}")
        return None

def fetch_schema_mappings(connection):
    """Fetch schema mappings, collections, and disciplines from the database."""
    query = """
    SELECT em.MappingName, c.CollectionName, d.Name
    FROM spexportschemamapping em
    JOIN collection c ON c.UserGroupScopeId = em.CollectionMemberID
    JOIN discipline d ON c.DisciplineID = d.disciplineId;
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        print("\nSchema Mappings:")
        print(f"{'Mapping Name':<30} {'Collection Name':<30} {'Discipline Name'}")
        print("=" * 80)
        for row in results:
            mapping_name, collection_name, discipline_name = row
            print(f"{mapping_name:<30} {collection_name:<30} {discipline_name}")
        
    except mariadb.Error as e:
        print(f"Error fetching data: {e}")
    finally:
        cursor.close()

def main():
    # Ask the user if they want to connect via SSH
    ssh_needed = input("Do you need to connect via SSH? (yes/no): ").strip().lower()
    
    ssh_process = None
    if ssh_needed == 'yes':
        # Get user input for SSH connection
        ssh_host = input("Enter the SSH hostname: ")
        ssh_user = input("Enter the SSH username: ")
        ssh_password = getpass.getpass("Enter the SSH password: ")

        # Create SSH tunnel
        ssh_process = create_ssh_tunnel(ssh_host, ssh_user, ssh_password)

        if not ssh_process:
            print("Failed to create SSH tunnel. Exiting.")
            return
    else:
        # If no SSH connection is needed
        print("No SSH connection will be established.")

    # Get user input for database connection
    username = input("Enter the MariaDB username: ")
    password = getpass.getpass("Enter the MariaDB password: ")
    database = input("Enter the database name: ")

    # Prompt for the database host (default to localhost if not using SSH)
    if ssh_needed == 'yes':
        db_host = input("Enter the database host (default is 127.0.0.1): ") or '127.0.0.1'
    else:
        db_host = input("Enter the database host (default is localhost): ") or 'localhost'

    # Establish database connection
    connection = get_database_connection(db_host, username, password, database)

    if connection:
        # Fetch and display schema mappings
        fetch_schema_mappings(connection)
        
        # Close the connection
        connection.close()
        print("Database connection closed.")

        # Close the SSH tunnel if it was created
        if ssh_process:
            ssh_process.terminate()  # Terminate the SSH tunnel process
            print("SSH connection closed.")

if __name__ == "__main__":
    main()
