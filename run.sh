#!/bin/bash

mkdir -p images
IMAGEIO_FFMPEG_EXE=ffmpeg python scrape.py "$@"