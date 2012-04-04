from distutils.core import setup
import os


packages, data_files = [], []
for dirpath, dirnames, filenames in os.walk(os.path.join(
    os.path.dirname(__file__),
    'usersettings',
)):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[len('usersettings/'):] # Strip "usersettings/" or "usersettings\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))


setup(name='django-usersettings',
      version='0.1',
      description='An pluggable application for Django to manage usersettings across projects.',
      author='Alexander van Ratingen',
      author_email='alexander@van-ratingen.nl',
      url='http://www.bitbucket.org/Blue/django-usersettings/',
      download_url='http://www.bitbucket.org/Blue/django-usersettings/',
      package_dir={'usersettings': 'usersettings'},
      packages=packages,
      package_data={'usersettings': data_files},
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License', # TODO
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities'],
      )

