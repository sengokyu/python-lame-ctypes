from ctypes import *
from enum import Enum
from ._dll import dll
from ._stdarg_ctypes import *

_dll = dll("LAME",
           {
               "win32": ["lame"],
               "cli": ["lame"],
               "darwin": ["libmp3lame"],
               "DEFAULT": ["libmp3lame"]
           })
_bind = _dll.bind_function


lame_report_function = CFUNCTYPE(
    c_void_p, c_char_p, va_list)


class vbr_mode(Enum):
    vbr_off = 0
    vbr_mt = 1              # obsolete, same as vbr_mtrh
    vbr_rh = 2
    vbr_abr = 3
    vbr_mtrh = 4
    vbr_max_indicator = 5   # Don't use this! It's used for sanity checks.
    vbr_default = vbr_mtrh  # change this to change the default VBR mode of LAME


class MPEG_mode(Enum):
    """
    MPEG modes
    """
    STEREO = 0
    JOINT_STEREO = 1
    DUAL_CHANNEL = 2  # LAME doesn't supports this!
    MONO = 3,
    NOT_SET = 4,
    MAX_INDICATOR = 5  # Don't use this! It's used for sanity checks.


class Padding_type(Enum):
    """
    Padding types
    """
    PAD_NO = 0
    PAD_ALL = 1
    PAD_ADJUST = 2
    PAD_MAX_INDICATOR = 3  # Don't use this! It's used for sanity checks.


class preset_mode(Enum):
    """
    presets
    """
    # /*values from 8 to 320 should be reserved for abr bitrates*/
    # /*for abr I'd suggest to directly use the targeted bitrate as a value*/
    ABR_8 = 8
    ABR_320 = 320

    V9 = 410   # Vx to match Lame and VBR_xx to match FhG
    VBR_10 = 410
    V8 = 420
    VBR_20 = 420
    V7 = 430
    VBR_30 = 430
    V6 = 440
    VBR_40 = 440
    V5 = 450
    VBR_50 = 450
    V4 = 460
    VBR_60 = 460
    V3 = 470
    VBR_70 = 470
    V2 = 480
    VBR_80 = 480
    V1 = 490
    VBR_90 = 490
    V0 = 500
    VBR_100 = 500
    # still there for compatibility
    R3MIX = 1000
    STANDARD = 1001
    EXTREME = 1002
    INSANE = 1003
    STANDARD_FAST = 1004
    EXTREME_FAST = 1005
    MEDIUM = 1006
    MEDIUM_FAST = 1007


class asm_optimizations(Enum):
    """
    asm optimizations
    """
    MMX = 1
    AMD_3DNOW = 2
    SSE = 3


class Psy_model(Enum):
    """
    psychoacoustic model
    """
    PSY_GPSYCHO = 1
    PSY_NSPSYTUNE = 2


class buffer_constraint(Enum):
    """
    buffer considerations
    """
    MDB_DEFAULT = 0,
    MDB_STRICT_ISO = 1,
    MDB_MAXIMUM = 2


class lame_global_struct(Structure):
    pass


lame_global_flags = lame_global_struct
lame_t = POINTER(lame_global_flags)

"""
/***********************************************************************
 *
 *  The LAME API
 *  These functions should be called, in this order, for each
 *  MP3 file to be encoded.  See the file "API" for more documentation
 *
 ***********************************************************************/
"""

"""
/*
 * REQUIRED:
 * initialize the encoder.  sets default for all encoder parameters,
 * returns NULL if some malloc()'s failed
 * otherwise returns pointer to structure needed for all future
 * API calls.
 */
lame_global_flags * CDECL lame_init(void);
"""
lame_init = _bind("lame_init", returns=lame_t)

"""
/*
 * REQUIRED:
 * sets more internal configuration based on data provided above.
 * returns -1 if something failed.
 */
int CDECL lame_init_params(lame_global_flags *);
"""
lame_init_params = _bind("lame_init_params", [lame_t], c_int)


"""
/*
 * REQUIRED:
 * final call to free all remaining buffers
 */
int  CDECL lame_close (lame_global_flags *);
"""
lame_close = _bind("lame_close", [lame_t], c_int)

"""
/* 1=decode only.  use lame/mpglib to convert mp3/ogg to wav.  default=0 */
int CDECL lame_set_decode_only(lame_global_flags *, int);
int CDECL lame_get_decode_only(const lame_global_flags *);
"""
lame_set_decode_only = _bind(
    "lame_set_decode_only",
    [lame_t, c_int], c_int)
lame_get_decode_only = _bind(
    "lame_get_decode_only",
    [lame_t], c_int)

"""
/*********************************************************************
 *
 * decoding
 *
 * a simple interface to mpglib, part of mpg123, is also included if
 * libmp3lame is compiled with HAVE_MPGLIB
 *
 *********************************************************************/

struct hip_global_struct;
typedef struct hip_global_struct hip_global_flags;
typedef hip_global_flags *hip_t;


typedef struct {
  int header_parsed;   /* 1 if header was parsed and following data was
                          computed                                       */
  int stereo;          /* number of channels                             */
  int samplerate;      /* sample rate                                    */
  int bitrate;         /* bitrate                                        */
  int mode;            /* mp3 frame type                                 */
  int mode_ext;        /* mp3 frame type                                 */
  int framesize;       /* number of samples per mp3 frame                */

  /* this data is only computed if mpglib detects a Xing VBR header */
  unsigned long nsamp; /* number of samples in mp3 file.                 */
  int totalframes;     /* total number of frames in mp3 file             */

  /* this data is not currently computed by the mpglib routines */
  int framenum;        /* frames decoded counter                         */
} mp3data_struct;

/* required call to initialize decoder */
hip_t CDECL hip_decode_init(void);
/* With that you don't have to care about MP3 encoder/decoder delay
   anymore. Only available with libmpg123 (returns NULL otherwise). */
hip_t CDECL hip_decode_init_gapless(void);

/* cleanup call to exit decoder  */
int CDECL hip_decode_exit(hip_t gfp);

/* HIP reporting functions */
void CDECL hip_set_errorf(hip_t gfp, lame_report_function f);
void CDECL hip_set_debugf(hip_t gfp, lame_report_function f);
void CDECL hip_set_msgf  (hip_t gfp, lame_report_function f);
"""


"""
/*********************************************************************
 *
 * decoding
 *
 * a simple interface to mpglib, part of mpg123, is also included if
 * libmp3lame is compiled with HAVE_MPGLIB
 *
 *********************************************************************/
"""


class hip_global_struct(Structure):
    pass


hip_global_flags = hip_global_struct
hip_t = POINTER(hip_global_flags)


class mp3data_struct(Structure):
    _fields_ = [
        # 1 if header was parsed and following data was computed
        ("header_parsed", c_int),
        ("stereo", c_int),      # number of channels
        ("samplerate", c_int),  # sample rate
        ("bitrate", c_int),     # bitrate
        ("mode", c_int),        # mp3 frame type
        ("mode_ext", c_int),   # mp3 frame type
        ("framesize", c_int),   # number of samples per mp3 frame
        # this data is only computed if mpglib detects a Xing VBR header
        ("nsamp", c_ulong),     # number of samples in mp3 file.
        ("totalframes", c_int),  # total number of frames in mp3 file
        # This data is not currently computed by the mpglib routines
        ("framenum", c_int)    # frames decoded counter
    ]


hip_decode_init = _bind("hip_decode_init", returns=hip_t)
hip_decode_exit = _bind("hip_decode_exit", [hip_t], c_int)
hip_set_errorf = _bind("hip_set_errorf", [hip_t, lame_report_function])
hip_set_debugf = _bind("hip_set_debugf", [hip_t, lame_report_function])
hip_set_msgf = _bind("hip_set_msgf", [hip_t, lame_report_function])

"""
/*********************************************************************
 * input 1 mp3 frame, output (maybe) pcm data.
 *
 *  nout = hip_decode(hip, mp3buf,len,pcm_l,pcm_r);
 *
 * input:
 *    len          :  number of bytes of mp3 data in mp3buf
 *    mp3buf[len]  :  mp3 data to be decoded
 *
 * output:
 *    nout:  -1    : decoding error
 *            0    : need more data before we can complete the decode
 *           >0    : returned 'nout' samples worth of data in pcm_l,pcm_r
 *    pcm_l[nout]  : left channel data
 *    pcm_r[nout]  : right channel data
 *
 *********************************************************************/
int CDECL hip_decode( hip_t           gfp
                    , unsigned char * mp3buf
                    , size_t          len
                    , short           pcm_l[]
                    , short           pcm_r[]
                    );

/* same as hip_decode, and also returns mp3 header data */
int CDECL hip_decode_headers( hip_t           gfp
                            , unsigned char*  mp3buf
                            , size_t          len
                            , short           pcm_l[]
                            , short           pcm_r[]
                            , mp3data_struct* mp3data
                            );

/* same as hip_decode, but returns at most one frame */
int CDECL hip_decode1( hip_t          gfp
                     , unsigned char* mp3buf
                     , size_t         len
                     , short          pcm_l[]
                     , short          pcm_r[]
                     );

/* same as hip_decode1, but returns at most one frame and mp3 header data */
int CDECL hip_decode1_headers( hip_t           gfp
                             , unsigned char*  mp3buf
                             , size_t          len
                             , short           pcm_l[]
                             , short           pcm_r[]
                             , mp3data_struct* mp3data
                             );

/* same as hip_decode1_headers, but also returns enc_delay and enc_padding
   from VBR Info tag, (-1 if no info tag was found) */
int CDECL hip_decode1_headersB( hip_t gfp
                              , unsigned char*   mp3buf
                              , size_t           len
                              , short            pcm_l[]
                              , short            pcm_r[]
                              , mp3data_struct*  mp3data
                              , int             *enc_delay
                              , int             *enc_padding
                              );
"""
hip_decode = _bind(
    "hip_decode",
    [
        hip_t,
        POINTER(c_ubyte),
        c_size_t,
        POINTER(c_short),
        POINTER(c_short)
    ],
    c_int)

hip_decode_headers = _bind(
    "hip_decode_headers",
    [
        hip_t,
        POINTER(c_ubyte),
        c_size_t,
        POINTER(c_short),
        POINTER(c_short),
        POINTER(mp3data_struct)
    ],
    c_int)

hip_decode1 = _bind(
    "hip_decode1",
    [
        hip_t,
        POINTER(c_ubyte),
        c_size_t,
        POINTER(c_short),
        POINTER(c_short)
    ],
    c_int)

hip_decode1_headers = _bind(
    "hip_decode1_headers",
    [
        hip_t,
        POINTER(c_ubyte),
        c_size_t,
        POINTER(c_short),
        POINTER(c_short),
        POINTER(mp3data_struct)
    ],
    c_int)
