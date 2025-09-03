'''This script enhances a signature image by converting it to black on a transparent background.
It uses the Pillow library.
was created by perplexity.ai
https://www.perplexity.ai/search/how-to-make-the-line-in-the-im-rlllRh.1TaKlYWnbCKruLA#1'''

from PIL import Image, ImageOps, ImageFilter

# Load image (replace filename as needed)
img = Image.open('/Users/nikolask/Documents/Private/SIGNATURES/doris-signature.png').convert('RGBA')

# Convert image to grayscale (removes color but keeps transparency)
gray_img = ImageOps.grayscale(img)

# Invert grayscale so signature becomes bright
inverted_img = ImageOps.invert(gray_img)

# Use a threshold to make lines solid black, background transparent
threshold = 100
binary_img = inverted_img.point(lambda p: 255 if p > threshold else 0)

# Combine binary mask with original alpha
alpha = img.split()[-1]
result = Image.merge('RGBA', (binary_img, binary_img, binary_img, alpha))

# Optional: Thicken lines using a filter
result = result.filter(ImageFilter.MaxFilter(3))

result.save('signature_black.png')
