import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GhTrack",
    version="0.0.1",
    py_modules=["GhTrack"],
    description="An Python module api app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zinaLacina/github-track",
    project_urls={
        "Bug Tracker": "https://github.com/zinaLacina/github-track/issues",
    },
    package_data={'': ['data/*']},
    test_suite="tests",
    author="Lacina ZINA",
    author_email="zinalacina@yahoo.com",
    package_dir={"": "ghtrack"},
    packages=setuptools.find_packages(where="ghtrack"),

    install_requires=[
        "requests~=2.26.0",
        "PyYAML~=5.4.1",
        "sendgrid==6.8.1",
        "colorama==0.4.4"
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
