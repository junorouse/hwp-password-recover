import zlib

from c import decompress_gen, decompress
from utils import gogo, pad
from password import genkey
import StringIO
import olefile
from os import _exit

from string import ascii_lowercase

from hwp import unlock_hwp

ole = olefile.OleFileIO("password_crack_test.hwp")
stream = ole.openstream("BodyText/Section0")
data = stream.read()

password = "{}bcde"
for first in ascii_lowercase:
    print first
    for second in ascii_lowercase:
        for third in ascii_lowercase:
            for fourth in ascii_lowercase:
                for fifth in ascii_lowercase:
                    ttt = password.format(first, second, third, fourth, fifth)
                    pwd = genkey(ttt)
                    docinfo = gogo(pwd, data[:16], is_encrypt=False)
                    if docinfo[0] == 'sbh':
                        print "password: {}".format(ttt)
                        unlock_hwp("password_crack_test.hwp", ttt)
                        _exit(0)