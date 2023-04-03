from allmeca.actions.base import Action, InputDecl


class RunBash(Action):
    command = "run_bash"
    description = "Run a bash command"
    input_declarations = [
        InputDecl(name="command", description="The command to run"),
    ]

    def perform(self, environment):
        head = f"$ {self.inputs.command}\n"
        cmd_out = environment.run_bash(self.inputs.command)
        if len(cmd_out) > 15000:
            cmd_out = cmd_out[:15000] + "\n\n(output truncated)"
        return head + cmd_out
