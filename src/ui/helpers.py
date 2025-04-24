import io
from PIL import Image, ImageTk
import cairosvg
    
def load_svg_to_image(filepath, size=(80, 80)):
    png_data = cairosvg.svg2png(url=filepath, output_width=size[0], output_height=size[1])
    image = Image.open(io.BytesIO(png_data)).resize(size,resample=Image.NEAREST)
    return ImageTk.PhotoImage(image)
