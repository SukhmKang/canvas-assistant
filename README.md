<img src="https://github.com/SukhmKang/canvas-assistant/blob/main/Screenshots/CanvasAssistantNavbar.png" width="600">

**Ishan Balakrishnan & Sukhm Kang**

Chrome extension that automatically gets a calendar &amp; to-do list of your Canvas assignments and finds personalized Study Buddies for you!

## File summary

```/extension``` - Simply unpack this directory in the Chrome Extension developer mode to give it a try. \
```/serverside``` - This is the Flask server backend for the Chrome Extension, which, given a Canvas API Key, generates a **.ics** file of the user's assignments, a **.csv** of the user's assignments in to-do list form, and a **.csv** of students that share multiple classes with the user. 

## Functionality

The Extension makes a ```POST``` request to the Flask server (hosted at https://canvashelper.pythonanywhere.com), which sends file data back to the Extension, which then downloads the file to the user.

<img src="https://github.com/SukhmKang/canvas-assistant/blob/main/Screenshots/Screen%20Shot%202022-03-21%20at%202.53.09%20PM.png" width="600">

## Acknowledgements

This project made extensive use of the Free version of ```Material Design for Bootstrap``` (https://mdbootstrap.com/).
