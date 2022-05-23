
# Plant Detector

![Sample Detection](/sample.png?raw=true "Sample Detection")

This sample code can detect the instance masks from an image
and estimate the green pixel count from each individual plant.

It's not perfect, as if you have multiple plants in the image that
overlap, then instances will be conjoined. But, if your setup is such
that a single plant is being imaged, or, your plant containers keep
the plants from overlapping, then this should work out purdy dang effectively.

## Install

```
python3 -m venv venv
pip3 install -r requirements.txt

python3 test.py
```

Modify the test script to pick up a specific image

### denoising/smoothing/contours
[](https://docs.opencv.org/3.4/d5/d69/tutorial_py_non_local_means.html)
[](https://betterprogramming.pub/3-steps-to-enhance-images-using-opencv-noise-reduction-in-python-f53d2abf2f6f)
[](https://stackoverflow.com/questions/52748270/how-to-remove-image-noise-using-opencv-python)
[](https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html)

### Apply object detection
[](https://curiousily.com/posts/object-detection-on-custom-dataset-with-tensorflow-2-and-keras-using-python/)
[](https://machinelearningmastery.com/how-to-train-an-object-detection-model-with-keras/)
[](https://github.com/matterport/Mask_RCNN#installation)
[](https://pyimagesearch.com/2020/10/05/object-detection-bounding-box-regression-with-keras-tensorflow-and-deep-learning/)