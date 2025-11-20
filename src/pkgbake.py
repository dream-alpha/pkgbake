#!/usr/bin/python
# coding=utf-8
# Copyright (C) 2018-2025 by dream-alpha
# License: GNU General Public License v3.0 (see LICENSE file for details)


import os
import sys
import getopt
from Version import VERSION
from FileUtils import readFile, deleteDirectory, createDirectory, copyFiles


LIBDIR = "/usr/lib"


def process_maks(gitdir, pkg_root):
    # print("=====> process_maks: %s > %s" % (gitdir, pkg_root))
    installdir = install_PYTHON = install_DATA = domain = ""
    langs = []
    lines = readFile(os.path.join(gitdir, "Makefile.am")).splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("SUBDIRS = "):
            subdirs = line.split(" ")[2:]
            # print(gitdir + " >>> SUBDIRS = %s" % subdirs)
            for subdir in subdirs:
                # print("subdir: %s" % subdir)
                process_maks(os.path.join(gitdir, subdir), pkg_root)
        elif line.startswith("installdir = "):
            installdir = line.split(" ")[2].replace("$(libdir)", LIBDIR)
            # print(gitdir + " >>> installdir = %s" % installdir)
        elif line.startswith("DOMAIN = "):
            domain = line.split(" ")[2]
            # print(gitdir + " >>> domain = %s" % domain)
        elif line.startswith("LANGS := "):
            langs = line.split(" ")[2:]
            # print(gitdir + " >>> LANGS = %s" + langs)
        elif line.startswith("install_PYTHON"):
            install_PYTHON = line.split(" ")[2:]
            # print(gitdir + " >>> install_PYTHON = %s" % install_PYTHON)
        elif line.startswith("install_DATA"):
            install_DATA = line.split(" ")[2:]
            # print(gitdir + " >>> install_DATA = %s" %s install_DATA)

    if installdir:
        if domain:
            installdir = installdir.replace("$(DOMAIN)", domain)
            if langs:
                for lang in langs:
                    destdir = os.path.join(
                        pkg_root + installdir, "locale", lang, "LC_MESSAGES")
                    createDirectory(destdir)
                    copyFiles(os.path.join(os.path.dirname(
                        gitdir), "src/locale", lang, "LC_MESSAGES", "*.mo"), destdir)
        if install_PYTHON:
            createDirectory(pkg_root + installdir)
            for afile in install_PYTHON:
                copyFiles(os.path.join(gitdir, afile), pkg_root + installdir)
        if install_DATA:
            createDirectory(pkg_root + installdir)
            for afile in install_DATA:
                copyFiles(os.path.join(gitdir, afile), pkg_root + installdir)

    # print("<===== process_maks: %s" % gitdir)


def pkgbake(argv):
    print(f"pkgbake version {VERSION}")
    gitdir = pkgdir = ""

    try:
        opts, _args = getopt.getopt(argv, "hi:o:", [])
    except getopt.GetoptError as e:
        print("Error: " + str(e))
        print('Usage: python pkgbake.py -i <gitdir> -o <pkgroot>')
        sys.exit(2)

    if len(opts) < 2:
        print('Usage: python pkgbake.py -i <gitdir> -o <pkgroot>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-i":
            gitdir = os.path.normpath(arg)
        elif opt == "-o":
            pkgdir = os.path.normpath(arg)

    print(f"git dir: {gitdir}")
    print(f"pkg dir: {pkgdir}")
    pkg_root = os.path.join(pkgdir, "pkgroot")
    print(f"pkg root: {pkg_root}")

    if not os.path.isfile(os.path.join(gitdir, "CONTROL/control")):
        print(f"{os.path.join(gitdir, 'CONTROL/control')} file does not exist, exiting...")
        sys.exit(2)

    deleteDirectory(pkg_root)
    createDirectory(os.path.join(pkg_root, "CONTROL"))
    copyFiles(os.path.join(gitdir, "CONTROL", "*"),
              os.path.join(pkg_root, "CONTROL"))
    os.system(f"echo \"2.0\" > {os.path.join(pkg_root, 'CONTROL/debian-binary')}")

    print("processing MAKs...")
    process_maks(gitdir, pkg_root)
    return pkg_root


if __name__ == "__main__":
    pkgroot = pkgbake(sys.argv[1:])
    if pkgroot:
        print(f"pkgroot: {pkgroot}")
        sys.exit(0)
    else:
        sys.exit(1)
