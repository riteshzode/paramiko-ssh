import paramiko

# Define connection parameters
hostname = '54.147.106.151'  # Replace with your instance's IP address or hostname
port = 22  # Default SSH port
username = 'ec2-user'  # Replace with your SSH username
private_key_path = 'my_key.pem'  # Replace with the path to your private key
command = 'sudo yum update -y && sudo yum upgrade -y && sudo yum install nginx -y'

# Using a context manager to automatically close the SSH client after the block
try:
    with paramiko.SSHClient() as client:
        # Automatically add the server's host key (this is insecure in production, better to manually add it)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Use your private key for authentication
        with open(private_key_path, 'r') as private_key_file:
            private_key = paramiko.RSAKey.from_private_key(private_key_file)

            # Connect to the remote instance using the private key
            print("Connecting to the server...")
            client.connect(hostname, port=port, username=username, pkey=private_key)
            print("Connection successful!")

        # print("Running command...")
        stdin, stdout, stderr = client.exec_command(command)

        # Check for errors in the command
        error_output = stderr.read().decode()
        if error_output:
            print(f"Error: {error_output}")
        else:
            # Print the output of the command
            output = stdout.read().decode()
            if output:
                print("Output:")
                print(output)
            else:
                print(f"No output from {command} command.")

except paramiko.AuthenticationException:
    print("Authentication failed, please check your private key and username.")
except paramiko.SSHException as e:
    print(f"SSH connection failed: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
