import zlib

from utils import gogo, pad
from password import genkey
import StringIO
import olefile


def unlock_hwp(filename, password):
	if filename == '':
		return

	ole = olefile.OleFileIO(filename, write_mode=True)

	ole.write_stream("FileHeader", "48575020446f63756d656e742046696c650000000000000000000000000000000502000501000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000".decode("hex"))

	stream = ole.openstream("DocInfo")
	data = stream.read()

	pwd = genkey(password)
	docinfo = gogo(pwd, pad(data), is_encrypt=False)
	zlib.decompress(docinfo, -15)

	ole.write_stream("DocInfo", docinfo[:len(data)])

	stream = ole.openstream("BodyText/Section0")
	data = stream.read()
	body = gogo(pwd, pad(data), is_encrypt=False)

	ole.write_stream("BodyText/Section0", body[:len(data)])

