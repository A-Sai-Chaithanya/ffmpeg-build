#!/usr/bin/env bash
bin_dir=$(pwd)/tests/ffmpeg_bin
rm -rf "$bin_dir"
mkdir -p "$bin_dir"
if [[ "$(docker images -q saichaithanya/ffmpeg-build-toolchain:v1 2>/dev/null)" == "" ]]; then
	docker pull saichaithanya/ffmpeg-build-toolchain:v1
fi
if [[ "$(docker images -q ffmpeg-buildmaster:latest 2>/dev/null)" == "" ]]; then
	docker build -t ffmpeg-buildmaster ./buildmaster
fi
docker run -d -t --name=ffmpeg-buildmaster ffmpeg-buildmaster &&
	docker cp ffmpeg-buildmaster:/root/ffmpeg_bin/. "$bin_dir" &&
	docker stop ffmpeg-buildmaster &&
	docker rm -f ffmpeg-buildmaster &&
	docker rmi -f ffmpeg-buildmaster saichaithanya/ffmpeg-build-toolchain:v1 &&
	python3 "$(pwd)"/tests/test.py
