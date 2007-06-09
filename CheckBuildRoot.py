# vim:sw=4:et
#############################################################################
# File          : CheckBuildRoot.py
# Package       : rpmlint
# Author        : Dirk Mueller, Stephan Kulow
# Purpose       : Check for files containing $RPM_BUILD_ROOT
#############################################################################

from Filter import *
import AbstractCheck
import rpm
import re
import os
import commands
import Config
import stat

class BuildRootCheck(AbstractCheck.AbstractFilesCheck):
    def __init__(self):
        AbstractCheck.AbstractFilesCheck.__init__(self, "BuildRootCheck", ".*")
        self.build_root_re = re.compile('/var/tmp/[\w\!-\.]{1,60}-build')

    def check_file(self, pkg, filename):
        if filename.startswith('/usr/lib/debug') or Pkg.isSource():
            return
        if not stat.S_ISREG(pkg.files()[filename][0]):
            return

        if len(pkg.grep(self.build_root_re, filename)):
            printError(pkg, "file-contains-buildroot", filename)

check=BuildRootCheck()

if Config.info:
    addDetails(
'file-contains-buildroot',
"Your file contains traces of $RPM_BUILD_ROOT."
)
