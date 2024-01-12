import pyvips
import cProfile
import pstats
import numpy as np
from memory_profiler import profile
from pdf2image import convert_from_path


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


@profile
def pdf2image_conversion(path):
    imgs = convert_from_path(path, dpi=300)
    return imgs


@profile
def pyvips_conversion(path):
    pdf = pyvips.Image.new_from_file(path, dpi=300)
    n_pages = pdf.get_n_pages()
    imgs = [vips_to_numpy(pyvips.Image.new_from_file(path, dpi=300, page=i)) for i in range(n_pages)]
    return imgs


def profile_func(func, *args, profile_fn):
    profiler = cProfile.Profile()
    profiler.enable()
    func(*args)
    profiler.disable()
    stat = pstats.Stats(profiler).sort_stats('cumtime')
    stat.dump_stats(profile_fn)


if __name__ == '__main__':
    test_fp = '/home/dakoro/Téléchargements/lbdl.pdf'
    profile_func(pyvips_conversion, test_fp, profile_fn='pyvips.prof')
    profile_func(pdf2image_conversion, test_fp, profile_fn='pdf2image.prof')
