from setuptools import setup

def get_requirements():
    with open('mupemenet/requirements.txt') as fs:
        lst = fs.readlines()
    rez = []
    for x in lst:
        rez.append(x.replace("\n", ""))
    return rez


setup(
    name = 'mupemenet',         # How you named your package folder (MyLib)
    packages = ['mupemenet'],   # Chose the same as "name"
    version = '0.1',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'mupemenet',   # Give a short description about your library
    author = 'Kelwe Technologies',                   # Type in your name
    author_email = 'jp@kelwe-tech.com',      # Type in your E-Mail
    url = 'https://kelwe-tech.com',   # Provide either the link to your github or to your website
    install_requires=[get_requirements()],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        "console_scripts": [
            "mupemenet=App:main",
        ]
    },
    include_package_data=True,
    include_dirs = ['./resources', "./resources/models"],
)