import paramiko


def sftp_upload(outputfile):
    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname="rqi1stop-sftp-preprod.rqi1stop.com", port=6239, username="116286",
                    password="bEtR0X6@O$", )

        sftp = ssh.open_sftp()
        sftp.chdir('uploads/116286')
        sftp.put('C:/Users/Ryan/OneDrive/Documents/GitHub/CSC-131-pIT-Crew-project/' + outputfile, 'output.csv')

        ssh.close()
