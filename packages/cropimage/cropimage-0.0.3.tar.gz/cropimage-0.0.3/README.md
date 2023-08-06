# cropimage
This is a simple toolkit for cropping main body from pictures.

<p align="center"><img title="crop_example" src="https://github.com/haofanwang/cropimage/raw/main/assets/example.png"></p>

## Installation
~~~sh
pip install cropimage
~~~

## Get Started
~~~python
from cropimage import Cropper

cropper = Cropper()

# Get a Numpy array of the cropped image
cropped_array = cropper.crop('./images/input.jpg', completeness=True, target_size=(500,500))

# Save the cropped image
cv2.imwrite('cropped.jpg', result)
~~~

## More Results
<p align="center"><img title="crop_example" src="https://github.com/haofanwang/cropimage/raw/main/assets/example1.png"></p>

## Contributing
If you find any issue of this project, feel free to open an issue or contribute!
