# Pixly Task List:
Home base for ongoing pixly work


## Flask Backend Todos:
### General app.py stuff:

1. move all helper functions back to separate .py file.
2. create file to hold filter functions
3. create file to hold S3 functions - (client_s3 function may need to remain in app.py due to circular export errors.)
4. think about adding a config file to hold s3 and other config settings.
        
        
### Routes:

1. Work on /images/edit so it can handle various edit requests
 
 
### Functionality:
 
1. Implement temp file module to keep image editing in memory, not on disk. - (I think)
2. Add code for additional filters & features
    - B&W filter
    - borders
    - cropping
    - thumbnails for display
    - more to come...

3. Reduce WTForms model to only be for CSRF protection? Are the other features needed now that we have React?
4. Remove jinja templates


<hr>


## React Frontend Todos:

1. Clean up any unused code/components.
2. Aim to, generally, build feature on the backend, then build component to fit.


<hr>


## Roadmap
Develop a mvp plan: high level plan for *minimum viable product*
    - what features we need.
    - how each one will be implemented.
    - we can come back to update the plan as we learn more.
    - add additional fun stuff to stretch goals.


1 for filters, I think we could easily pre-render several versions of the image, send them all to the front end, and let the user toggle between them.  However, if we want to implement sliders... we'll need to experiment to see if that's workable using ajax, or if we need to do frontend algorithms.
    - If we do front end, this tutorial looks super reasonable:
    - https://hackernoon.com/understanding-basic-image-processing-algorithms-a-hands-on-javascript-tutorial-8r3u32qk
2. Once we get the filters all hooked up, we can see how quickly flask can process and return an image. If it's not *very* quick then lets probaly lean into a combination of prerendering some things, like filtered images, and doing other things, like RGB sliders, in the browser?


## Stretch Goals
Thinking we can set phase 1 goals in the roadmap section, and then start adding phase 2 ideas here that we can implement once we have all the core features in place.

- user system to see your personal images?



# Research
(list any topics needing additional research)
1. Look into github's ticket system, may be a good way to streamline tasks.
2. Python's Temp File library
