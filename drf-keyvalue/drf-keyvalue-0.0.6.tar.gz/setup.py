import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

DEPENDENCIES = [
    "redis",
    "requests",
    "Django>=2.0",
    "django-filter==2.1.0",
    "djangorestframework==3.9.3",
    "psycopg2==2.8.2",
]

setuptools.setup(
    name="drf-keyvalue",
    version="0.0.6",
    author="Christo Crampton",
    author_email="christo@appointmentguru.co",
    description="Store and retrieve data in a consistent way in a key-value store using Django Rest Framework serializers",
    long_description="Please see README for details.",
    # long_description_content_type="text/markdown",
    install_requires=DEPENDENCIES,
    url="https://gitlab.com/SchoolOrchestration/libs/drf-keyvalue",
    packages=["drf_keyvalue"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
