from alphavantage import get_daily_avg
from prefect.deployments import Deployment
from prefect.filesystems import GitHub


gh = GitHub.load("personal-github2")


deploy_gh = Deployment.build_from_flow(
    flow=get_daily_avg,
    name="alpha-vantage-github-flow3",
    work_queue_name = "cisco-training",
    storage= gh

)


if __name__ == "__main__":
    deploy_gh.apply()