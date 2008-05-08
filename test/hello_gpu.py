import pycuda.driver as drv
import numpy
import numpy.linalg as la

drv.init()
dev = drv.Device(0)
ctx = dev.make_context()

mod = drv.SourceModule("""
__global__ void multiply_them(float *dest, float *a, float *b)
{
  const int i = threadIdx.x;
  dest[i] = a[i] * b[i];
}
""")

multiply_them = mod.get_function("multiply_them")

import numpy
a = numpy.random.randn(400).astype(numpy.float32)
b = numpy.random.randn(400).astype(numpy.float32)

dest = numpy.zeros_like(a)
multiply_them(
        drv.Out(dest), drv.In(a), drv.In(b),
        shared=4096, block=(400,1,1))

print dest-a*b
del mod
