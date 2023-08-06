from setuptools import setup

def get_requirements():
    with open('requirements.txt') as fs:
        lst = fs.readlines()
    rez = []
    for x in lst:
        y = x.replace("\n", "")
        if 'tflite_runtime' not in y:
            rez.append(y)
    return rez


setup(
    name = 'mupemenet',         # How you named your package folder (MyLib)
    packages = ['mupemenet'],   # Chose the same as "name"
    version = '0.1.7',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'mupemenet',   # Give a short description about your library
    author = 'Kelwe Technologies',                   # Type in your name
    author_email = 'jp@kelwe-tech.com',      # Type in your E-Mail
    url = 'https://kelwe-tech.com',   # Provide either the link to your github or to your website
    install_requires=get_requirements(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        "console_scripts": [
            "mupemenet=App:main",
        ]
    },
    include_dirs = ['mupemenet', 'mupemenet/resources', "mupemenet/resources/models"],
    package_data={'': ['requirements.txt']},
)