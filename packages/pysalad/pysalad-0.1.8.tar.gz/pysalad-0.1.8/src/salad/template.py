import string
import click
from click import STRING


class CommentFormatter(string.Formatter):
    def __init__(self):
        self.values = dict()

    def format_template(self, format_string) -> str:
        if format_string is None:
            return ""
        else:
            return self.format(format_string)

    def set(self, key: str, value):
        if value is not None:
            self.values[key] = str(value)

    def get_value(self, key, args, kwargs):
        return key

    def format_field(self, value, default_value):
        if value in self.values:
            return self.values[value]

        if default_value is None or not default_value:
            new_value = click.prompt(f"{value}", type=STRING)
        else:
            new_value = click.prompt(f"{value}", type=STRING, default=default_value)

        if new_value is not None:
            self.set(value, new_value)

        return new_value
