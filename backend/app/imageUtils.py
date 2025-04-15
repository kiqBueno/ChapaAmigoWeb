from .logging_config import setup_logging
from io import BytesIO
from PIL import Image

# Configure logging
setup_logging()

def cropImage(imgBytes):
    img = Image.open(imgBytes)
    width, height = img.size
    cropHeight = int(height * 0.09)
    croppedImg = img.crop((0, cropHeight, width, height - cropHeight))
    croppedImgBytes = BytesIO()
    croppedImg.save(croppedImgBytes, format='PNG')
    croppedImgBytes.seek(0)
    return croppedImgBytes

def addTransparency(imagePath, transparency):
    img = Image.open(imagePath).convert("RGBA")
    alpha = img.split()[3]
    alpha = alpha.point(lambda p: p * transparency)
    img.putalpha(alpha)
    imgBytes = BytesIO()
    img.save(imgBytes, format='PNG')
    imgBytes.seek(0)
    return imgBytes