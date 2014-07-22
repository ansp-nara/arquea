# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import codecs

version = '2.0.1.dev0'

"""
zest.releaser available commands

prerelease: asks you for a version number (defaults to the current version minus a 'dev' or so) with this new version number and offers to commit those changes to subversion

release: copies the the trunk or branch of the current checkout and creates a version control tag of it. Makes a checkout of the tag in a temporary directory. Offers to register and upload a source dist of this package to PyPI (Python Package Index).

postrelease: asks you for a version number (gives a sane default), adds a development marker to it, updates the setup.py or version.txt and the CHANGES/HISTORY/CHANGELOG file with this and offers to commit those changes to version control.

fullrelease: all of the above in order.

"""

def read(filename):
    return unicode(codecs.open(filename, encoding='utf-8').read())

long_description = '\n\n'.join([read('README.rst'),])
                                
setup(
        name = 'sistema',
        version = version,
        description = "Sistema administrativo do ANSP",
        long_description = long_description,
        keywords = '',
        author = 'NARA',
        author_email = 'noc@ansp.br',
        url = 'http://www.ansp.br',
        license = '',
        packages = find_packages(exclude=['ez_setup']),
        #namespace_packages = [''],
        include_package_data = True,
        zip_safe = False,
        install_requires = [
          'setuptools',
          # -*- Extra requirements: -*-
        ]
     )