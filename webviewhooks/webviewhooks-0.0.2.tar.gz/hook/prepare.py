import subprocess


def check_adb_env(adb_name):
    process = subprocess.run([adb_name, 'version'], stdout=subprocess.PIPE, shell=True)
    if process.returncode < 0:
        boo = False
    elif len(process.stdout.decode('UTF-8')) == 0:
        boo = False
    else:
        boo = True
    return boo


def check_frida_env():
    process = subprocess.run(['frida-ps', '-U'], stdout=subprocess.PIPE, shell=True)
    if process.returncode < 0:
        boo = False
    elif process.stdout.decode('UTF-8').find('PID') < 0:
        boo = False
    else:
        boo = True
    return boo


def start_check(adb_name):
    if not check_adb_env(adb_name):
        raise RuntimeError('adb env is error, please check adb path is ok')
    if not check_frida_env():
        msg = """
        frida server is error, please check frida server file was already ran in the device,
        you should push the file to the device /data/local/tmp dir first,
        change the file permission second and execute it finally.
        """
        raise RuntimeError(msg)
    return True
