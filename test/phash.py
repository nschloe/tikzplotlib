from PIL import Image
import numpy
import scipy.fftpack


def _binary_array_to_hex(arr):
    """
    internal function to make a hex string out of a binary array
    """
    h = 0
    s = []
    for i, v in enumerate(arr.flatten()):
        if v:
            h += 2**(i % 8)
        if (i % 8) == 7:
            s.append(hex(h)[2:].rjust(2, '0'))
            h = 0
    return "".join(s)


def phash(image, hash_size=8, highfreq_factor=4):
    '''Perceptual Hash computation.
    Implementation follows
    http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
    @image must be a PIL instance.
    '''
    img_size = hash_size * highfreq_factor
    image = image.convert('L').resize((img_size, img_size), Image.ANTIALIAS)
    pixels = numpy.array(
        image.getdata(),
        dtype=numpy.float
        ).reshape((img_size, img_size))
    dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
    print(dct)
    print(sum(sum(dct)))
    dctlowfreq = dct[:hash_size, :hash_size]
    med = numpy.median(dctlowfreq)
    diff = dctlowfreq > med
    print(diff)
    # <http://stackoverflow.com/a/4066807/353337>
    #a = sum(1<<i for i, b in enumerate(dff) if b)
    return _binary_array_to_hex(diff)
