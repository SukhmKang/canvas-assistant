<img src="https://github.com/SukhmKang/canvas-assistant/blob/main/Screenshots/CanvasAssistantNavbar.png" width="600">

**Ishan Balakrishnan & Sukhm Kang**

Chrome extension that automatically gets a calendar &amp; to-do list of your Canvas assignments and finds personalized Study Buddies for you!

**Now on the Google Chrome Web Store! Check it out [here](https://chrome.google.com/webstore/detail/canvas-assistant/ikabnodlfakajogmdoojofebcejmjlll?hl=en-US)!**

## File summary

```/extension``` - Simply unpack this directory in the Chrome Extension developer mode to give it a try. \
```/serverside``` - This is the Flask server backend for the Chrome Extension, which, given a Canvas API Key sent as ```POST``` data, generates a **.ics** file of the user's assignments, a **.csv** of the user's assignments in to-do list form, and a **.csv** of students that share multiple classes with the user. 

## Functionality

The Extension makes a ```POST``` request to the Flask server (hosted at https://canvashelper.pythonanywhere.com). The Flask server makes a ```GET``` request to the Canvas API, performs various checks and reformats the data using a custom sorting algorithm that we developed and a few APIs (```icalendar``` and ```pandas```), and then sends file data back to the Extension, which then downloads the file to the user's system.

<img src="https://github.com/SukhmKang/canvas-assistant/blob/main/Screenshots/ezgif.com-gif-maker%20(4).gif" width="600">

<img src="https://github.com/SukhmKang/canvas-assistant/blob/main/Screenshots/Screen%20Shot%202022-03-21%20at%202.53.09%20PM.png" width="600">

## Authors & Contact Information

This project was authored by **Sukhm Kang** and **Ishan Balakrishnan**.

**Sukhm Kang**\
Mathematics @ The University of Chicago\
https://www.linkedin.com/in/sukhm-kang


**Ishan Balakrishnan**\
Computer Science & Business @ University of California, Berkeley\
https://www.linkedin.com/in/ishanbalakrishnan

Feel free to reach out to either one of us by email @ ishan.balakrishnan(at)berkeley.edu or sukhmkang(at)uchicago.edu! 

## Acknowledgements

This project made extensive use of the Free version of ```Material Design for Bootstrap``` (https://mdbootstrap.com/).
