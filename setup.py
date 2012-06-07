from distutils.core import setup


setup(
    name='django-usersettings',
    version='0.1',
    description='A pluggable application for Django to manage usersettings across apps.',
    author='Alexander van Ratingen',
    author_email='alexander@van-ratingen.nl',
    url='http://www.bitbucket.org/Blue/django-usersettings/',
    download_url='http://www.bitbucket.org/Blue/django-usersettings/',
    packages=[
        'usersettings',
        'usersettings.tests',
    ],
    package_data={'usersettings': [
        'templates/usersettings/*.html',
        'static/*',
        'locale/*/LC_MESSAGES/*',
    ]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
