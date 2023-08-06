#!/usr/bin/env python

#############################################################################
##
# This file is part of Taurus
##
# http://taurus-scada.org
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""
Release data for the taurus project. It contains the following members:

    - version : (str) version string
    - description : (str) brief description
    - long_description : (str) a long description
    - license : (str) license
    - authors : (dict<str, tuple<str,str>>) the list of authors
    - url : (str) the project url
    - download_url : (str) the project download url
    - platforms : list<str> list of supported platforms
    - keywords : list<str> list of keywords

The version string follows PEP440 (https://www.python.org/dev/peps/pep-0440)
Normally the release segment consists of 3 dot-separated numbers with the
same meanings as the "major", "minor" and "patch" components in
Semantic Versioning (http://semver.org/).

Exceptionally, we may use additional numbers in the release segment to
preserve a reasonable version sorting in the case of parallel releases (see
e.g. https://gitlab.com/taurus-org/taurus/-/issues/1192)
"""

# -*- coding: utf-8 -*-
__docformat__ = "restructuredtext"


# Name of the package for release purposes.  This is the name which labels
# the tarballs and RPMs made by distutils, so it's best to lowercase it.
name = 'taurus'

# The version string is normally bumped using bumpversion script
# (https://github.com/peritus/bumpversion), except when adding/removing
# extra numbers in the release segment (e.g. for hotfixes), which is done
# manually.
version = '4.8.1'

# generate version_info and revision (**deprecated** since version 4.0.2-dev).
if '-' in version:
    (_v, _rel), _r = version.split('-'), '0'
elif '.dev' in version:
    (_v, _r), _rel = version.split('.dev'), 'dev'
else:
    _v, _rel, _r = version, '', '0'
_v = tuple([int(n) for n in _v.split('.')])
version_info = _v + (_rel, int(_r))   # deprecated, do not use
revision = _r  # deprecated, do not use


description = "A framework for scientific/industrial CLIs and GUIs"

long_description = """Taurus is a python framework for control and data
acquisition CLIs and GUIs in scientific/industrial environments.
It supports multiple control systems or data sources: Tango, EPICS,...
New control system libraries can be integrated through plugins."""

license = 'LGPL'

authors = {'Tiago_et_al': ('Tiago Coutinho et al.', ''),
           'Community': ('Taurus Community',
                         'tauruslib-devel@lists.sourceforge.net'),
           }


url = 'http://www.taurus-scada.org'

download_url = 'http://pypi.python.org/packages/source/t/taurus'

platforms = ['Linux', 'Windows']

keywords = ['CLI', 'GUI', 'PyTango', 'Tango', 'Shell', 'Epics']
