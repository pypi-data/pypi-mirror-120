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
    version = '0.2',         
    description = 'mupemenet',  
    author = 'Kelwe Technologies',                  
    author_email = 'jp@kelwe-tech.com',    
    url = 'https://kelwe-tech.com',   
    packages = find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    package_data={
        'mupemenet': ['requirements.txt'],
        'mupemenet.config': ['*.json'],
        'mupemenet.resources': ['*'],
        'mupemenet.resources.models': ['*'],
        'mupemenet.resources.certificates': ['*'],
        'mupemenet.VL53L0X_rasp_python.bin': ['*.so'],
    },
)