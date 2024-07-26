from PIL import Image as PILImage
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid


def process_image(file):
    img = PILImage.open(file)
    img = img.convert("RGB")
    img_io = BytesIO()
    img.save(img_io, format="JPEG", quality=40)
    img_io.seek(0)

    file_name = f"{uuid.uuid4()}.jpeg"
    profile = InMemoryUploadedFile(
        img_io, None, file_name, "image/jpeg", img_io.getbuffer().nbytes, None
    )

    return profile
