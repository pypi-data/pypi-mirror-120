from setuptools import setup, find_packages

with open("./README.md", "r") as readme:
    description = readme.read()
setup(
    name="numwords",
    version="1.0.0",
    description="",
    long_description=description,
    long_description_content_type="text/markdown",
    author="Ankur Goswami",
    author_email="ankurgoswami1401@gmail.com",
    url="https://github.com/TheAnkurGoswami/NumWords",
    packages=["numwords"],
    install_requires=["typing"],
    python_requires=">=3.6",
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)