import subprocess


def check_adb_env(adb_name):
    process = subprocess.run([adb_name, 'version'], stdout=subprocess.PIPE, shell=True)
    if process.returncode != 0:
        raise RuntimeError('adb env is error, please check adb path is ok')
    elif len(process.stdout.decode('UTF-8')) == 0:
        raise RuntimeError('adb env is error, please check adb path is ok')
    else:
        msg = """
             frida server is error, please check frida server file was already ran in the device,
                            you should push the file to the device /data/local/tmp dir first,
                            change the file permission second and execute it finally.
             """
        process = subprocess.run(['frida-ps', '-U'], stdout=subprocess.PIPE, shell=True)
        if process.returncode != 0:
            raise RuntimeError(msg)
        elif process.stdout.decode('UTF-8').find('PID') < 0:
            raise RuntimeError(msg)
        else:
            return True


def start_check(adb_name):
    return check_adb_env(adb_name)
