#!/usr/bin/python

import os.path
from os.path import join as pjoin
import sys
import struct
from PIL import Image

FILE_HDR_FMT = '<' + 'H12sH' + 'H' * 48
RECORD_FMT   = '<' + 'H' * 22

H_MAGIC       =  1
H_COLLECTIONS = 14

I_WIDTH    =  9
I_HEIGHT   = 11
I_CHANNELS = 15

def log(msg=''):
	sys.stdout.write(msg+'\n')

def read_collection(fp):
	hdr = fp.read(16)
	count, = struct.unpack('<H',hdr[10:12])
	# TODO: find out what the other fields are about
	records = []
	for i in range(count):
		data = fp.read(44)
		record = struct.unpack(RECORD_FMT,data)
		records.append(record)
	return hdr, records

def dumpimgs(filename,outdir):
	sum_coll_count = 0
	file_count     = 0
	img_count      = 0
	fsize = os.path.getsize(filename)

	with open(filename,"rb") as fp:
		while True:
			offset = fp.tell()
			file_hdr_data = fp.read(112)
			
			if not file_hdr_data:
				break

			file_hdr = struct.unpack(FILE_HDR_FMT, file_hdr_data)
			magic = file_hdr[H_MAGIC]

			if magic != b'DATADUMP_171':
				raise ValueError('illegal file magic at offset %d: %r' % (offset, magic))

#			if file_hdr[0] != file_count:
#				raise ValueError("it's not the file index (offset = %d, value = %d, file_count = %d)" % (offset, file_hdr[0], file_count))

			file_count += 1

			coll_count = file_hdr[H_COLLECTIONS]
			sum_coll_count += coll_count

			log("[offset %d] sub-file %d with %d collections:" % (offset, file_count, coll_count))

			for coll in range(coll_count):
				offset = fp.tell()
				hdr, records = read_collection(fp)

				log("[offset %d] sub-file %d collection %d with %d images:" % (offset, file_count, coll+1, len(records)))
	
				for i, record in enumerate(records):
					img_count += 1

					width    = record[I_WIDTH]
					height   = record[I_HEIGHT]
					channels = record[I_CHANNELS]
	
					if channels == 1:
						mode = 'L'
					elif channels == 3:
						mode = 'RGB'
					else:
						raise ValueError('illegal value for channels: %d' % channels)

					offset = fp.tell()
					imgname = pjoin(outdir,"file%02d_coll%02d_img%02d_off%d_%s_%dx%d.png" % (file_count, coll+1, i+1, offset, mode.lower(), width, height))
					log(imgname)
					data = fp.read(width * height * channels)
					img = Image.frombuffer(mode,(width,height),data,'raw',mode,0,1)
					img.save(imgname)
				log()
			log()

	log("sub-file count: %d" % file_count)
	log("collection count: %d" % sum_coll_count)
	log("image count: %d" % img_count)

if __name__ == '__main__':
	filename = sys.argv[1]

	if len(sys.argv) > 2:
		outdir = sys.argv[2]
	else:
		outdir = "."

	dumpimgs(filename, outdir)
