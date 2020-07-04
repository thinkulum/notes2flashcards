
from setuptools import setup, find_packages
from notes2flashcards.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='notes2flashcards',
    version=VERSION,
    description='A Python tool to convert various note formats to various flashcard formats',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Andy Culbertson',
    author_email='thinkulum@gmail.com',
    url='https://github.com/thinkulum/notes2flashcards',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'notes2flashcards': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        notes2flashcards = notes2flashcards.main:main
    """,
)
