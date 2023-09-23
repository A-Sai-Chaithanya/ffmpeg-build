FROM ubuntu:latest

ENV ANDROID_NDK_VERSION=25c
ENV PATH="$PATH:/root/.zeranoe/mingw-w64/x86_64/bin:/usr/local/osxcross/bin"
ENV PATH="$PATH:/android-ndk-r${ANDROID_NDK_VERSION}/toolchains/llvm/prebuilt/linux-x86_64/bin/"
ENV PKG_CONFIG_PATH="/root/.zeranoe/mingw-w64/x86_64/x86_64-w64-mingw32/lib/pkgconfig"
ENV ANDROID_LIB="/android-ndk-r${ANDROID_NDK_VERSION}/toolchains/llvm/prebuilt/linux-x86_64/lib64/"
ENV ANDROID_INCLUDE="/android-ndk-r${ANDROID_NDK_VERSION}/toolchains/llvm/prebuilt/linux-x86_64/include/"

RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update \
  && apt-get upgrade -y \
  && apt-get autoremove -y \
  && apt-get install --reinstall ca-certificates -y \
  && update-ca-certificates -y \
  && apt-get install build-essential nasm git wget curl make flex \
  gcc-aarch64-linux-gnu binutils-aarch64-linux-gnu bison texinfo \
  uuid-dev libxml2-dev libssl-dev patch tar bzip2 python3 python3-dev \
  sed cpio libbz2-dev zlib1g-dev gzip libarchive-tools cmake unzip -y \
  && rm -rf /var/lib/apt/lists/*
RUN git clone 'https://github.com/Zeranoe/mingw-w64-build.git' \
  && chmod 744 /mingw-w64-build/mingw-w64-build \
  && /mingw-w64-build/mingw-w64-build x86_64 \
  && rm -rf /mingw-w64-build ~/.cache/ /tmp/* \
  && cp /root/.zeranoe/mingw-w64/x86_64/libexec/gcc/x86_64-w64-mingw32/12.3.1/liblto_plugin.la \
  /root/.zeranoe/mingw-w64/x86_64/libexec/gcc/x86_64-w64-mingw32/12.3.1/liblto_plugin.so \
  /root/.zeranoe/mingw-w64/x86_64/lib/bfd-plugins/
RUN git clone 'https://github.com/tpoechtrager/osxcross.git' \
  && wget -q -nv -P /osxcross/tarballs/ 'https://github.com/alexey-lysiuk/macos-sdk/releases/download/12.3/MacOSX12.3.tar.xz' \
  && UNATTENDED=1 /osxcross/build_clang.sh && make -C "/osxcross/build/build_stage" install \
  && TARGET_DIR=/usr/local/osxcross UNATTENDED=1 /osxcross/build.sh \
  && rm -rf /osxcross /tmp/* ~/.cache/
RUN wget -q -nv "https://dl.google.com/android/repository/android-ndk-r${ANDROID_NDK_VERSION}-linux.zip" \
  && unzip /android-ndk-r${ANDROID_NDK_VERSION}-linux.zip \
  && rm -f /android-ndk-r${ANDROID_NDK_VERSION}-linux.zip