![](https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white)

# Surveillance Camera

<p align="center">
  <img src="https://user-images.githubusercontent.com/54184905/110909041-ab3c9b00-8320-11eb-8f9c-13e0a1dbf602.png" />
</p>

**Want to watch what happens in your home when you are not at home?**
- Thanks to this application, you can deploy the cameras connected to your device on a public url, each individual with a username and password can access your cameras and watch your home, and individuals with sudo password can control which users can and cannot enter.

**Application detail**
- This application takes images from your device with python-opencv and these images are presented to the user on the website I wrote with python-flask, this website is deployed with ngrok so that you can access the camera images on your device via this url. In order to access the camera images, you must of course have a username and password, otherwise you cannot login and view the images, sudo password is required for new registration, and this password is in the same location as the application. The app can support up to 10 cameras, it controls and includes the cameras itself, you don't need to do anything.

**You can turn these devices into a surveillance home**
- Your personal computer, Raspberry Pi and NVIDIA Jetson Nano.

**System requirements**
- Python 3.5 (opencv, flask, flask_sqlalchemy, passlib, wtforms, flask_ngrok)

**Application video**
- [Link: click](https://user-images.githubusercontent.com/54184905/110907797-f9509f00-831e-11eb-96c9-0bb264c39128.mp4)