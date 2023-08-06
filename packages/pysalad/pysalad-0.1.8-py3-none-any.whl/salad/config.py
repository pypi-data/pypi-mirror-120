import base64
import os
from configparser import ConfigParser


def encrypt(value: str) -> str:
    base64_bytes = base64.b64encode(value.encode('ascii'))
    return base64_bytes.decode('ascii')


def decrypt(value: str) -> str:
    base64_bytes = value.encode('ascii')
    return base64.b64decode(base64_bytes).decode('ascii')


def load(args, file_name: str) -> ConfigParser:
    config = ConfigParser()

    if os.path.isfile(file_name):
        with open(file_name, "r") as config_file:
            config.read_file(config_file)

        if args.user is None and \
                config.has_option(config.default_section, "user"):
            args.user = config.get(config.default_section, "user")

        if args.password is None and \
                config.has_option(config.default_section, "password"):
            args.password = decrypt(config.get(config.default_section, "password"))

        if args.url is None and \
                config.has_option(config.default_section, "url"):
            args.url = config.get(config.default_section, "url")

        if args.jira_user is None and \
                config.has_option(config.default_section, "jira_user"):
            args.jira_user = config.get(config.default_section, "jira_user")

        if args.jira_token is None and \
                config.has_option(config.default_section, "jira_token"):
            args.jira_token = decrypt(config.get(config.default_section, "jira_token"))

        if args.jira_url is None and \
                config.has_option(config.default_section, "jira_url"):
            args.jira_url = config.get(config.default_section, "jira_url")

        if args.default_order is None and \
                config.has_option(config.default_section, "default_order"):
            args.default_order = config.get(config.default_section,
                                            "default_order")

    return config


def save(args, config: ConfigParser, file_name: str):
    if args.user is not None:
        config.set(config.default_section, "user",
                   args.user)

    if args.password is not None:
        config.set(config.default_section, "password", encrypt(args.password))
        print(f"CAUTION: password saved in config file")

    if args.url is not None:
        config.set(config.default_section, "url",
                   args.url)

    if args.jira_user is not None:
        config.set(config.default_section, "jira_user",
                   args.jira_user)

    if args.jira_token is not None:
        config.set(config.default_section, "jira_token", encrypt(args.jira_token))
        print(f"CAUTION: Jira Token saved in config file")

    if args.jira_url is not None:
        config.set(config.default_section, "jira_url",
                   args.jira_url)

    if args.default_order is not None:
        config.set(config.default_section, "default_order",
                   args.default_order)

    if args.template_name is not None:
        if not config.has_section(args.template_name):
            config.add_section(args.template_name)
        if args.template_order is not None:
            config.set(args.template_name, "order",
                       args.template_order)
        if args.template_comment is not None:
            config.set(args.template_name, "comment",
                       args.template_comment)
        if args.template_duration is not None:
            config.set(args.template_name, "duration",
                       str(args.template_duration))
        if args.template_jira_issue is not None:
            config.set(args.template_name, "jira_issue",
                       str(args.template_jira_issue))
        if args.template_jira_comment is not None:
            config.set(args.template_name, "jira_comment",
                       str(args.template_jira_comment))

    with open(file_name, "w") as config_file:
        config.write(config_file)


def reset(file_name: str):
    os.remove(file_name)


def show(config: ConfigParser, section: str):
    if not config.has_section(section) and section != config.default_section:
        raise RuntimeError(f"unknown section {section}")

    for key in config[section]:
        print(f"{key: <15} = {config.get(section, key): <30}")
