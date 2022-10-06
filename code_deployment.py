from prefect.filesystems import GitHub
from flows import Deployment
github_block = GitHub.load("personal-git")