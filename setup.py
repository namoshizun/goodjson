from setuptools import setup


LONG_DESCRIPTION = open('README.md').read().strip()

SHORT_DESCRIPTION = """
Functional validators to check anything about your JSON with ease.""".strip()

REQUIREMENTS = list(map(str.strip, filter(bool, open('requirements.txt').readlines())))
TEST_REQUIREMENTS = list(map(str.strip, filter(bool, open('requirements.test.txt').readlines())))


URL = 'https://github.com/namoshizun/goodjson'

setup(
    name='goodjson',
    version='0.1.0',
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,

    author='Di Lu',
    author_email='dilu3100@gmail.com',
    license='GPL',

    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        'License :: OSI Approved :: GNU General Public License (GPL)',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',

        'Operating System :: POSIX',
        'Operating System :: Unix',
    ],

    keywords='JSON Validation,Python,JSON Schema',

    packages=['goodjson'],
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    python_requires='~=3.6'
)
