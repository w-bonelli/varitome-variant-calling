Bootstrap: docker
From: ubuntu:16.04

%labels
    Auther Angelo Williams
    Maintainer Manoj Sapkota, Wes Bonelli

%post
    apt-get update && apt-get install -y \
    software-properties-common \
    python-software-properties && \
    add-apt-repository "ppa:webupd8team/java" && \
    add-apt-repository "ppa:openjdk-r/ppa" && \
    apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gpp \
    gcc \
    git \
    make \
    openjdk-8* \
    python2.7 \
    python-dev \
    python-yaml \
    ncurses-dev \
    zlib1g-dev \
    curl \
    vim \
    wget \
    autoconf \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    gawk \
    libssl-dev \
    openjdk-7-jre-headless \
    unzip \
    python3-pip

    # git lfs
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
    apt-get install git-lfs

    # gatk
    git clone https://github.com/broadinstitute/gatk.git && \
    cd gatk && \
    ./gradlew bundle

    # sambamba
    curl -OL https://github.com/biod/sambamba/releases/download/v0.6.7/sambamba_v0.6.7_linux.tar.bz2 && \
    tar -xvf sambamba_v0.6.7_linux.tar.bz2 && \
    cp sambamba /usr/local/bin/

    # samblaster
    git clone git://github.com/GregoryFaust/samblaster.git && \
    cd samblaster && \
    make && \
    cp samblaster /usr/local/bin/

    # samtools
    curl -OL https://github.com/samtools/samtools/releases/download/1.8/samtools-1.8.tar.bz2 && \
    tar -xvf samtools-1.8.tar.bz2 && \
    cd samtools-1.8 && \
    ./configure && make && make install

    # vcftools
    git clone https://github.com/vcftools/vcftools.git && \
    cd vcftools && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make install

    # bedtools
    curl -OL https://github.com/arq5x/bedtools2/releases/download/v2.27.1/bedtools-2.27.1.tar.gz && \
    tar -xvf bedtools-2.27.1.tar.gz && \
    cd bedtools2 && \
    make && \
    cp bin/* /usr/local/bin/

    # picard
    curl -OL https://github.com/broadinstitute/picard/releases/download/2.18.5/picard.jar && \
    mv picard.jar /usr/local/bin

    # lumpy
    git clone --recursive https://github.com/arq5x/lumpy-sv && \
    cd lumpy-sv && \
    make && \
    cp bin/* /usr/local/bin/. &&

    # speedseq
    git clone --recursive https://github.com/hall-lab/speedseq && \
    cd speedseq && \
    make

    # pysam, numpy, scipy
    pip3 install --upgrade pip && \
    pip3 install pysam && \
    pip3 install numpy && \
    pip3 install scipy
