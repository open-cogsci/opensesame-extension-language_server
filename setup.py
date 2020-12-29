#!/usr/bin/env python

import os
import glob
import yaml
from setuptools import setup


with open('opensesame_extensions/LanguageServer/info.json') as fd:
    d = yaml.load(fd)
version = d['version']
print('Version %s' % version)


def files(path):
    
    return [
        fname for fname in glob.glob(path)
        if os.path.isfile(fname) and not fname.endswith('.pyc')
    ]


def data_files():

    return [
        (
            "share/opensesame_extensions/LanguageServer",
            files("opensesame_extensions/LanguageServer/*")
        ),
        (
            "share/opensesame_extensions/LanguageServer/lsp_code_edit_widgets",
            files("opensesame_extensions/LanguageServer/lsp_code_edit_widgets/*")
        ),
    ]


setup(
    name="opensesame-extension-language_server",
    version=version,
    description="Adds language-server support to OpenSesame and Rapunzel",
    author="Sebastiaan Mathot",
    author_email="s.mathot@cogsci.nl",
    url='https://github.com/open-cogsci/opensesame-extension-language_server',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    install_requires=['pyqode3.langugage_server', 'pyyaml'],
    include_package_data=False,
    packages=[],
    data_files=data_files()
)
