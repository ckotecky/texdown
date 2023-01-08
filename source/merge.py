#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--input', default='', type=str, help='Input file path')
parser.add_argument('--output', default='', type=str, help='Output file path')
parser.add_argument('--strip_top', default=0, type=int, help='Number of lines to remove from the top')
parser.add_argument('--strip_bottom', default=0, type=int, help='Number of lines to remove from the bottom')



def main(args: argparse.Namespace):
	merged = ''


	for filename in sorted(os.listdir(args.input)):
		path = os.path.join(args.input, filename)

		if os.path.isfile(path) and os.path.splitext(path)[-1] == '.md':
			with open(path, 'r') as inFile:
				text = inFile.read()

				lines = text.splitlines()
				lines = lines[args.strip_top : len(lines) - args.strip_bottom + 1]

				text = '\n'.join(lines)

				merged += text + '\n'

	if args.output != '':
		with open(args.output, 'w') as outFile:
			outFile.write(merged)




if __name__ == '__main__':
	args = parser.parse_args([] if "__file__" not in globals() else None)

	main(args)