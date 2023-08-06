from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='auto-click',
    version='0.0.11',
    author='Jung Ji-Hyo',
    author_email='cord0318@gmail.com',
    description='Python Auto-Click Library.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["click", "pynput"],
    keywords=["korea", "autoclick", "auto", "jihyo", "click", "auto-click"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "auto = autoclick.command:main"
        ]
    },
    python_requires=">=3",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)