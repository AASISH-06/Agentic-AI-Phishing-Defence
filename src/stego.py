from PIL import Image
import io

def extract_lsb_text_from_image_bytes(image_bytes):
    # open image bytes
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    pixels = list(img.getdata())
    bits = []
    for r,g,b in pixels:
        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)
    # group bits into bytes
    bytes_out = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i+j < len(bits):
                byte = (byte << 1) | bits[i+j]
        bytes_out.append(byte)
    # convert to string until null terminator or EOF
    chars = []
    for b in bytes_out:
        if b == 0:
            break
        try:
            chars.append(chr(b))
        except:
            break
    text = ''.join(chars)
    return text.strip()

# helper that accepts a filename or file-stream
def extract_lsb_from_file(path_or_fileobj):
    if hasattr(path_or_fileobj, 'read'):
        data = path_or_fileobj.read()
        return extract_lsb_text_from_image_bytes(data)
    else:
        with open(path_or_fileobj, 'rb') as f:
            return extract_lsb_text_from_image_bytes(f.read())
