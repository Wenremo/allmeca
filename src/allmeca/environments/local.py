from pathlib import Path
import subprocess


from allmeca.environments.base import BaseEnvironment


class LocalEnvironment(BaseEnvironment):
    def __init__(self, work_dir):
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def run_bash(self, command):
        output = f"$ {command}\n"

        try:
            cmd_out = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT, timeout=10
            ).strip()
            if len(cmd_out) > 0:
                output += cmd_out.decode("utf-8")
            else:
                output += "(no output)"
        except subprocess.CalledProcessError as e:
            output += e.output.decode("utf-8")
            output += f"(process exited with code {e.returncode})"
        except subprocess.TimeoutExpired as e:
            output += e.output.decode("utf-8")
            output += "(process timed out after 10 seconds)"

        return output

    def write_file(self, path, content):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
