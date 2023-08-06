#!/usr/bin/env python3
import qrcode

BB_BLK = " "
BW_BLK = chr(0x2584)
WB_BLK = chr(0x2580)
WW_BLK = chr(0x2588)

blocksW = {
    False: {
        False: BB_BLK,
        True: BW_BLK
    },
    True: {
        False: WB_BLK,
        True: WW_BLK
    }
}

blocksB = {
    False: {
        False: WW_BLK,
        True: WB_BLK
    },
    True: {
        False: BW_BLK,
        True: BB_BLK
    }
}


def qrcode_string(data, version=1, inverse=False, frame_width=3, ansi_white=True):
    """
    Generates a QR Code from given data.

    :param data: Data to be encoded into the QR Code
    :param version: QR Code version to be used
    :param inverse: If True, swap foreground and background colors
    :param frame_width: Add a background frame of given width around the QR Code
    :param ansi_white: if True, add ANSI escape sequences to set foreground color to white. Otherwise,
    no ANSI sequences are inserted.
    :returns: a printable string containing the generated QR code
    """
    qr = qrcode.QRCode(version)
    qr.add_data(data)
    qr.make()
    if inverse:
        blocks = blocksW
    else:
        blocks = blocksB
    data = qr.modules
    width = len(data[0])
    height = len(data) + frame_width * 2
    # if frame_width == 0:
    for _ in range(frame_width):
        data.insert(0, width * [False])
        data += [width * [False]]
    data += [width * [not inverse]]
    height += 1
    output = ""
    low_part = False
    lines = []
    for i in range(height // 2):
        if i == height // 2 - 1:
            low_part = not inverse
        line = frame_width * blocks[False][low_part]
        for j in range(width):
            line += blocks[data[2 * i][j]][data[2 * i + 1][j]]
        line += frame_width * blocks[False][low_part]
        lines += [line]
    output = "\n".join(lines)
    if ansi_white:
        output = "\033[97m" + output + "\033[39m"
    return output


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option("-d", "--data",
                      action="store", type="string", dest="data", default="Hello world!",
                      help="Data to be encoded into the QR Code")

    parser.add_option("-v", "--version",
                      action="store", type="int", dest="version", default=1,
                      help="QR Code version to be used")

    parser.add_option("-f", "--frame_width",
                      action="store", type="int", dest="frame_width", default=3,
                      help="Add a background frame of given width around the QR Code")

    parser.add_option("-i", "--inverse",
                      action="store_true", dest="inverse", default=False,
                      help="Swap foreground and background colors")

    parser.add_option("-n", "--no_white",
                      action="store_true", dest="no_white", default=False,
                      help="Disable ANSI escape sequences to set foreground color to white")

    (options, args) = parser.parse_args()

    print(qrcode_string(options.data,
                        version=options.version,
                        inverse=options.inverse,
                        frame_width=options.frame_width,
                        ansi_white=not options.no_white))
    print(options.data)
