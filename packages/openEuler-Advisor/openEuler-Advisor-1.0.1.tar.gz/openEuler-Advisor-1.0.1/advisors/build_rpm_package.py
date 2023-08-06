#!/usr/bin/python3

# -*- encoding=utf-8 -*-
"""
# **********************************************************************************
# Copyright (c) Huawei Technologies Co., Ltd. 2020-2020. All rights reserved.
# [openeuler-jenkins] is licensed under the Mulan PSL v1.
# You can use this software according to the terms and conditions of the Mulan PSL v1.
# You may obtain a copy of Mulan PSL v1 at:
#     http://license.coscl.org.cn/MulanPSL
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v1 for more details.
# Author:
# Create: 2020-09-23
# Description: build result rpm package info
# **********************************************************************************
"""

import os
import re


class BuildRPMPackage():
    """
    build result rpm package info
    """

    LINKMAGIC = "0X080480000XC0000000"      # 不要和gitee中用户名相同

    def __init__(self, repo, rpmbuild_dir):
        """

        :param repo: 包名
        :param rpmbuild_dir: rpmbuild路径
        """
        self._repo = repo
        self._rpmbuild_dir = rpmbuild_dir

        self._rpm_packages = {"srpm": {}, "rpm": {}}
        self._package_structure(rpmbuild_dir)

    def main_package_local(self):
        """
        返回主包在本地路径
        :param arch:
        :return:
        """
        package = self._rpm_packages["rpm"].get(self._repo)
        if not package:
            # not exist
            return None

        return os.path.join(self._rpmbuild_dir, "RPMS", package["arch"], package["fullname"])

    def main_package_in_repo(self, committer, arch, rpm_repo_url):
        """
        返回主包在repo mirror路径
        :param committer:
        :param arch:
        :param rpm_repo_url:
        :return:
        """
        return self.get_package_path(committer, arch, self._repo, rpm_repo_url)

    def last_main_package(self, arch, rpm_repo_url):
        """
        返回主包在repo mirror链接路径（上次构建的rpm包）
        :param arch:
        :param rpm_repo_url: 构建出的rpm包保存的远端地址
        :return:
        """
        return os.path.join(rpm_repo_url, self.LINKMAGIC, arch, self._repo)

    def debuginfo_package_local(self):
        """
        返回debuginfo包在本地路径
        :return:
        """
        package = self._rpm_packages["rpm"].get("{}-debuginfo".format(self._repo))
        if not package:
            # not exist
            return None

        return os.path.join(self._rpmbuild_dir, "RPMS", package["arch"], package["fullname"])

    def debuginfo_package_in_repo(self, committer, arch, rpm_repo_url):
        """
        返回debuginfo包在repo mirror路径
        :param committer:
        :param arch:
        :return:
        """
        return self.get_package_path(committer,
                                     arch, "{}-debuginfo".format(self._repo), rpm_repo_url)

    def last_debuginfo_package(self, arch, rpm_repo_url):
        """
        返回debuginfo包在repo mirror链接路径（上次构建的rpm包）
        :param arch:
        :return:
        """
        return os.path.join(rpm_repo_url, self.LINKMAGIC, arch, "{}-debuginfo".format(self._repo))

    @staticmethod
    def checkabi_md_in_repo(committer, repo, arch, md_file, rpm_repo_url):
        """
        返回checkabi结果在repo mirror路径
        :param committer:
        :param arch:
        :param md:
        :param rpm_repo_url:
        :return:
        """
        return os.path.join(rpm_repo_url, committer, repo, arch, md_file)

    def get_package_path(self, committer, arch, name, remote_url):
        """
        返回包在repo mirror路径
        :param committer:
        :param arch:
        :param name: 包名
        :param remote_url: 仓库远端地址
        :return:
        """
        package = self._rpm_packages["rpm"].get(name)
        if not package:
            # not exist
            return None

        if arch == "noarch":
            full = os.path.join(remote_url, committer, name, arch, package["fullname"])
        else:
            full = os.path.join(remote_url, committer, name, arch, "noarch", package["fullname"])
        return full

    def get_package_fullname(self, name):
        """
        获取包全名
        :param name:
        :return:
        """
        package = self._rpm_packages["rpm"].get(name)
        return package["fullname"] if package else name

    def get_srpm_path(self):
        """
        for future
        :return:
        """
        raise NotImplementedError

    @staticmethod
    def extract_rpm_name(rpm_fullname):
        """
        取出名字部分
        :param rpm_fullname:
        :return:
        """
        try:
            rpm_name = re.match("(.*)-[0-9.]+-.*rpm", rpm_fullname)
        except NameError:
            return rpm_fullname
        else:
            return rpm_name.group(1)

    def _package_structure(self, rpmbuild_dir):
        """
        rpm package 结构
        :param rpmbuild_dir: rpmbuild路径
        :return:
        """
        rpms_dir = os.path.join(rpmbuild_dir, "RPMS")
        for dirname, _, filenames in os.walk(rpms_dir):
            arch = dirname.split("/")[-1]
            if arch == "i386":
                aarch = "x86-64"
            else:
                aarch = arch
            for filename in filenames:
                name = self.extract_rpm_name(filename)
                self._rpm_packages["rpm"][name] = {"name": name, "fullname": filename,
						           "arch": aarch}

        srpms = os.path.join(rpmbuild_dir, "SRPMS")
        for dirname, _, filenames in os.walk(srpms):
            for filename in filenames:
                name = self.extract_rpm_name(filename)
                self._rpm_packages["srpm"][name] = {"name": name, "fullname": filename}
