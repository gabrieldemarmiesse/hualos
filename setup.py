from setuptools import setup, find_packages

setup(
    name='hualos',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'gevent',
    ],
    entry_points='''
         [console_scripts]
        hualos-serve=hualos.api:main
    '''
)
