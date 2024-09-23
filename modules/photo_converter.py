from PIL import Image
import numpy as np

def rgb_to_hex555(red, green, blue):
    return "0x%0.4X" % ((int(red / 255 * 31) << 10) | (int(green / 255 * 31) << 5) | (int(blue / 255 * 31)))

if __name__ == '__main__':
    path = 'images/wolf64.jpg'
    image = Image.open(path).convert('RGB')
    rgbArray = np.array(image)
    test = np.vectorize(rgb_to_hex565)(rgbArray[:,:,0], rgbArray[:,:,1], rgbArray[:,:,2])
    lines = []
    for r in test:
        for color in r:
            lines.append(color)
            #lines.append(f"MOV r1, #{color}")
            #lines.append("push r1")

    with open('test.hex', 'w') as f:
        f.writelines('\n'.join(lines))

