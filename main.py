import os
import mscr_client_python3 as mscr_client
import argparse
import shutil

SHARED_SOCKET = '/var/run/memscrimper/ms.sock'
SHARED_LOCAL_DIRECTORY = '/data/memory_dumps'
COMPRESS_OUTNAME = 'compressed_memory_dump.compress'
DECOMPRESS_OUTNAME = 'compressed_memory_dump.decompress'
DIFFING = False
INTRADEDUP = True
PAGESIZE = 4096
COMPRESSION_FORMAT = mscr_client.Compression.GZIP

parser = argparse.ArgumentParser(description='Diff Memory with Docker.')

parser.add_argument('-shared_sock', default=SHARED_SOCKET,
                    help='shared socket')

parser.add_argument('-no_intra', action="store_true", 
                    help='No intra-deduplication')

parser.add_argument('-no_diff', action="store_true", 
                    help='No diffing')

parser.add_argument('-inner_compression', default=COMPRESSION_FORMAT, type=int,
                    help='compression of the inner pages')

parser.add_argument('-shared_dir', default=SHARED_LOCAL_DIRECTORY,
                    help='base directory')

parser.add_argument('-copy_dumps', action="store_true",
                    help='copy dumps from reference location')

parser.add_argument('-reference', default=None, type=str,
                    help='location to the memory dump locally')

parser.add_argument('-source', default=None, type=str,
                    help='location to the source memory dump locally')

parser.add_argument('-compress_out', default=COMPRESS_OUTNAME, type=str,
                    help='decompressed memory dump locally')

parser.add_argument('-decompress_out', default=DECOMPRESS_OUTNAME, type=str,
                    help='decompressed memory dump locally')

parser.add_argument('-pagesize', default=PAGESIZE, type=int,
                    help='location to the source memory dump locally')

parser.add_argument('-compress', action="store_true",
                    help='compress the memory image based on reference')

parser.add_argument('-decompress', action="store_true",
                    help='decompress the memory image based on reference')


get_shareable_file = lambda base, fname: os.path.join(base, fname)

if __name__ == "__main__":
    args = parser.parse_args()

    if args.compress and (args.reference is None or args.source is None):
        raise Exception("Must provide the reference and source dump to manipulate")
    elif args.decompress and (args.reference is None or args.source is None):
        raise Exception("Must provide the reference and source dump to manipulate")

    pagesize = args.pagesize
    compression = args.inner_compression
    ref_name = args.reference
    src_name = args.source
    cout_name = args.compress_out
    dout_name = args.decompress_out

    shared_ref_name = get_shareable_file(args.shared_dir, ref_name)
    shared_src_name = get_shareable_file(args.shared_dir, src_name)
    shared_cout_name = get_shareable_file(args.shared_dir, cout_name)
    shared_dout_name = get_shareable_file(args.shared_dir, dout_name)
    diff = not args.no_diff
    intradedup = not args.no_intra
    compress = args.compress
    decompress = args.decompress
    if args.copy_dumps:
        ref_name = os.path.split(ref_name)[-1]
        src_name = os.path.split(src_name)[-1]
        cout_name = os.path.split(cout_name)[-1]
        shared_ref_name = get_shareable_file(args.shared_dir, ref_name)
        shared_src_name = get_shareable_file(args.shared_dir, src_name)
        shared_cout_name = get_shareable_file(args.shared_dir, cout_name)
        shared_dout_name = get_shareable_file(args.shared_dir, dout_name)
        print("Copying {} to {}".format(args.reference, shared_ref_name))
        shutil.copy(args.reference, shared_ref_name)
        print("Copying {} to {}".format(args.source, shared_src_name))
        shutil.copy(args.source, shared_src_name)

    if decompress and (dout_name is None  or src_name is None):
        raise Exception("Must provide the output dump file if decompressing")

    mscr = mscr_client.MscrClient(args.shared_sock, True)
    print("Adding {} as reference dump.".format(shared_ref_name))
    # adding reference dump (for faster compression)
    mscr.add_referencedump(shared_ref_name, pagesize)

    # send compression request
    if compress:
        print("Compressing {} from reference {}, writing to {}.".format(shared_src_name, shared_ref_name, shared_cout_name))
        mscr.compress_dump(shared_ref_name, shared_src_name, shared_cout_name,
                            pagesize, intradedup, diff, compression)
    
    if decompress:
        print("Decompressing {} from reference {}, writing to {}.".format(shared_src_name, shared_ref_name, shared_dout_name))
        mscr.decompress_dump(shared_src_name, compression)

    # remove reference dump from server memory (optional)
    mscr.del_referencedump(shared_ref_name)
