# Automatic Speech Recognition

This repository contains the implementation of an Automatic Speech Recognition system in python, using a client-server architecture with Web Sockets.

If you want to know the explanation, I leave you the link to my video on YouTube.
<a href="https://youtu.be/gdSUyI1z50o">YouTube: Speech Recognition in Your PC</a>

## 1. Files

- The `docs` directory the list of resources used for this project.
- The `client.py` script defines the client websocket. It handles stuff related to recognizing mic, setting audio features, etc.
- The `server.py` script defines the server websocket. It handles stuff related to loading Speech Recognition Models, inference, etc.

## 2. The architecture

<p align="center">
<img src='img/asr.jpg'>
</p>

## 3. Dependencies

In order to install the correct versions of each dependency, it is highly suggested to work under a virtual environment. In this case, I'm using the `pipenv` environment. To install the dependencies you just need type:

```
pipenv install -r requirements.txt
```

then, in order to lauch the environment you would need to type:

```
pipenv shell
```

## 4. How to use

Once you have correctly installed the requirements. You must set in line `17` of `client.py` your input device. In my case, my device is defined as `INPUT_DEVICE = "UMC204HD 192k"

### Server

First, you need to launch the server. My recommendation is to use one terminail (or session) for the server. You can also run the server in background.

```
$ python -B server.py -l [EN | ES]
```

### Client

Then, you will be able to lauch the client.

```
$ python -B client.py
```

## 5. Comments

Any comment, suggestion or colaboration, just reach me out at: fer.neutron@gmail.com

Feel free to clone or fork!
