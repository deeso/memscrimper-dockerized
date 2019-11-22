# Docker Container for Memscrimper

Memscrimper is a proof-of-concept memory image diff'ing tool.  In short, it uses deduplication to remove null and other similar memory pages from memory.

This project provides a working service for users to compress their images down using the tool.  It creates 2 shared directories between the
docker container and the host.  One directory is used to share a Unix socket between the two systems.  This socket is used by the MSCR client to 
communicate with the `memscrimper` service running in the Docker container.  The second directory is used to share memory samples and service 
outputs between the two hosts.  


This repository includes the `docker-compose.yaml`, a `Dockerfile` to build the image, and scripts to run and communicate with `memscrimper`.


### Example usage of the main script to communicate with the service and perform memory diffing.

```
python3 main.py -copy_dumps \ # copy memory dumps to shared docker volume
                -compress \ # compress "source" memory image
                -compress_out test_dump.compress \  # compressed output filename
                -reference /path/to/reference.bin \ # reference image, used to create diff
                -source /path/to/memdump.bin # image to compress


python3 main.py -decompress \ # decompress compressed "source" memory image
                -decompress_out test_dump.decompress \  # decompressed output filename
                -reference /path/to/reference.bin \ # reference image, used to create original diff
                -source /path/to/testdump.compress # compressed image to decompress

```

## Acknowledgements

1. Daniel Weber
2. Michael Brengel and Christian Rossow, "`MemScrimper`: Time- and Space-Efficient Storage of Malware Sandbox Memory Dumps", https://github.com/mbrengel/memscrimper

