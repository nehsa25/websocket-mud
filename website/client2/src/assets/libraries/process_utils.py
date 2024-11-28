import psutil
import traceback

# from script utils
from subprocess_utils import SubprocessUtils
from log_utils import LogUtils
from helper_utils import HelperUtils

class ProcessUtils:

    @staticmethod
    def get_process_info(process_name, logger=None):
        process_info = None

        for proc in psutil.process_iter():
            tmpobj = proc.as_dict(attrs=['pid', 'name', 'username'])
            if tmpobj['name'] == process_name:
                process_info = tmpobj
                break

        if process_info == None:
            LogUtils.info("The process {} is not running!".format(process_name))

        return process_info

    @staticmethod
    def get_process_cpu_memory_handles(exe_name, logger=None):
        memory = None
        handles = None
        proc_cpu = None
        proc_info = ProcessUtils.get_process_info(exe_name, logger)
        if proc_info != None:
            # get process cpu usage
            proc_cpu = str(ProcessUtils.get_process_cpu_usage(ProcessUtils.get_process_info(exe_name, logger)['pid']))

            # memory stuff
            memory = ProcessUtils.get_process_virtual_memory(proc_info['pid'])
            handles = ProcessUtils.get_process_handles(proc_info['pid'])
            LogUtils.debug(f"{proc_info['name']} - cpu: {proc_cpu},  virtual memory: {memory.vms}, working set: {memory.rss}, handle used: {handles}", logger)
        return (proc_cpu, memory, handles)

    @staticmethod
    def get_process_virtual_memory(process_pid):
        process = psutil.Process(process_pid)
        return process.memory_info()

    @staticmethod
    def get_process_handles(process_pid):
        process = psutil.Process(process_pid)
        return process.num_handles()

    @staticmethod
    def get_process_cpu_usage(process_pid):
        process = psutil.Process(process_pid)
        return process.cpu_percent()

    @staticmethod
    def list_services(logger=None):
        running_services = SubprocessUtils.run_command("net start", logger).stdout.split('\n')
        clean_list = []
        for service in running_services:
            service = service.strip(' ') 
            if service != 'These Windows services are started:' and service != '':
                clean_list.append(service)

        return clean_list

    @staticmethod
    def stop_service(service_name, logger=None):
        LogUtils.info("Stopping service " + service_name, logger)
        out = SubprocessUtils.run_command("net stop {} /yes".format(service_name), logger)
        HelperUtils.sleep_for(3)
        return out

    @staticmethod
    def start_service(service_name, logger=None):
        LogUtils.info("Starting service " + service_name, logger)            
        out = SubprocessUtils.run_command("net start {} /yes".format(service_name), logger)
        HelperUtils.sleep_for(3)
        return out

    @staticmethod
    def restart_service(service, logger=None):
         ProcessUtils.stop_service(service, logger)
         ProcessUtils.start_service(service, logger)

    @staticmethod
    def kill_process_by_name(name, logger=None):
        num_killed = 0
        for proc in psutil.process_iter():
            if name.lower() in proc.name().lower():                
                proc.kill()
                num_killed += 1
        LogUtils.debug(f"Killed {num_killed} \"{name}\" processes", logger)
        return num_killed
        