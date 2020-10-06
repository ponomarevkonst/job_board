import pkg_resources
from setuptools import setup


def get_requires():
    path = 'requirements.txt'
    filepath = pkg_resources.resource_filename(__name__, path)
    with open(filepath) as file:
        packages = [name.rstrip() for name in file.readlines()]
    return packages


setup(
    name='job_board',
    version='1.0',
    packages=['jobs', 'jobs.management', 'jobs.management.commands', 'jobs.migrations', 'account', 'account.migrations',
              'job_board'],
    url='http://github.com/ponomarevkonst/job_app/',
    license='MIT',
    author='Konstantin Ponomarev',
    author_email='ponomarevkonst@gmail.com',
    description='Simple job classified web-app.',
    install_requires=get_requires()
)
