### Instaresizer

#### Description

Takes in an image URL as an argument and returns PIL image object which resizes the original image to optimally fit instagram supported aspect ratio. 

#### Usage

##### Installation

```
pip install instaresizer
```

##### Example

###### Importing the library
```
#!/usr/bin/env python3
from instaresizer import instasize
```
###### Usage - resizing remote image file supplied via a URL. 

This is useful if the image is publicly accessible with no additional authentication requirements. 
```
image_url = 'https://s3.amazonaws.com/images.seroundtable.com/30th-anniversary-of-the-world-wide-web-google-1552390014.gif'
img = instasize.resize_remote(image_url)
img.save('resized_file.png', 'PNG')
```
###### Usage - resizing local image file. 
```
image = Image.open("test_image.jpeg")
img = instasize.resize_image(image)
img.save('resized_file.png', 'PNG')
```
