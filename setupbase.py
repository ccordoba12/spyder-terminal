
"""
General setup rules to download external JS dependencies
via Bower

Some functions were taken from the Jupyter Notebook
setupbase definition
See: https://github.com/jupyter/notebook/blob/master/setupbase.py
"""

import os
import sys
import pipes

from distutils import log
from distutils.core import Command
from setuptools.command.develop import develop
from setuptools.command.sdist import sdist
from subprocess import check_call

if sys.platform == 'win32':
    from subprocess import list2cmdline
else:
    def list2cmdline(cmd_list):
        return ' '.join(map(pipes.quote, cmd_list))


repo_root = os.path.dirname(os.path.abspath(__file__))


def run(cmd, *args, **kwargs):
    """Echo a command before running it"""
    log.info('> ' + list2cmdline(cmd))
    kwargs['shell'] = (sys.platform == 'win32')
    return check_call(cmd, *args, **kwargs)


class DevelopWithBuildStatic(develop):
    def install_for_development(self):
        self.run_command('build_static')
        return develop.install_for_development(self)


class SdistWithBuildStatic(sdist):
    def make_distribution(self):
        self.run_command('build_static')
        return sdist.make_distribution(self)


class BuildStatic(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        log.info("running [bower install]")
        run(['bower', 'install', '--allow-root'], cwd=repo_root)
