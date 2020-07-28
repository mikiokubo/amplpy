#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import shutil
import tempfile

VERSION = 'nightly'
API_URL = 'http://ampl.com/dl/API/future/{}/libampl.zip'.format(VERSION)

def updatelib(archs):
    from zipfile import ZipFile
    try:
        from urllib import urlretrieve
    except Exception:
        from urllib.request import urlretrieve

    os.chdir(os.path.dirname(__file__) or os.curdir)

    tmpfile = tempfile.mktemp('.zip')
    tmpdir = os.path.join(os.curdir, 'tmp', 'libampl')
    try:
        shutil.rmtree(tmpdir)
    except Exception:
        pass

    print("Downloading:", API_URL)
    urlretrieve(API_URL, tmpfile)
    with ZipFile(tmpfile) as zp:
        zp.extractall(tmpdir)
    try:
        os.remove(tmpfile)
    except Exception:
        pass

    include_dir = os.path.join(tmpdir, 'include', 'ampl')
    wrapper_dir = os.path.join(tmpdir, 'python')

    amplpy_include = os.path.join('amplpy', 'amplpython', 'cppinterface', 'include', 'ampl')
    try:
        shutil.rmtree(amplpy_include)
    except Exception:
        pass
    shutil.copytree(include_dir, amplpy_include)
    print(
        '*\n!.gitignore\n',
        file=open(os.path.join(amplpy_include, '.gitignore'), 'w')
    )

    print('wrapper:')
    for filename in os.listdir(wrapper_dir):
        print('\t{}'.format(filename))
        shutil.copyfile(
            os.path.join(wrapper_dir, filename),
            os.path.join('amplpy', 'amplpython', 'cppinterface', filename)
        )

    dstbase = os.path.join('amplpy', 'amplpython', 'cppinterface', 'lib')
    try:
        shutil.rmtree(dstbase)
        os.mkdir(dstbase)
    except Exception:
        pass
    print(
        '*\n!.gitignore\n',
        file=open(os.path.join(dstbase, '.gitignore'), 'w')
    )

    for libname in archs:
        srcdir = os.path.join(tmpdir, libname)
        dstdir = os.path.join(dstbase, libname)
        os.mkdir(dstdir)
        print('{}:'.format(libname))
        for filename in os.listdir(srcdir):
            if filename.endswith('.jar'):
                continue
            if 'java' in filename:
                continue
            if 'csharp' in filename:
                continue
            print('\t{}'.format(filename))
            shutil.copyfile(
                os.path.join(srcdir, filename),
                os.path.join(dstdir, filename)
            )


if __name__ == '__main__':
    if len(sys.argv) > 1:
        updatelib(sys.argv[1:])
    else:
        updatelib(['intel32', 'amd64', 'ppc64le'])
