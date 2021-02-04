# Karaoke

My karaoke system at home, using [youtube-dl](https://github.com/ytdl-org/youtube-dl) and [spleeter](https://github.com/deezer/spleeter) to process the audio. **Please remember that it is only for research and educational purpose, use at your own risk!**

## Installation
- Copy config.py.example to config.py
```
$ cp config.py.example config.py
```
- Modify path to spleeter and youtube-dl binary in config.py
- Install requirements
```
$ pip install -r requirements.txt
```
- Run server
```
$ python index.py
```

## Notes
- **It is for private use and research only, not for commercial use**
- First extract takes more time, to download the pretrained model.
