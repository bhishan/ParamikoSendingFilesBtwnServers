import paramiko 
import os
import glob 
import datetime

def main(host, username, password):
    cur_date_time = datetime.datetime.now()
    cur_date_time = str(cur_date_time)
    cur_date = (cur_date_time.split(' '))[0]
    remote_path = '/root/bhishantest/'
    files = glob.glob("*.*")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    apath = '/root/bhishantest'
    apattern = '"*.*"'
    rawcommand = 'find {path} -name {pattern}'
    command = rawcommand.format(path=apath, pattern=apattern)
    stdin, stdout, stderr = ssh.exec_command(command)
    filelist = stdout.read().splitlines()
    filelist = [(afile.split(apath+'/'))[-1] for afile in filelist]
    print filelist
    for afile in filelist:
        print afile

    ftp = ssh.open_sftp()
    for each_file in files:
        if cur_date + each_file not in filelist:
            local_path = os.getcwd() + '/' + each_file
            final_remote_path = remote_path + cur_date + each_file
            print local_path 
            print final_remote_path
            ftp.put(local_path, final_remote_path)
        else:
            local_path = os.getcwd() + '/' + each_file
            final_remote_path = remote_path + cur_date + "1" + each_file
            ftp.put(local_path, final_remote_path)
    ftp.close()
    ssh.close()

if __name__ == '__main__':
    main('ip', 'username', 'password')
