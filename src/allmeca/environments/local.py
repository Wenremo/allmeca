from pathlib import Path
import subprocess


from allmeca.environments.base import BaseEnvironment


class LocalEnvironment(BaseEnvironment):
    def __init__(self, work_dir):
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def run_bash(self, command):
        try:
            out = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT, timeout=10
            ).strip()
            out = out.decode("utf-8")
            if len(out) > 0:
                return out
            else:
                return "(no output)"
        except subprocess.CalledProcessError as e:
            return (
                e.output.decode("utf-8")
                + f"\n(process exited with code {e.returncode})"
            )
        except subprocess.TimeoutExpired as e:
            return e.output.decode("utf-8") + "\n(process timed out after 10 seconds)"

    def write_file(self, path, content):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
