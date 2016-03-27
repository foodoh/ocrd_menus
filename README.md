## OCR'd menus

#### Approach1: User Tesseract OCR

We have used `tesseract` as the OCR engine.

Further more we have divided the images to 

|   |    |
|:--:|:--:|
|dark colored | light colored |

Which allows us to tweak us the OCR algorithm accordingly and help it perform better


#### Approach2: free-ocr.com

Used selenium to automate the interaction with free-ocr.com. Has been giving better results
than the previous method.

**Note**: 

_Requirements for that_: `$ pip install selenium`

- Implemented in `free_ocr_selenium.py` 

_`processed_files.sh`_: shows the ratio of menu images and the processed files in dir. (To keep track of things!)

## Packages inside

**rmgarbage**
    Implements the various rules presented in the paper [_Automatic Removal of “Garbage Strings” in OCR Text: An Implementation_](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.8901) which helps us decide whether a string is a valid one or garbage.
