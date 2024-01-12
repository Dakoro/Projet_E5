import numpy as np

format_to_dtype = {
    'uchar': np.uint8,
    'char': np.int8,
    'ushort': np.uint16,
    'short': np.int16,
    'uint': np.uint32,
    'int': np.int32,
    'float': np.float32,
    'double': np.float64,
    'complex': np.complex64,
    'dpcomplex': np.complex128,
}


def vips_to_numpy(vips_img):
    img = np.ndarray(
        buffer=vips_img.write_to_memory(),
        dtype=format_to_dtype[vips_img.format],
        shape=[vips_img.height, vips_img.width, vips_img.bands])
    return img