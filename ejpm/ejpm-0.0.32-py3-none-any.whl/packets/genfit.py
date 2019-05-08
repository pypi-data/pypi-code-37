"""
This file provides information of how to build and configure Genfit framework:
https://github.com/GenFit/GenFit

"""

import os

from ejpm.engine.commands import run, workdir
from ejpm.engine.env_gen import Set, Append
from ejpm.engine.installation import PacketInstallationInstruction


class GenfitInstallation(PacketInstallationInstruction):
    """Provides data for building and installing Genfit framework
    source_path  = {app_path}/src/{version}          # Where the sources for the current version are located
    build_path   = {app_path}/build/{version}        # Where sources are built. Kind of temporary dir
    install_path = {app_path}/root-{version}         # Where the binary installation is
    """


    def __init__(self, default_tag='master', build_threads=8):
        """
        Installs Genfit track fitting framework
        """

        # Set initial values for parent class and self
        super(GenfitInstallation, self).__init__('genfit')
        self.build_threads = build_threads
        self.clone_command = ''             # will be set by self.set_app_path
        self.build_cmd = ''                 # will be set by self.set_app_path

    def setup(self, app_path):
        """Sets all variables like source dirs, build dirs, etc"""

        # We don't care about tags and have only 1 branch name
        branch = 'master'

        #
        # use_common_dirs_scheme sets standard package variables:
        # source_path  = {app_path}/src/{version}          # Where the sources for the current version are located
        # build_path   = {app_path}/build/{version}        # Where sources are built. Kind of temporary dir
        # install_path = {app_path}/root-{version}         # Where the binary installation is
        self.use_common_dirs_scheme(app_path, branch)

        #
        # JANA download link. Clone with shallow copy
        # TODO accept version tuple to get exact branch
        self.clone_command = "git clone --depth 1 -b {branch} https://github.com/GenFit/GenFit {source_path}"\
            .format(branch=branch, source_path=self.source_path)

        # cmake command:
        # the  -Wno-dev  flag is to ignore the project developers cmake warnings for policy CMP0075
        self.build_cmd = "cmake -Wno-dev -DCMAKE_INSTALL_PREFIX={install_path} {source_path}" \
                         "&& cmake --build . -- -j {build_threads}" \
                         "&& cmake --build . --target install" \
                         .format(
                             source_path=self.source_path,    # cmake source
                             install_path=self.install_path,  # Installation path
                             build_threads=self.build_threads)     # make global options like '-j8'. Skip now

    def step_install(self):
        self.step_clone()
        self.step_build()

    def step_clone(self):
        """Clones JANA from github mirror"""

        # Check the directory exists and not empty
        if os.path.exists(self.source_path) and os.path.isdir(self.source_path) and os.listdir(self.source_path):
            # The directory exists and is not empty. Nothing to do
            return
        else:
            # Create the directory
            run('mkdir -p {}'.format(self.source_path))

        # Execute git clone command
        run(self.clone_command)

    def step_build(self):
        """Builds JANA from the ground"""

        # Create build directory
        run('mkdir -p {}'.format(self.build_path))

        # go to our build directory
        workdir(self.build_path)

        # run scons && scons install
        run(self.build_cmd)

    def step_reinstall(self):
        """Delete everything and start over"""

        # clear sources directories if needed
        run('rm -rf {}'.format(self.app_path))

        # Now run build root
        self.step_install()

    @staticmethod
    def gen_env(data):
        path = data['install_path']
        """Generates environments to be set"""

        yield Set('GENFIT', path)
        yield Set('GENFIT_DIR', path)

        # it could be lib or lib64. There are bugs on different platforms (RHEL&centos and WSL included)
        # https://stackoverflow.com/questions/46847939/config-site-for-vendor-libs-on-centos-x86-64
        # https: // bugzilla.redhat.com / show_bug.cgi?id = 1510073

        import platform
        if platform.system() == 'Darwin':
            yield Append('DYLD_LIBRARY_PATH', os.path.join(path, 'lib'))
            yield Append('DYLD_LIBRARY_PATH', os.path.join(path, 'lib64'))

        yield Append('LD_LIBRARY_PATH', os.path.join(path, 'lib'))
        yield Append('LD_LIBRARY_PATH', os.path.join(path, 'lib64'))

    #
    # OS dependencies are a map of software packets installed by os maintainers
    # The map should be in form:
    # os_dependencies = { 'required': {'ubuntu': "space separated packet names", 'centos': "..."},
    #                     'optional': {'ubuntu': "space separated packet names", 'centos': "..."}
    # The idea behind is to generate easy to use instructions: 'sudo apt-get install ... ... ... '
    os_dependencies = {
        'required': {
            'ubuntu': "libboost-dev libeigen3-dev",
            'centos': "boost-devel eigen3-devel"
        },
        'optional': {
            'ubuntu': "",
            'centos': ""
        },
    }