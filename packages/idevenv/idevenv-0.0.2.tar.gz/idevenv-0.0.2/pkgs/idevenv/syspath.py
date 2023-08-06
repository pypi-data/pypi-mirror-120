# -*- coding: utf-8 -*-
import os
import sys
from platform import python_version_tuple
from pathlib import PureWindowsPath, PurePosixPath

from idevenv.viewer import *


def clean_path(p):
    # 운영체제 타입에 따라 path 를 수정한다
    if os.name == 'posix':
        return str(PurePosixPath(p))
    elif os.name == 'nt':
        return str(PureWindowsPath(p))



class Syspath(object):
    """
    pip로 설치되지 않은 패키지들의 경로를 수동으로 추가한다
    그러나, 최종적으로는 pip를 사용하라
    """
    def __init__(self, projectName, pypkgX=False):
        self._ProjectName = projectName
        self.set_BasePath()
        if pypkgX:
            p = f"{self._BasePath}/pypkgX/{self._ProjectName}"
        else:
            p = f"{self._BasePath}/{self._ProjectName}"
        self._ProjectPath = clean_path(p)
        self.add_project_packages()

    def set_BasePath(self, p=None):
        if p is None:
            if os.name == 'posix':
                p = "/Users/sambong/pjts"
            elif os.name == 'nt':
                p = 'C:\\pjts'
        self._BasePath = clean_path(p)

    def view(self):
        pretty_title(f'Current sys.path at {__file__}')
        pp.pprint(sorted(set(sys.path)))

    def add_venv_site_packages(self):
        # VirtualEnv Site-Packages 경로를 추가한다
        if os.name == 'posix':
            v = python_version_tuple()
            envpath = f"env/lib/python{v[0]}.{v[1]}/site-packages"
        elif os.name == 'nt':
            envpath = "env\\Lib\\site-packages"
        p = clean_path(f"{self._ProjectPath}/{envpath}")
        sys.path.append(p)
        sys.path = list(set(sys.path))

    def add_project_packages(self):
        # 소스코드 패키지 경로를 추가한다
        p = clean_path(f"{self._ProjectPath}/pkgs")
        sys.path.append(p)
        sys.path = list(set(sys.path))

    def add_uninstall_packages(self, projects):
        updated = []
        for project in projects:
            p = clean_path(f"{self._BasePath}/{project}/pkgs")
            sys.path.append(p)
            updated.append(p)
        sys.path = list(set(sys.path))

        pretty_title(f'!!! 경고 !!! at {__file__}')
        print(self.__doc__)
        print('임시로 추가한 패키지들 경로:')
        pp.pprint(updated)
