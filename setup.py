from setuptools import find_packages, setup

setup(
    name="easy_ge",
    version="0.1.0",
    description="A package for simplified data validation with Great Expectations",
    author="Elsayed91",
    author_email="islam.elsayed.da@gmail.com",
    packages=find_packages(),
    install_requires=[
        "great-expectations==0.17.4",
        "pyyaml==6.0",
        "jsonschema==4.18.0",
        "jinja2==3.1.2",
        "pyarrow==12.0.1",
        "fsspec==2023.6.0",
    ],
    extras_require={
        "google": ["google-cloud-storage==2.10.0", "google-cloud-secret-manager==2.16.2"],
        "aws": ["s3fs==2023.6.0"],
    },
    tests_require=["pytest==7.4.0"],
)
