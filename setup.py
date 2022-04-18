import os

from setuptools import find_packages, setup


def read(file_name):
    """Read the provided file."""
    this_dir = os.path.dirname(__file__)
    file_path = os.path.join(this_dir, file_name)
    with open(file_path) as f:
        return f.read()


def version_scheme(version):
    """
    Version scheme hack for setuptools_scm.
    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342
    If that issue is resolved, this method can be removed.
    """
    import time

    from setuptools_scm.version import guess_next_version

    if version.exact:
        return version.format_with("{tag}")
    else:
        _super_value = version.format_next_version(guess_next_version)
        now = int(time.time())
        return _super_value + str(now)


def local_version(version):
    """
    Local version scheme hack for setuptools_scm.
    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342
    If that issue is resolved, this method can be removed.
    """
    return ""


setup(
    name="court-scraper",
    description="Command-line tool for scraping data from U.S. county courts",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Big Local News",
    author_email="biglocalnews@stanford.edu",
    url="https://github.com/biglocalnews/court-scraper",
    packages=find_packages(),
    package_data={"court_scraper": ["data/*.csv"]},
    entry_points="""
        [console_scripts]
        court-scraper=court_scraper.cli:cli
    """,
    install_requires=[
        "anticaptchaofficial",
        "bs4",
        "click",
        "click-option-group",
        "cssselect",
        "lxml",
        "my-fake-useragent",
        "pyyaml",
        "retrying",
        "selenium",
        "sqlalchemy",
        "typing-extensions",
    ],
    license="ISC license",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    test_suite="tests",
    tests_require=["flake8", "pytest", "pytest-vcr"],
    project_urls={
        "Maintainer": "https://github.com/biglocalnews",
        "Source": "https://github.com/biglocalnews/court-scraper",
        "Tracker": "https://github.com/biglocalnews/court-scraper/issues",
    },
    setup_requires=["setuptools_scm"],
    use_scm_version={"version_scheme": version_scheme, "local_scheme": local_version},
)
