from ghapi.all import GhApi
import logging


log = logging.getLogger()

ORG_NAME = "homelab-library"
PKG_TYPE = "container"


class GithubProvisioner(object):
    def __init__(self, config):
        self.config = config
        self.api = GhApi(token=config.github_token)

    @property
    def repos(self):
        if not hasattr(self, '_repos'):
            self._repos = self.api.repos.list_for_org(ORG_NAME)
        return self._repos

    def provision_repo(self, name: str):
        log.info(f"Creating repository {name}...")
        # (org, name, description, homepage, private, visibility,
        # has_issues, has_projects, has_wiki, is_template, team_id,
        # auto_init, gitignore_template, license_template, allow_squash_merge,
        # allow_merge_commit, allow_rebase_merge, delete_branch_on_merge):
        self.api.repos.create_in_org(
            ORG_NAME, name, None, None, True, None,
            True, True, True, False, None,
            False, None, None, True,
            True, True, False,
        )
