from . import nude
from os import path
from cv2 import imwrite
def not_in_data(name):
    return not path.isfile(path.join(path.dirname(__file__), 'checkpoints', name))
def gui():
    from os import getcwd
    from tkinter import Tk
    from tkinter.messagebox import showerror
    from tkinter.filedialog import askopenfilename, asksaveasfilename
    Tk().withdraw()
    if not_in_data("cm.lib") or not_in_data("mm.lib") or not_in_data("mn.lib"):
        return showerror("Setup issue", "You didn't set up nude or set it up incorrectly try running \"python3 -m nude.setup\"")
    types = [("Bitmap Image File", ".bpm .BPM .dib .DIB"), ("JPEG", ".jpeg .JPEG .jpg .JPG .jpe .JPE"), ("JPEG 2000", ".jp2 .JP2"), ("Portable Network Graphics", ".png .PNG"), ("Portable Bitmap", ".pbm .PBM"), ("Portable Graymap", ".pgm .PGM"), ("Portable Pixmap", ".ppm .PPM"), ("Sun Raster", ".sr .SR .ras .RAS"), ("Tag Image File Format", ".tiff .TIFF .tif .TIF")]
    input_file = askopenfilename(initialdir=getcwd(), filetypes = types)
    if not input_file: exit()
    chosen_type = None
    for i in types:
        for type in i[1].split(' '):
            if input_file.endswith(type):
                chosen_type = i
                break
        if chosen_type: break
    output_file = asksaveasfilename(filetypes=[chosen_type])
    if not output_file: exit()
    imwrite(output_file, nude(input_file))
def cli():
    if not_in_data("cm.lib") or not_in_data("mm.lib") or not_in_data("mn.lib"):
        class SetupIssue(Exception):
            __module__ = Exception.__module__
            __str__ = lambda _: "You didn't set up nude or set it up incorrectly try running \"python3 -m nude.setup\""
        raise SetupIssue()
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, required=True, help="Give the name of the input image")
    parser.add_argument('-o', '--output_file', type=str, required=True, help="Give a name for the output image")
    parser.add_argument('-as', '--areola_size', type=float, default=1, help="Scale the areola on a scale of 0 to 2")
    parser.add_argument('-ns', '--nipple_size', type=float, default=1, help="Scale the nipples on a scale of 0 to 2")
    parser.add_argument('-ts', '--tit_size', type=float, default=1, help="Scale the tits on a scale of 0 to 2")
    parser.add_argument('-vs', '--vagina_size', type=float, default=1, help="Scale the vagina on a scale of 0 to 2")
    parser.add_argument('-hs', '--hair_size', type=float, default=1, help="Scale the hair on a scale of 0 to 2")
    args = parser.parse_args()
    imwrite(args.output_file, nude(args.input_file, args.areola_size, args.nipple_size, args.tit_size, args.vagina_size, args.hair_size))
