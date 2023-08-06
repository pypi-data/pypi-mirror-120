from setuptools import setup, find_packages


def get_readme(name="README.md"):
    with open(name) as f:
        return f.read()


requirements = ["redis", "qtpy", "PyQt5", "msgpack", "msgpack-numpy"]


setup(
    name="qredis",
    version="1.0.1",
    description="Qt based Redis GUI",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    author="Tiago Coutinho",
    author_email="coutinhotiago@gmail.com",
    url="https://github.com/tiagocoutinho/qredis",
    packages=find_packages(),
    package_data={"qredis.images": ["*.png"], "qredis.ui": ["*.ui"]},
    entry_points={"console_scripts": ["qredis=qredis.window:main"]},
    install_requires=requirements,
    keywords="redis,GUI,Qt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.5",
)
