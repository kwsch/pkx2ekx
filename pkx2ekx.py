# pkx2ekx
# Spits out an encrypted PKX with Party Data included; heavy use of Ceol's code.
from __future__ import with_statement
print "PKX to EKX\nBy Kaphotics.\n"
import os,sys,struct
from array import array
from rng import Prng

# Functions
def _unpack(data):

    ev = struct.unpack('<L', data[:4])[0]
    chksum = struct.unpack('<H', data[6:8])[0]

    return (ev, chksum, data[8:232])
def _shuffle(ec, data):
	# Create the blocks of data using its length.
	blocksize = len(data) / 4
	blocks = [
		data[:(blocksize * 1)],
		data[(blocksize * 1):(blocksize * 2)],
		data[(blocksize * 2):(blocksize * 3)],
		data[(blocksize * 3):],
	]
	
	# The shift value is derived from the PV
	shiftval = ((ec >> 0xD) & 0x1F) % 24
    
	blockorder = [
		shiftval / 6,
		(shiftval % 6) / 2,
		(shiftval % 6) % 2,
		0,
	]
    
	shuffledblocks = []
    
	# Grab the correct block according to the block order.
	for block in blockorder:
		shuffledblocks.append(blocks.pop(block))
    
	shuffledblocks = ''.join(shuffledblocks)

	return shuffledblocks
def _crypt(seed, data, obj=Prng):

	data = array('H', data)
	lc = obj(seed)

	new_data = array('H')
	for word in data:
		new_data.append(word ^ lc.advance())
    
	return new_data.tostring()
def encrypt(data):
	(ec, chksum, box_data) = _unpack(data)

	box_data = _shuffle(ec, box_data)
	box_data = _crypt(ec, box_data)

	return _pack(ec, chksum, box_data)
def _pack(ec, chksum, box_data):
	chunks = [
		struct.pack('<L', ec),
		'\x00\x00',
		struct.pack('<H', chksum),
		box_data,
	]
	return ''.join(chunks)
def printspacer():
	print "/*------------------*/\n"
def main(inputpk):
	if True == True:
		newekx = os.path.splitext(inputpk)[0] + ".ekx"
		with open(inputpk,'rb') as f:
			with open(newekx,'wb') as g:
				g.write(encrypt(f.read()))

# Process Drag&Drop
del sys.argv[0]
for item in sys.argv:
	printspacer()
	print "Converting Drag&Drop File:\n%s" % (item)
	main(item)
# Process Manual Input
go=1
while go==1:
	printspacer()
	inputpk = raw_input("Instructions: Drag & Drop PKM File into the window, then press Enter.\nFile: ").replace('"', '')
	print ""
	main(inputpk)
	print ""
	if raw_input("Process another? (y/n): ") != "y":
		go=0
		print ""
		raw_input("Press Enter to Exit.")
		break
		
#eof