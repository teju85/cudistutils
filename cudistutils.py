from Cython.Distutils import build_ext
import os
import subprocess
import distutils
import nvcccompiler


class cuda_build_ext(build_ext):
    def initialize_options(self):
        super(cuda_build_ext, self).initialize_options()
        self.compiler = "unix-cuda"


class CudaEnv:
    def __init__(self):
        nvcc = self._find_in_path("nvcc", os.environ["PATH"])
        if nvcc is None:
            raise EnvironmentError("nvcc binary could not be "
                                   "located in your $PATH")
        home = os.path.dirname(os.path.dirname(nvcc))
        self.include = os.path.join(home, "include")
        self.lib64 = os.path.join(home, "lib64")
        self.base_cuda_libs = ["cudart"]
        self.version = self._nvcc_version()
        self.gencode = self._default_gencode()

    def default_nvcc_opts(self):
        out = self.gencode + ["--ptxas-options=-v", "-Xcompiler", "-fPIC"]
        return out

    #ref: http://code.activestate.com/recipes/52224-find-a-file-given-a-search-path/
    def _find_in_path(self, name, path):
        for dir in path.split(os.pathsep):
            binpath = os.path.join(dir, name)
            if os.path.exists(binpath):
                return os.path.abspath(binpath)
        return None

    def _default_gencode(self):
        version_map = {
            b"8.0" : ["62", "61", "60",  # Pascal
                      "53", "52", "50",  # Maxwell
                      "37", "35"]        # Kepler (only sm35 onwards)
        }
        version_map[b"9.0"] = ["70"] + version_map[b"8.0"]  # Volta support
        version_map[b"9.1"] = version_map[b"9.0"]
        if self.version not in version_map:
            raise EnvironmentError("CUDA version %s is not supported" % self.version)
        versions = version_map[self.version]
        arr = []
        for ver in versions:
            arr.append("-gencode")
            if isinstance(ver, tuple):
                arch, code = ver
            else:
                arch, code = ver, ver
            arr.append("arch=compute_%s,code=sm_%s" % (arch, code))
        return arr

    # TODO: do this is in a more pythonic way?
    def _nvcc_version(self):
        cmd = "nvcc --version | tail -n1 | awk '{print $(NF-1)}' | sed -e 's/,//'"
        out = subprocess.check_output(cmd, shell=True)
        out = out.rstrip()
        return out
