# JSONShower

The JSONViewer allows Jupyter Notebook users to quickly view JSONs as if they were 
tables. They are able to display images, audio files and even highlight fields 
all in 1 function call. 

## How to install 

You can clone and install the repository using:

```
pip install jsonshower
```

## How to use

```
from jsonshower import show_json

docs = [
    {
        "images.image_url": "https://imgs.xkcd.com/comics/voting.png",
        "key": "This is strange",
        "value": "strange"
    },
    {
        "images.image_url": "https://imgs.xkcd.com/comics/animal_songs.png"
    }
]

show_json(
    docs, 
    image_fields=["images.image_url"], # Image fields
    audio_fields=[], # Audio fields,
    text_fields=[], # Text fields
    chunk_image_fields=[],# Images to display in the same row
    highlight_fields={"key": ["value"]}, # Fields to highlight.
    image_width=200, # Adjust the image width
)
```

Note: The fields also support indexing (for example - if you write 'images.image_url.0', it will get the first element of the array if it is there)

![image](example.png)

We also have supported multiple highlighting. It uses a reverse-sorted algorithm hinged on Python's native built-in stable sort. On top of this algorithm, it also enables counters.

![image2](multiple_color_highlighting.PNG)

## Preview PDFs from JSONs

```{python}
from jsonshower.pdfs import show_pdf_from_json 

def show_pdf_from_json(
    results, 
    pdf_field='pdf_url', # Field in JSONs
    include_bounding_box: bool=True, # Whether to include bounding box
    pre_show_hook=None, # function to run on each result before showing PDF page
    autodelete_images=True, # Delete image files used for rendering
    pdf_image_size=800, # pdf image size
    stroke_color=(1, 0, 0), # Color of PDF bounding box
    stroke_width=1, # width of border
    return_images=False #Whether to return the list of images or not
    )

```
