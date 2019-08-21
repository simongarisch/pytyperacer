from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Simon Garisch",
    author_email="gatman946@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    description="Python racing bot for https://play.typeracer.com/",
    install_requires=["selenium>=3.141.0", "beautifulsoup4>=4.8.0"],
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="pytyperacer",
    name="pytyperacer",
    packages=find_packages(include=["pytyperacer"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/simongarisch/pytyperacer",
    version="0.1.0",
    zip_safe=False,
)
