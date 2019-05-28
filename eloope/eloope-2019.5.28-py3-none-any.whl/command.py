from . import service_pb2_grpc, service_pb2
from .server import run_server
import grpc


class Command:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @classmethod
    def execute(cls, cmd, *args, host='localhost', port=6991):
        return getattr(cls(host, port), cmd, Command.help)(*args)

    def _send_command(self, cmd):
        channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        stub = service_pb2_grpc.ControllerStub(channel)
        resp = stub.SendCommand(service_pb2.SendCommandRequest(command=cmd))
        return resp.info

    @staticmethod
    def help():
        return """View the list of commands (or check the correctness of the command input):
            help --- view the list of commands.
            stop --- stop sending tasks to the client.
            start --- start sending tasks to the client.
            save --- save the task to a file.
            quit --- quit the server and clients.
            task_total --- total number of tasks.
            task_count --- number of tasks on the server.
            start_time --- start time.
            connect --- connect to the server.
            run_server <load_file> <dump_path> <log_path> --- run server.
        """

    def stop(self, *args):
        return self._send_command('stop')

    def start(self, *args):
        return self._send_command('start')

    def save(self, *args):
        return self._send_command('save')

    def quit(self, *args):
        return self._send_command('quit')

    def task_total(self, *args):
        return self._send_command('task_total')

    def task_count(self, *args):
        return self._send_command('task_count')

    def start_time(self, *args):
        return self._send_command('start_time')

    def run_server(self, *args):
        if len(args) > 3:
            return Command.help()
        run_server(*args, host=self.host, port=self.port)
        return 'Quit successfully!'

    def connect(self, *args):
        while True:
            cmd = input('Command: ')
            if cmd == 'exit': break
            if not cmd: continue
            cmd, *args = cmd.strip().split()
            print('-->', getattr(self, cmd, Command.help)(*args))
