from git import Repo, Actor
from textwrap import dedent
from allmeca.user_interaction import info, prompt_yesno

from allmeca.logger import log


class GitCommitter:
    def __init__(self, repo_path):
        self.repo = Repo(repo_path)
        self.author = Actor(name="Allmeca", email="info@allmeca.dev")

    def on_before_run_start(self):
        if self.repo.is_dirty():
            raise RuntimeError("Repo is dirty, cancelling run")

        self.branch_before = self.repo.active_branch
        self.branch = self.repo.create_head(self._find_branch_name())
        self.branch.checkout()
        log.info("created_branch", branch=self.branch.name)
        info(f"Created branch {self.branch.name} for this run.")

    def on_action_performed(self, action, output):
        self._commit_all(action, output)

    def on_run_complete(self):
        info(f"All changes have been committed to {self.branch.name}.")
        if prompt_yesno(f"Want me to switch back to {self.branch_before.name}?"):
            self.branch_before.checkout()
            log.info("switched_back_to_branch", branch=self.branch_before.name)

    def _find_branch_name(self):
        existing = set(b.name for b in self.repo.branches)
        i = 1
        while True:
            name = f"allmeca-run-{i}"
            if name not in existing:
                return name
            i += 1

    def _commit_all(self, action, output):
        # TODO: ignore huge files
        self.repo.git.add("--all")
        msg = dedent(
            """
            {summary}

            Context:
            {context}

            Output:
            {output}
            """
        ).format(summary=action.summary(), context=action.context, output=output)
        commit = self.repo.index.commit(msg, author=self.author)
        log.info("changes_committed", commit=commit.hexsha)
