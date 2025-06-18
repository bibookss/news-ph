from setuptools import find_packages, setup

setup(
    name="news_ph",
    packages=find_packages(exclude=["news_ph_tests"]),
    install_requires=["dagster", "dagster-cloud"],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
