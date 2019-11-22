FROM debian:buster-slim

RUN mkdir compile
WORKDIR compile
RUN apt update

RUN apt install -y libbz2-dev libzip-dev cmake \
    git build-essential \
    git libz-dev liblzma-dev libzstd-dev wget unzip

RUN wget https://dl.bintray.com/boostorg/release/1.71.0/source/boost_1_71_0.zip && \
    unzip boost_1_71_0.zip && cd boost_1_71_0 && \
    ./bootstrap.sh && \
    ./b2 install --prefix=/usr/ && \
    cd .. && rm -r boost_1_71_0 boost_1_71_0.zip

RUN git clone https://github.com/mbrengel/memscrimper.git && \
    cd memscrimper/memscrimper_cpp_implementation && \
    mkdir build_folder && \
    pwd && cd build_folder && \
    pwd && ls -all && \
    cmake --version && \
    cmake .. && make

WORKDIR /compile/memscrimper/memscrimper_cpp_implementation/build_folder
RUN ls -all
# RUN mkdir build_folder && cd build_folder && cmake .. && make

RUN ls -all /var/run/
# RUN touch /var/run/memscrimper.sock
#ENTRYPOINT ["sh",  "./start_service.sh"]
ENTRYPOINT ["./memscrimper"]

# CMD [ ]

