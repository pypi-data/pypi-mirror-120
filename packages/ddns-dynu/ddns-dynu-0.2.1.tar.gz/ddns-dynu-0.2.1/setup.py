import setuptools

setuptools.setup(
    name="ddns-dynu",
    version="0.2.1",
    author="agfn",
    author_email="lavender.tree9988@gmail.com",
    description="ddns for dynu.com",
    long_description='',
    long_description_content_type="text/markdown",
    install_requires = [
        "python-daemon",
        "requests"
        ],
    url="https://github.com/agfn/ddns",
    project_urls={
        "Bug Tracker": "https://github.com/agfn/ddns/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points='''
    [console_scripts]
        ddns-dynu=ddnsdynu.ddns:main
    '''
)