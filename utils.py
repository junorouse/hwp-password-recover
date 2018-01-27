from Crypto.Cipher import AES
from password import genkey

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(raw)

    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.decrypt(enc)


from pwn import *

pwd = "e7fe06eb0b552a1631fa8df303f8b61a".decode("hex")

pwd = "40fc1ff828306c3ab4efc6df53939455".decode("hex")

# data = open("mymem","rb").read()
# data = open("final_data","rb").read()

def gogo(pwd, data, is_encrypt=True):
    final_data = ''
    TMP_IN = bytearray(16)

    final_data = ''

    for kkk in range(0, len(data), 16):

        REAL_INPUT = bytearray(data[kkk:kkk+16])

        for i in range(128):

            OUT = AESCipher(pwd).encrypt(str(TMP_IN))

            # OUT = u32(OUT[:4])
            OUT = ord(OUT[0])

            ff = i & 7;

            if is_encrypt:
                REAL_INPUT[i>>3] ^= (OUT & 0x80) >> (i & 7);

            tmp = 1;
            for j in range(3):
                v14 = TMP_IN[tmp];

                TMP_IN[tmp-1] = ((2 * TMP_IN[tmp-1])&0xff) | (TMP_IN[tmp] >> 7);
                v15 = TMP_IN[tmp+1];
                v16 = ((2 * v14)&0xff) | (TMP_IN[tmp+1] >> 7);

                v17 = TMP_IN[tmp+2];
                TMP_IN[tmp] = v16;
                v18 = ((2 * v15)&0xff) | (v17 >> 7);

                v19 = TMP_IN[tmp+3];
                TMP_IN[tmp+1] = v18;
                v20 = ((2 * v17)&0xff) | (v19 >> 7);

                v21 = ((2 * v19)&0xff) | (TMP_IN[tmp+4] >> 7);

                TMP_IN[tmp+2] = v20;
                TMP_IN[tmp+3] = v21;

                tmp += 5;

            if is_encrypt:
                TMP_IN[15] = ((2 * TMP_IN[15])&0xff) | (REAL_INPUT[i>>3] >> (7 - ff))
            else:
                TMP_IN[15] = ((2 * TMP_IN[15])&0xff) | (REAL_INPUT[i>>3] >> (7 - ff)) & 1 

            if not is_encrypt:
                REAL_INPUT[i>>3] ^= (OUT & 0x80) >> (i & 7);

        if is_encrypt:
            final_data += str(TMP_IN)
            print str(REAL_INPUT).encode("hex")
        else:
            final_data += str(REAL_INPUT)

    return final_data


if __name__ == '__main__':
    pwd = "40fc1ff828306c3ab4efc6df53939455".decode("hex")

    # pwd = genkey(raw_input("password: ").strip())

    pwd = genkey("asdfasdf")

    # enc = gogo(pwd, pad(raw_input("input: ").strip()))
    # print "enc: ", enc.encode("hex")
    plain = gogo(pwd, open("wowmem").read(), False)
    print "plain: ", plain.encode("hex")

