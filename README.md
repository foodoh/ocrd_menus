## OCR'd menus

We have used `tesseract` as the OCR engine.

Further more we have divided the images to 

|   |    |
|:--:|:--:|
|dark colored | light colored |

Which allows us to tweak us the OCR algorithm accordingly and help it perform better

### Packages inside

**rmgarbage**
    Implements the various rules presented in the paper [_Automatic Removal of “Garbage Strings” in OCR Text: An Implementation_](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.8901) which helps us decide whether a string is a valid one or garbage.