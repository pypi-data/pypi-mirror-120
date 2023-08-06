from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='ASvid',
   version='0.0.1',
   description='A useful module for image to video converision',
   license="ASHIK-SAMIN-KUET-BD",
   long_description='This module provide functional support to convert image to video on the basis of spoken word, helpful for real time voice to video generation using images',
   author='Ashikur Rahman',
   author_email='ash.rahman.cse@gmail.com',
   url="https://github.com/Ashik-90/Speech-to-Sign-Language-Translator-Application",
   packages=['ASvid'],
   install_requires=['datetime', 'cv2', 'glob','shutil', 'os','PIL', 'speech_recognition'], 
   keywords=['python', 'image', 'video', 'sign language'],
   classifiers=[
      "Intended Audience :: Developers",
      "Programming Language :: Python :: 3",
      "Operating System :: Unix",
      "Operating System :: MacOS :: MacOS X",
      "Operating System :: Microsoft :: Windows",
   ]
)