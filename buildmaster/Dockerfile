FROM saichaithanya/ffmpeg-build-toolchain:v1
ENV FFMPEG_VERSION "6.0"
ENV DECODER 'aac,opus,vorbis,mjpeg,mp3'
ENV DEMUXER 'mov,matroska,image2,mp3'
ENV MUXER 'mp3,mp4,webm,null'
ENV PARSER 'vorbis,opus,vp9,vp8,aac,mjpeg,h264'
RUN mkdir /root/custom_build /root/ffmpeg_bin/ /root/ffmpeg_src /root/lame_src
RUN wget -q -nv https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.xz -O /root/ffmpeg_src.tar.xz \
  && tar xf /root/ffmpeg_src.tar.xz -C /root/ffmpeg_src --strip-components 1 \
  && rm -rf /root/ffmpeg_src.tar.xz
RUN wget -q -nv https://downloads.sourceforge.net/lame/lame-3.100.tar.gz -O /root/lame_src.tar.gz \
  && tar xf /root/lame_src.tar.gz -C /root/lame_src --strip-components 1 \
  && rm -rf /root/lame_src.tar.gz
#win-build
WORKDIR /root/lame_src
RUN ./configure --host=x86_64-w64-mingw32 --prefix=/root/custom_build \
  --disable-shared --enable-static --enable-nasm CFLAGS="-O3 -flto=4" \
  && make -j 8 \ 
  && make install \
  && make clean && make distclean
WORKDIR /root/ffmpeg_src
RUN ./configure --arch=x86_64 --target-os=mingw64 --disable-everything \
  --disable-network --disable-autodetect --enable-small --disable-debug \
  --disable-doc --disable-manpages --enable-static --disable-shared \
  --disable-podpages --disable-txtpages --disable-htmlpages \
  --enable-decoder=${DECODER} --enable-cross-compile --enable-parser=${PARSER} \
  --enable-demuxer=${DEMUXER} --enable-protocol=file --pkg-config=PKG_CONFIG_PATH \
  --enable-muxer=${MUXER} --enable-libmp3lame --enable-encoder=libmp3lame \
  --enable-filter=aresample --enable-logging --enable-w32threads --enable-lto \
  --disable-ffprobe --disable-ffplay --extra-cflags=-'I/root/custom_build/include -O3 -flto=4' \
  --cross-prefix=/root/.zeranoe/mingw-w64/x86_64/bin/x86_64-w64-mingw32- \
  --prefix=/root/custom_build --extra-ldflags=-'L/root/custom_build/lib' \
  && make -j 8 \
  && make install \
  && make clean && make distclean
RUN mv /root/custom_build/bin/ffmpeg.exe /root/ffmpeg_bin/ffmpeg_windows_amd64.exe \
  && rm -rf /root/custom_build/*
#linux-x86_64-build
WORKDIR /root/lame_src
RUN ./configure --enable-static --disable-shared --enable-nasm \
  --prefix=/root/custom_build CFLAGS="-O3 -flto" \
  && make -j 8 \ 
  && make install \
  && make clean && make distclean
WORKDIR /root/ffmpeg_src
RUN ./configure --arch=x86_64 --target-os=linux --disable-everything \
  --disable-network --disable-autodetect --enable-small --disable-debug \
  --disable-doc --disable-manpages --enable-static --disable-shared \
  --disable-podpages --enable-decoder=${DECODER} --enable-parser=${PARSER} \
  --enable-demuxer=${DEMUXER} --enable-protocol=file --disable-txtpages \
  --enable-muxer=${MUXER} --enable-libmp3lame --enable-encoder=libmp3lame \
  --enable-filter=aresample --enable-logging --enable-pthreads --enable-lto \
  --disable-ffprobe --disable-ffplay --extra-cflags=-'I/root/custom_build/include -O3 -flto=4' \
  --prefix=/root/custom_build --extra-ldflags=-'L/root/custom_build/lib' \
  --disable-htmlpages \
  && make -j 8 \
  && make install \
  && make clean && make distclean
RUN mv /root/custom_build/bin/ffmpeg /root/ffmpeg_bin/ffmpeg_linux_x86_64 \
  && rm -rf /root/custom_build/*
#linux-aarch64-build
WORKDIR /root/lame_src
RUN ./configure --host=aarch64-linux --enable-static --disable-shared \ 
  --enable-nasm --prefix=/root/custom_build CFLAGS="-O3 -flto" \
  CC=aarch64-linux-gnu-gcc CXX=aarch64-linux-gnu-g++ \
  AR=aarch64-linux-gnu-as AR=aarch64-linux-gnu-ar \
  RANLIB=aarch64-linux-gnu-ranlib STRIP=aarch64-linux-gnu-strip \
  OBJDUMP=aarch64-linux-gnu-objdump NM=aarch64-linux-gnu-nm \
  && make -j 8 \ 
  && make install \
  && make clean && make distclean
WORKDIR /root/ffmpeg_src
RUN ./configure --arch=aarch64 --target-os=linux --disable-everything \
  --disable-network --disable-autodetect --enable-small --disable-debug \
  --disable-doc --disable-manpages --enable-static --disable-shared \
  --disable-podpages --enable-decoder=${DECODER} --enable-parser=${PARSER} \
  --enable-demuxer=${DEMUXER} --enable-protocol=file --disable-txtpages \
  --enable-muxer=${MUXER} --enable-libmp3lame --enable-encoder=libmp3lame \
  --enable-filter=aresample --enable-logging --enable-pthreads --enable-lto \
  --disable-ffprobe --disable-ffplay --extra-cflags=-'I/root/custom_build/include -O3 -flto=4' \
  --prefix=/root/custom_build --extra-ldflags=-'L/root/custom_build/lib' \
  --disable-htmlpages --cross-prefix=aarch64-linux-gnu- \
  && make -j 8 \
  && make install \
  && make clean && make distclean
RUN mv /root/custom_build/bin/ffmpeg /root/ffmpeg_bin/ffmpeg_linux_aarch64 \
  && rm -rf /root/custom_build/*
#darwin-x86_64-build
WORKDIR /root/lame_src
RUN CC=x86_64-apple-darwin21.4-clang ./configure --host=x86_64-apple-darwin21.4 \
  --enable-static --disable-shared --enable-nasm \
  --prefix="/root/custom_build/" CFLAGS="-O3" \
  && make -j 8 \
  && make install \
  && make clean && make distclean
WORKDIR /root/ffmpeg_src
RUN ./configure --arch=x86_64 --target-os=darwin --enable-cross-compile \
  --disable-everything --disable-network --disable-autodetect \ 
  --enable-small --disable-txtpages  --disable-shared --enable-static \
  --enable-decoder=${DECODER} --disable-podpages --enable-parser=${PARSER} \
  --enable-demuxer=${DEMUXER} --enable-protocol=file \
  --enable-muxer=${MUXER} --enable-libmp3lame --enable-encoder=libmp3lame \
  --enable-filter=aresample --enable-logging --enable-pthreads \
  --disable-ffprobe --disable-ffplay --prefix='/root/custom_build/' \
  --extra-cflags=-"I/root/custom_build/include -O3" --disable-manpages \
  --extra-ldflags="-L/root/custom_build/lib" --disable-doc \
  --cross-prefix="/usr/local/osxcross/bin/x86_64-apple-darwin21.4-" \
  --cc="x86_64-apple-darwin21.4-clang" --disable-debug --disable-htmlpages \
  --pkg-config="/usr/local/osxcross/bin/x86_64-apple-darwin21.4-pkg-config" \
  && make -j 8 \
  && make install
RUN mv ./ffmpeg /root/ffmpeg_bin/ffmpeg_darwin_x86_64 \
  && rm -rf /root/custom_build/* && make clean && make distclean
#darwin-arm64-build
WORKDIR /root/lame_src
RUN CC=aarch64-apple-darwin21.4-clang ./configure --host=aarch64-apple-darwin21.4 \
  --enable-static --disable-shared --enable-nasm \
  --prefix="/root/custom_build/" CFLAGS="-O3" \
  && make -j 8 \
  && make install \
  && make clean && make distclean
WORKDIR /root/ffmpeg_src
RUN ./configure --arch=aarch64 --target-os=darwin --enable-cross-compile \
  --disable-everything --disable-network --disable-autodetect --enable-small \
  --disable-htmlpages --disable-shared --enable-static --disable-debug \
  --enable-decoder=${DECODER} --disable-txtpages --enable-parser=${PARSER} \
  --enable-demuxer=${DEMUXER} --enable-protocol=file \
  --enable-muxer=${MUXER} --enable-libmp3lame --enable-encoder=libmp3lame \
  --enable-filter=aresample --enable-logging --enable-pthreads \
  --disable-ffprobe --disable-ffplay --prefix='/root/custom_build/' \
  --extra-cflags=-"I/root/custom_build/include -O3" \
  --extra-ldflags="-L/root/custom_build/lib" --disable-podpages \
  --cross-prefix="/usr/local/osxcross/bin/aarch64-apple-darwin21.4-" \
  --cc="aarch64-apple-darwin21.4-clang" --disable-manpages --disable-doc \
  --pkg-config="/usr/local/osxcross/bin/aarch64-apple-darwin21.4-pkg-config" \
  && make -j 8 \
  && make install
RUN mv ./ffmpeg /root/ffmpeg_bin/ffmpeg_darwin_arm64 \
  && rm -rf /root/custom_build/* && make clean && make distclean
#android-aarch64-build
WORKDIR /root/lame_src
RUN CC=aarch64-linux-android33-clang ./configure --host=aarch64-linux-android33 \
  --enable-static --disable-shared --enable-nasm \
  --prefix="/root/custom_build/" CFLAGS="-O3 -flto" \
  && make -j 8 \
  && make install \
  && make clean && make distclean
WORKDIR /root/ffmpeg_src
RUN ./configure --arch=aarch64 --target-os=android --enable-cross-compile \
  --disable-everything --disable-network --disable-autodetect --enable-small \
  --disable-debug --disable-txtpages  --disable-shared --enable-static \
  --enable-decoder=${DECODER} --disable-htmlpages --enable-parser=${PARSER} \
  --enable-demuxer=${DEMUXER} --enable-protocol=file \
  --enable-muxer=${MUXER} --enable-libmp3lame --enable-encoder=libmp3lame \
  --enable-filter=aresample --enable-logging --enable-pthreads --disable-doc \ 
  --disable-ffprobe --disable-ffplay --prefix='/root/custom_build/' \
  --extra-cflags="-I/root/custom_build/include -O3 -I${ANDROID_INCLUDE}" --disable-manpages \
  --extra-ldflags="-L/root/custom_build/lib -L${ANDROID_LIB}" --disable-podpages \
  --cc="aarch64-linux-android33-clang" --nm=llvm-nm --strip=llvm-strip \
  && make -j 8 \
  && make install \
  && make clean && make distclean
RUN mv /root/custom_build/bin/ffmpeg /root/ffmpeg_bin/ffmpeg_android_aarch64 \
  && rm -rf /root/custom_build/*
CMD ["tail", "-f", "/dev/null"]