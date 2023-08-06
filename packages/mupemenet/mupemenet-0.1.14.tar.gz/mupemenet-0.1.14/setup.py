from setuptools import find_packages, setup

def get_requirements():
    with open('mupemenet/requirements.txt') as fs:
        lst = fs.readlines()
    rez = []
    for x in lst:
        y = x.replace("\n", "")
        if 'tflite_runtime' not in y:
            rez.append(y)
    return rez


setup(
    name = 'mupemenet',           
    version = '0.1.14',         
    description = 'mupemenet',  
    author = 'Kelwe Technologies',                  
    author_email = 'jp@kelwe-tech.com',    
    url = 'https://kelwe-tech.com',   
    packages = find_packages(include=['mupemenet', 'mupemenet.*']),
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    include_dirs = ['mupemenet'],
    package_data={'': ['requirements.txt']},
)