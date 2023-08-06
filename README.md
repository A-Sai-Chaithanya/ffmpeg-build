# FFmpeg Build

This project contains docker files necessary to build and test, minimal and static FFmpeg binaries with LAME encoder support for Linux, Windows, macOS and Android-Linux OS/Platforms.

### Supported OS/Platforms

 - [x] MacOS (arm64) 
 - [x] MacOS (x86_64)
 - [x] Linux (aarch64)
 - [x] Linux (x86_64)
 - [x] Windows (amd64)
 - [x] Android-Linux (aarch64)

### Folder Overview

 - **build-tools** - Dockerfile to build a docker image with all cross compilation tools needed  
Docker Hub (prebuild image) :	[saichaithanya/ffmpeg-build-toolchain](https://hub.docker.com/r/saichaithanya/ffmpeg-build-toolchain)
 - **buildmaster** - Dockerfile to build FFmpeg binaries
 - **test_files** - media test files to test the built FFmpeg binaries

### Licence
The source code of ``ffmpeg-build`` is offered under MIT license. See the ``LICENSE.txt`` for more details.

However, the binaries of ``FFmpeg`` software included with ``ffmpeg-build`` source code have a different license.

**As per FFmpeg License Compliance**:  
This software uses code of [FFmpeg](http://ffmpeg.org) licensed under the  [LGPLv2.1 ](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)and its source can be downloaded [here](http://ffmpeg.org).   
This software uses libraries from the FFmpeg project under the LGPLv2.1.


