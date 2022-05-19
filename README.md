# WIP: Pix.ly - Image Editing and Cloud Storage

## Description

Add to description once core functionality is in place:
  - Flask Server
  - Python image editing
  - React frontend
  - S3 file storage
  - text & exif data search.

## Getting Started

### Installing Dependencies

```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip3 install -r requirements.txt
```

### Running the app

Run `seed.py` file directly to create database tables:

```
$ python3 seed.py
```

You only need to do this once, unless you change your model definitions.

Then run the app itself:

```
$ flask run -p 5001
```

Visit [http://localhost:5001/](http://localhost:5001/) in your browser to see the results.
`
## Future
1. Additional editing features
2. More interactive image UI:
    - delete, download, edit overlay
4. Improved search capabilities.


## Acknowledgments

Inspiration, code snippets, etc.
Sepia Filter - add url to sepia author
