from PIL import Image
import os

def get_outname(fname, r, g, b):
    return '%s_%s_%s_%s_jpeg.jpg' % (fname, r, g, b)

def jpegify(fpath, background=(255,255,255)):
    """
    Takes a filename relative to MEDIA_PATH
    """
    base = os.path.basename(fpath)
    path = os.path.dirname(fpath)
    outname = get_outname(base, *background)
    outpath = os.path.join(path, outname)
    if not os.path.exists(outpath):
        im = Image.open(fpath)
        bg = Image.new('RGBA', im.size, background)
        bg.paste(im, im)
        im = bg.convert('RGB')
        im.save(outpath)
    return outpath