"""
Copyright 2020 The Microsoft DeepSpeed Team
"""
import torch
from .builder import CUDAOpBuilder, is_rocm_pytorch


class FusedLambBuilder(CUDAOpBuilder):
    BUILD_VAR = 'DS_BUILD_FUSED_LAMB'
    NAME = "fused_lamb"

    def __init__(self):
        super().__init__(name=self.NAME)

    def absolute_name(self):
        return f'deepspeed.ops.lamb.{self.NAME}_op'

    def sources(self):
        return ['csrc/lamb/fused_lamb_cuda.cpp', 'csrc/lamb/fused_lamb_cuda_kernel.cu']

    def include_paths(self):
        return ['csrc/includes']

    def cxx_args(self):
        return ['-O3'] + self.version_dependent_macros()

    def nvcc_args(self):
        nvcc_flags=['-O3'] + self.version_dependent_macros()
        if not is_rocm_pytorch:
            nvcc_flags.extend(['-lineinfo', '--use_fast_math'] + self.compute_capability_args())
        return nvcc_flags