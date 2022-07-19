import time
import os
from typing import Any, Dict, List

from PIL import Image as PILImage
from PIL.Image import Image
from cv2 import cvtColor, imencode, COLOR_BGR2RGB, VideoCapture, VideoWriter, VideoWriter_fourcc, CAP_PROP_FPS, \
    CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_COUNT
from yolov5.models.common import Detections

from app.lib.detector.models import YoloV5ModelSingleton
from app.lib.processes.imageProcedures import decodeDataImage, encodeDataImage

from app.lib.files.directories import createDirectory
from app.lib.files.files import OUTPUT_FOLDER

from app.lib.utils.TimeUtils import initTimer, endTimer

CURRENT_DIR = os.path.join(os.getcwd(), 'yolov5s_helmet.pt')


def predictImgs(files: List[Dict[str, str]], statistics=False) -> bool | tuple[List[Dict[str, Any]], Dict[str, float]] | \
        List[Dict[str, Any]]:
    # Load model singleton
    model = YoloV5ModelSingleton()
    model.loadModel()

    # Set default values for variables
    imgs: List[Image] = []
    results: Detections = []

    # START Load process
    print('Load images...', end=' ')
    start = initTimer()
    try:
        imgs = [PILImage.open(f['filepath']) for f in files]
    except Exception as e:
        print(e)
        return False
    loadingTime = endTimer(start)
    print(f'Load in time: {loadingTime:.2f}s')
    # END Load process

    # START Predict process
    print('Predict...', end=' ')
    start = initTimer()
    try:
        # results = model(imgs)
        results = model.detect(imgs)
    except Exception as e:
        print(e)
        return False
    predictTime = endTimer(start)
    print(f'Predict in time: {predictTime:.2f}s')
    # END Predict process

    # START Render process
    print('Render...', end=' ')
    start = initTimer()
    try:
        results.render()
    except Exception as e:
        print(e)
        return False
    renderTime = endTimer(start)
    print(f'Render in time: {renderTime:.2f}s')
    # END Render process

    # START Save process
    print('Save...')
    start = initTimer()
    try:
        createDirectory(OUTPUT_FOLDER, deleteContent=True)
        results.save(save_dir=OUTPUT_FOLDER)
    except Exception as e:
        print(e)
        return False
    saveTime = endTimer(start)
    print(f'Save in time: {saveTime:.2f}s')
    # END save process

    # Extract the results to a list of dictionaries
    dictResults = [xyxy.to_dict(orient='records')
                   for xyxy in results.pandas().xyxy]

    # Prepare result data
    result = [{'filename': filename, 'detections': dictResult}
              for filename, dictResult in zip(results.files, dictResults)]

    # Return statistics if required
    if statistics:
        return result, {'loadingTime': loadingTime, 'predictTime': predictTime, 'renderTime': renderTime,
                        'saveTime': saveTime}

    return result


def predictRealTime(dataImage, iddle: bool = True):
    model = YoloV5ModelSingleton()

    if iddle:
        img = decodeDataImage(dataImage)

        if img is None:
            yield None, True

        # Detect procces
        predicts = model.detect(img)
        predicts.render()

        numDetections = len(
            predicts.pandas().xyxy[0].to_dict(orient='records'))
        imgPredicted = predicts.imgs[0]

        # To gray scale
        frame = cvtColor(imgPredicted, COLOR_BGR2RGB)
        (flag, imgCode) = imencode('.jpg', frame)

        if not flag:
            yield None, True
        # if not flag:
        #     continue

        # Return enconded image and flag to proccess next image
        yield encodeDataImage(imgCode), numDetections, True


def predictVid(videoName: str, videoPath: str):
    # Load model
    model = YoloV5ModelSingleton()
    model.loadModel()

    vid = None

    # START Load process
    print('Load video...', end=' ')
    start = initTimer()
    try:
        vid = VideoCapture(videoPath)
    except Exception as e:
        print(e)
        return False
    loadingTime = endTimer(start)
    print(f'Load in time: {loadingTime:.2f}s')
    # END Load process

    # Extract data from video
    fps = float(vid.get(CAP_PROP_FPS))
    width = int(vid.get(CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(CAP_PROP_FRAME_HEIGHT))
    frames = int(vid.get(CAP_PROP_FRAME_COUNT))

    # START Load video writer
    createDirectory(OUTPUT_FOLDER, deleteContent=True)

    fourcc = VideoWriter_fourcc(*'AVC1')
    output = VideoWriter(os.path.join(
        OUTPUT_FOLDER, videoName), fourcc, fps, (width, height))
    # END Load video writer

    # Variables for detect optimization
    numFrameToProcess = 2 if fps <= 25 else 3
    numFrameActual = 1

    start = initTimer()
    while vid.isOpened():
        ret, frame = vid.read()

        if ret == True:
            if numFrameActual % numFrameToProcess == 0:
                print(f'Inference frame {numFrameActual} | {frames}')

                # Detect procces
                predicts = model.detect(frame)
                predicts.render()

                numDetections = len(
                    predicts.pandas().xyxy[0].to_dict(orient='records'))
                framePredicted = predicts.imgs[0]

                # Write the predicted frame
                output.write(framePredicted)
            else:
                output.write(frame)

        else:
            break

        numFrameActual += 1

    # Close and save video writer
    vid.release()
    output.release()

    detectionTime = endTimer(start)

    # Results
    return [{
        'filename': videoName,
        'detections': 1,
        'statistics': {
            'fps': fps,
            'dimensions': {
                'width': width,
                'height': height
            },
            'frames': frames,
            'time': detectionTime
        }
    }]
