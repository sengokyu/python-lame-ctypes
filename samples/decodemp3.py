from ctypes import *
from io import BufferedReader
import logging
import struct
import sys
import wave
from lame_ctypes import *

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


def read_header(src):
    pcm_buf_l = (c_short * 16384)()
    pcm_buf_r = (c_short * 16384)()
    mp3data = mp3data_struct()

    hip = hip_decode_init()

    with BufferedReader(open(src, "rb")) as fp:
        buf = fp.read(4096)

        while(len(buf) > 0):
            nout = hip_decode1_headers(
                hip,
                (ctypes.c_ubyte * len(buf)).from_buffer(bytearray(buf)),
                len(buf),
                pcm_buf_l,
                pcm_buf_r,
                byref(mp3data))

            if nout == -1:
                logging.warning("Decoding error.")

            if mp3data.header_parsed == 1:
                break

            buf = fp.read(4096)

    hip_decode_exit(hip)

    return mp3data


def decode_to(src, dst):
    pcm_buf_l = (c_short * 16384)()
    pcm_buf_r = (c_short * 16384)()

    hip = hip_decode_init()

    with BufferedReader(open(src, "rb")) as fp:
        buf = fp.read(4096)
        buf_len = len(buf)

        while(buf_len > 0):
            nout = 1

            while(nout > 0):
                nout = hip_decode1(
                    hip,
                    (ctypes.c_ubyte * buf_len).from_buffer(bytearray(buf)),
                    buf_len,
                    pcm_buf_l,
                    pcm_buf_r)

                if nout == -1:
                    logging.warning("Decoding error.")

                for r, l in zip(pcm_buf_l[:nout], pcm_buf_r[:nout]):
                    dst.writeframes(struct.pack("<h", r))
                    dst.writeframes(struct.pack("<h", l))

                # re-execute hip_docode with empty buf
                # cause decoding is incomplete
                buf_len = 0

            buf = fp.read(4096)
            buf_len = len(buf)

    hip_decode_exit(hip)


def dump_mp3data(mp3data):
    logging.debug("stereo: %s", mp3data.stereo)
    logging.debug("samplerate: %s", mp3data.samplerate)
    logging.debug("bitrate: %s", mp3data.bitrate)
    logging.debug("mode: %s", mp3data.mode)
    logging.debug("mode_ext: %s", mp3data.mode_ext)
    logging.debug("framesize: %s", mp3data.framesize)
    logging.debug("nsamp: %s", mp3data.nsamp)
    logging.debug("totalframes: %s", mp3data.totalframes)
    logging.debug("framenum: %s", mp3data.framenum)


def main(src, dst):
    lame = lame_init()

    mp3data = read_header(src)

    if mp3data.header_parsed == 1:
        logging.debug("header_parsed: succeed")
        dump_mp3data(mp3data)

        with wave.open(dst, "wb") as wf:
            wf.setnchannels(mp3data.stereo)
            wf.setsampwidth(2)  # 16bit audio
            wf.setframerate(mp3data.samplerate)

            decode_to(src, wf)
    else:
        logging.debug("header_parsed: failed")

    lame_close(lame, 1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: %s input.mp3 output.wav" % (sys.argv[0]))
        sys.exit()
    main(sys.argv[1], sys.argv[2])
