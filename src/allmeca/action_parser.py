import re

from allmeca.logger import log


class ActionParser:
    RE_FLAGS = re.MULTILINE | re.VERBOSE | re.DOTALL
    RE_ACTION_START = re.compile(
        r"^ \s* ACTION: \s* (?P<action_name>\w+) \s* $", RE_FLAGS
    )
    RE_ACTION_END = re.compile(r"^ ENDACTION \s* $", RE_FLAGS)
    RE_INPUT = re.compile(
        r"^ \s* (?P<input_name>\w+) \s* = \s* \{\{ (?P<value>.*?) }}", RE_FLAGS
    )

    def __init__(self, available_actions):
        self.available_actions = available_actions
        log.debug(
            "init_action_parser", available_actions=list(available_actions.keys())
        )

    def extract_actions(self, msg):
        start_pos = 0
        actions = []

        while True:
            result = self.extract_action(msg, start_pos)
            if result is None:
                break
            action, start_pos = result
            actions.append(action)

        if len(actions) > 0:
            # Any remaining text is added to the last action's context
            actions[-1].context += msg[start_pos:]

        return actions

    def extract_action(self, msg, start_pos):
        log.debug("extract_action", start_pos=start_pos, msg=msg[start_pos:])
        start = self.RE_ACTION_START.search(msg, pos=start_pos)
        if start is None:
            log.debug("no_action_found", start_pos=start_pos)
            return

        action_name = start.group("action_name")
        end = self.RE_ACTION_END.search(msg, pos=start.end())
        errors = []
        inputs = dict()
        log.debug("action_found", action_name=action_name)
        if end is None:
            errors.append(f"ENDACTION missing")
            end_pos = start.end()
            log.debug("no_endaction_found", start_pos=start_pos)
        else:
            end_pos = end.end()
            log.debug("endaction_found", end_pos=end_pos)

            inputs_str = msg[start.end() : end.start()]
            for match in self.RE_INPUT.finditer(inputs_str):
                input_name, value = match.group("input_name"), match.group("value")
                inputs[input_name] = value
                log.debug("input_found", input_name=input_name, value=value)

        context = msg[start_pos:end_pos]
        action = self.available_actions[action_name](context, inputs, errors=errors)
        log.debug("action_created", action=action.summary(), errors=action.errors)
        return action, end_pos


if __name__ == "__main__":
    from inspect import cleandoc
    from allmeca import actions

    msg = cleandoc(
        """
        ALLMECA THOUGHTS: I need to write a Python script that can get URLs from DuckDuckGo search results.
        REASONING: I'll need to automate web interactions with Python, so I should use a popular library such as requests or selenium. I can then write code to parse the HTML of the DuckDuckGo search results and extract the URLs.
        CRITICISM:
        ACTION: create_file
          path={{search.py}}
          contents={{import requests
        from bs4 import BeautifulSoup

        search_term = 'whats new'
        url = f"https://duckduckgo.com/html/?q={search_term}"
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}
        s = requests.Session()
        s.headers.update(headers)

        soup = BeautifulSoup(s.get(url).text, 'html.parser')

        results = soup.select('a.result__url')

        for a in results:
            print(a['href'])}}
        ENDACTION

        ALLMECA THOUGHTS: Blablabla
        REASONING: Blublublu
        CRITICISM:
        ACTION: run_bash
          command={{ls -al}}
        ENDACTION

        NOTES: Install the necessary libraries before running this code.
        """
    )

    actions = ActionParser(actions.all).extract_actions(msg)
    for action in actions:
        print(repr(action))
        print()
        print(str(action))
        print()
        print("Context:")
        print(action.context)
        print()
        print()
