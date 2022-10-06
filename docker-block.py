

from alphavantage import get_daily_avg
from prefect.infrastructure import DockerContainer
from prefect.deployments import Deployment


infra = DockerContainer.load()