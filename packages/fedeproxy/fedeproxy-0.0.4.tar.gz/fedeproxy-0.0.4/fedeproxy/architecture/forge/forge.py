import abc
import os

from furl import furl

from ...format import format
from ...interfaces import forge
from ..dvcs import git


class Persistent(forge.Persistent):
    @abc.abstractmethod
    def create_from_json(self, j):
        ...

    @abc.abstractmethod
    def list(self):
        ...


class Forge(forge.Forge):
    def save(self, pathname):
        return self.users.save(f"{pathname}/users.json")

    def load(self, pathname):
        return self.users.load(f"{pathname}/users.json")

    def hook_register(self, url):
        r = []
        for p in self.projects.list():
            r.append(p.hook_register(f"{url}/hook/project/{p.namespace}/{p.project}"))
        return r

    def _hook_receive_system(payload):
        pass

    def hook_receive(self, payload, **kwargs):
        if len(kwargs) > 0:
            self.projects.get(kwargs["namespace"], kwargs["project"]).hook_receive(payload)
        else:
            self._hook_receive_system(payload)


class Projects(forge.Projects):
    pass


class Project(forge.Project):
    def save(self, pathname):
        p = f"{pathname}/{self.namespace}/{self.project}"
        if not os.path.exists(p):
            os.makedirs(p)
        return self.issues.save(f"{p}/issues.json")

    def load(self, pathname):
        p = f"{pathname}/{self.namespace}/{self.project}"
        return self.issues.load(f"{p}/issues.json")

    def dvcs_factory(self):
        return git.Git

    def dvcs(self, directory):
        o = furl(self.http_url_to_repo)
        o.username = "oauth2"
        o.password = self.forge.get_token()
        return self.dvcs_factory()(directory, o.tostr())


class Milestones(forge.Milestones, Persistent):
    @property
    def format(self):
        ...

    def load(self, filename):
        ...

    def save(self, filename):
        ...

    def create_from_json(self, j):
        ...


class Milestone(forge.Milestone):
    pass


class Issues(forge.Issues, Persistent):
    def load(self, filename):
        return format.FormatIssues().load(filename, self.create_from_json)

    def save(self, filename):
        return format.FormatIssues().save(filename, self.list())

    def create_from_json(self, j):
        i = self.get(j["id"])
        if i is None:
            i = self.create(j["title"])
        i.from_json(j)
        return i


class Issue(forge.Issue):
    pass


class Users(forge.Users, Persistent):
    def load(self, filename):
        return format.FormatUsers().load(filename, self.create_from_json)

    def save(self, filename):
        return format.FormatUsers().save(filename, self.list())

    def create_from_json(self, j):
        i = self.get(j["username"])
        if i is None:
            i = self.create(j["username"], "no password", "foo@example.com")
        i.from_json(j)
        return i

    def convert_url_to_username(self, url):
        return os.path.basename(url)


class User(forge.User):
    pass
