from flask import Blueprint
from flask_socketio import emit

from app.config import INPUT_FOLDER
from app.lib.detector.models import YoloV5ModelSingleton
from app.lib.detector.predict import predictRealTime, predictImgs, predictVid
from app.lib.files.directories import getFilesnamesAndFilepathsInDirectory
from app.server.responses.genericResponses import genericResponse
from app import socketio

yoloRoutes = Blueprint('yoloRoutes', __name__)


@yoloRoutes.get('/image')
def predictImages():
    filepaths = getFilesnamesAndFilepathsInDirectory(INPUT_FOLDER)

    results = predictImgs(filepaths, statistics=True)

    if not results:
        return genericResponse('No helmet detected', 400)

    if isinstance(results, tuple):
        return genericResponse({'message': 'Ok', 'predictions': results[0], 'statistics': results[1]})

    return genericResponse({'message': 'Ok', 'predictions': results})


@yoloRoutes.get('/video')
def predictVideo():
    filepath = getFilesnamesAndFilepathsInDirectory(INPUT_FOLDER)

    videoPath = filepath[0]['filepath']
    videoName = filepath[0]['filename']

    result = predictVid(videoName, videoPath)

    if not result:
        return genericResponse('No helmet detected', 400)

    return genericResponse({'message': 'ok', 'predictions': result})


@socketio.on('load-model')
def loadModel():
    print('Initialize model')
    model = YoloV5ModelSingleton()
    model.loadModel()
    print('Model initialized')

    emit('model-loaded')


@socketio.on('predict')
def predictSocket(dataImage):
    encodedImg, numDetections, iddle = next(predictRealTime(dataImage))

    if encodedImg is not None:
        emit('predicted', (encodedImg, numDetections))
