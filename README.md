An **A**utonomous **LLM** **E**ngineer **C**alled **A**llmeca.

It's an experiment in getting LLMs to work on software, human help
optional.
An experiment to make GPT-4 work autonomously on software projects by giving it access to the shell, the ability to edit files, giving it a task, and putting it in a continuous loop. It turned out that GPT-4 is still not good enough to be useful for this because prompting it and fixing its mistakes takes more time than doing it yourself.

# Development Setup

```shell
asdf install
poetry install
poetry shell
```

