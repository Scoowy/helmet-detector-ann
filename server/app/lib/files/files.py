import os
from typing import Dict, List
import uuid
import base64
from io import BytesIO
from PIL import Image

from werkzeug.datastructures import FileStorage

from app.config import INPUT_FOLDER, OUTPUT_FOLDER
from app.lib.files.directories import createDirectory


def __uploadFile(file: FileStorage) -> Dict[str, str]:
    extensionFile = file.content_type.split('/')[-1]
    filename = str(uuid.uuid4()) + '.' + extensionFile
    filepath = os.path.join(INPUT_FOLDER, filename)

    file.save(filepath)

    return {'filename': filename, 'filepath': filepath}


def uploadFiles(files: List[FileStorage]) -> List[Dict[str, str]]:
    createDirectory(INPUT_FOLDER, deleteContent=True)

    result = []

    for file in files:
        if file:
            result.append(__uploadFile(file))

    return result


def __encodeImg(filepath: str) -> str:
    img = Image.open(filepath, mode='r')
    buffered = BytesIO()
    img.save(buffered, format='JPEG')
    imgBase64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return imgBase64


def encodeImgs(filepaths: List[str]) -> List[str]:
    result = []

    for filepath in filepaths:
        result.append(__encodeImg(filepath))

    return result


def __downloadFile(filename: str) -> str:
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    img = __encodeImg(filepath)
    return img


def downloadFiles(filesnames: List[str]) -> List[str]:
    filepaths = [os.path.join(OUTPUT_FOLDER, filename)
                 for filename in filesnames]
    imgs = encodeImgs(filepaths)

    return imgs
