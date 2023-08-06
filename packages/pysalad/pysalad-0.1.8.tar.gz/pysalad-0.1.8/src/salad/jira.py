import requests
import getpass


class Connection(object):
    def __init__(self, user, token, url):
        if user is None:
            user = input("Bitte den Benutzernamen eingeben (E-Mail): ")

        if token is None:
            token = getpass.getpass("Bitte den Token eingeben: ")

        if url is None:
            url = input("Bitte die Jira URL eingeben: ")

        self.auth = (
            user,
            token
        )

        self.url = url

        self.session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def comment(self, issue, comment):
        response = self.session.post(url=f"{self.url}/rest/api/latest/issue/{issue}/comment", auth=self.auth,
                                     json={"body": comment})
        if not response.ok:
            raise RuntimeError(f"save comment failed with status code {response.status_code}")
