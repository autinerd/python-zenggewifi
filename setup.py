import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zenggewifi",
    version="0.0.1",
    author="Sidney Kuyateh",
    author_email="sidneyjohn23@icloud.com",
    description="Communication to Zengge Wifi bulbs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/autinerd/python-zenggewifi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
)