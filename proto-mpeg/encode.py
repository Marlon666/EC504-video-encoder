import argparse
import proto_mpeg_x
from os import listdir
import sys

def main():

    parser = argparse.ArgumentParser(description='EC504 proto-mpeg encoder. At minimum, you must specify files to encode either through --dir or --files arguments.')
    parser.add_argument('--out', nargs=1, default='output.bin', help='filename of encoded file. default is output.bin')
    parser.add_argument('--dir', nargs=1, help='directory from which to source files. Filenames will be encoded in sorted filename order')
    parser.add_argument('--alg', nargs=1, choices=['n', 'fd', 'bm'], default='n', help='temporal compression algorithm. n=none; fd=frame difference; bm=block matching. Default is none.')
    parser.add_argument('--qf', nargs=1, type=int, choices=[1, 2, 3, 4], default=1, help='quantization factor for HF suppression. Default is 1.')
    parser.add_argument('--limit', nargs=1, type=int, help='cap the number of images that will be encoded. Default is all files.')
    parser.add_argument('--files', nargs=argparse.REMAINDER, help='files to encode. Ignored if a directory is specified.')

    if (len(sys.argv[1:])) == 0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()

    #print("input arguments:", args)

    # Handle output filename argument
    if args.out == None:
        outname = 'output.bin'
    else:
        outname = args.out[0]

    # Handle source location
    if args.dir == None:
        if args.files == None:
            print("No files specified.")
            return
        else:
            files = args.files
    else:
        filenames = sorted(listdir(args.dir[0]))
        files = [args.dir[0] + fname for fname in filenames]

    # Handle number of files
    if args.limit != None and len(files) > args.limit[0]:
        files = files[:args.limit[0]]

    # Capture algorithm
    if args.alg[0]=='n':
        method='none'
    elif args.alg[0]=='fd':
        method='frame_difference'
    elif args.alg[0]=='bm':
        method='block_matching'

    print("Encoding", len(files), "files into", outname, "with motion algorithm", method, "and QF", args.qf)
    proto_mpeg_x.encodeVideo(outname, files, mot_est=method, QF=args.qf)

if __name__ == "__main__":
    main()