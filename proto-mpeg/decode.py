import argparse
import proto_mpeg_x
import sys

def main():

    parser = argparse.ArgumentParser(description='EC504 proto-mpeg decoder')
    parser.add_argument('input', nargs=1, help='file to be decoded')

    args = parser.parse_args()

    # Print help if no arguments are given
    if (len(sys.argv[1:])) == 0:
        parser.print_help()
        parser.exit()

    print("Decoding file", args.input[0])

    proto_mpeg_x.playVideo(args.input[0], realTime=False, delay=0.04)

if __name__ == "__main__":
    main()