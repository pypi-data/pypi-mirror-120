### Instaresizer-0.0.3

#### Description

Takes in an image URL as an argument and returns PIL image object which resizes the original image to optimally fit instagram supported aspect ratio. 

#### Usage

##### Installation

```
pip install instaresizer
```

##### Example

1. Importing the library
```
#!/usr/bin/env python3

from instaresizer import instasize

```
2. Usage - resizing remote image file supplied via a URL. 
```
image_url = 'https://s3.amazonaws.com/images.seroundtable.com/30th-anniversary-of-the-world-wide-web-google-1552390014.gif'

img = instasize.resize_remote(image_url)

img.save('resized_file.png', 'PNG')
```
3. Usage - resizing local image file supplied via a URL. 
```
image = Image.open("test_image.jpeg")

img = instasize.resize_image(image)

img.save('resized_file.png', 'PNG')
```
