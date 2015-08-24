File Format Overview
--------------------

A history.bin file contains a structure basically like this:

 * Data Dump 1
   - Image Collection 1
     - Image Record 1
     - Image Record 2
       ...
     - Image Data 1
     - Image Data 2
       ...
   - Image Collection 2
     - Image Record 1
     - Image Record 2
       ...
     - Image Data 1
     - Image Data 2
       ...
 * Data Dump 2
   ...

Byte order: little endian

My guess is that all the records are divided into 16 bit wide fields (`uint16_t`).
When you interprete all bytes of the image records like this, you get some nice
looking numbers (e.g. the last field in all records I saw is then "1234").

### Data Dump

	Offset  Size  Type          Description
	     0     2  uint16_t      Data dump index. Starts at 0, is incremented by
	                            1 for everye following dump.
	     2    12  char[12]      Always "DATADUMP_171". Probably some kind of
	                            file magic.
	    14    24  uint8_t[24]   ??? (the first two bytes of this block seem
	                            always to be 0)
	    38     2  uint16_t      Image collection count.
	    40    72  uint8_t[72]   ???

### Image Collection

	Offset  Size  Type          Description
	     0    10  uint8_t[10]   ???
	    10     2  uint16_t      Image count.
	    12     4  uint8_t[4]    ???

### Image Record

In theory width and height could be the other way around (all examples I got
are squares), but usually width is the first of the two.

	Offset  Size  Type          Description
	     0    18  uint8_t[18]   ???
	    18     2  uint16_t      width
	    20     2  uint16_t      ???
	    22     2  uint16_t      height
	    24     6  uint8_t[6]    ???
	    30     2  uint16_t      channles. 1 = grayscale, 3 = RGB
	    32    12  uint8_t[12]   ???

### Image

Images are just plain image data, 1 byte per channel and row after row, the way
you usually pass image data to a graphics API. This means the size of an image
in bytes is simply:

	size = width * height * channels
