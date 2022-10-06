from prefect.infrastructure import DockerContainer


inf = DockerContainer(
    env = {"EXTRA_PIP_PACKAGES": "s3fs pandas"}
)


if __name__ == "__main__":
    inf.save("alphavantage-image")
