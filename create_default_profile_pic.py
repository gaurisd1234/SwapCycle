from PIL import Image, ImageDraw
import os

# Create directory if it doesn't exist
os.makedirs('media/profile_pics', exist_ok=True)

# Create a simple colored image for default profile picture
img = Image.new('RGB', (200, 200), color='lightblue')
# Draw a circle for the avatar
draw = ImageDraw.Draw(img)
draw.ellipse([40, 40, 160, 160], fill='darkblue')
img.save('media/profile_pics/default.jpg', 'JPEG')