from distutils.unixccompiler import UnixCCompiler
import distutils.ccompiler
import os
import distutils

class UnixNvccCompiler(UnixCCompiler):
    nvcc_so = ["nvcc"]
    UnixCCompiler.language_map[".cu"] = "c++"
    UnixCCompiler.src_extensions.append(".cu")

    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        """
        Interface for this is exactly the same as its parent, except that now
        the caller has to pass extra_postargs as a hash of options. The 2 keys
        inside it are options for 'nvcc' and 'gcc' compilers. Eg:
        extra_postargs = {
          "nvcc" : ["-arch=sm60"]
          "gcc"  : ["-Wall"]
        }
        """
        default_so = self.compiler_so
        if os.path.splitext(src)[1] == ".cu":
            self.compiler_so = self.nvcc_so
            _extra_postargs = extra_postargs["nvcc"] if "nvcc" in extra_postargs else []
        else:
            _extra_postargs = extra_postargs["gcc"] if "gcc" in extra_postargs else []
        super(UnixNvccCompiler, self)._compile(obj, src, ext, cc_args,
                                               _extra_postargs, pp_opts)
        self.compiler_so = default_so

# helps distutils core will be able to find our nvcc compiler
distutils.unixccompiler.UnixNvccCompiler = UnixNvccCompiler

# TODO: add support for msvc-cuda
distutils.ccompiler.compiler_class["unix-cuda"] = ("unixccompiler",
                                                   "UnixNvccCompiler",
                                                   "CUDA compiler on UNIX")
