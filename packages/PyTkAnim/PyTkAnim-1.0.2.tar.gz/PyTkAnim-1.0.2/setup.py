from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README



setup(
    name="PyTkAnim",
    version="1.0.2",
    description="PyTkAnim is extension for tkinter that provides animator and simple usage.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/carlFandino",
    project_urls={"Source":"https://github.com/carlFandino/pytkanim-1.0.2"},
    author="Carl Gian D Fandiño",
    author_email="giancarl.fandino@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: User Interfaces",
        "Natural Language :: English"
    ],
    packages=["pytkanim","pytkanim/CustomAnimations","pytkanim/Animations","pytkanim/__easingfunctionsX__","pytkanim/__easingfunctionsY__"],

    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
           
        ]
    },
)
