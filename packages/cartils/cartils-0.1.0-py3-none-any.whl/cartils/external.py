import os
import subprocess

def cmd(cmd, redirect_stdout=False, redirect_stderr=False):
    # create a subprocess to run the command
    if redirect_stdout and redirect_stderr:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        output = output.decode()
        error = error.decode()
        # grab and return the exit code
        rc = p.poll()
        return rc, output, error
    if redirect_stdout:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        # wait for it to finish and grab the output
        output = p.communicate()[0].decode()
        # grab and return the exit code
        rc = p.poll()
        return rc, output
    if redirect_stderr:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        # wait for it to finish and grab the output
        error = p.communicate()[1].decode()
        # grab and return the exit code
        rc = p.poll()
        return rc, error
    p = subprocess.Popen(cmd, shell=True)
    # wait for it to finish
    p.wait()
    # grab and return the exit code
    rc = p.poll()
    return rc

def check_program(program):
    if os.name == 'nt':
        if cmd(f'where {program}', redirect_stdout=True)[0] == 0:
            return True
    else:
        if cmd(f'command -v {program}', redirect_stdout=True)[0] == 0:
            return True
    return False

if __name__ == '__main__':
    print(check_program('python'))
    print(cmd('docker info', redirect_stdout=True))
    print(cmd('docker info', redirect_stdout=True, redirect_stderr=True))