import hid
from pySympleAF import SympleAutoFocus, SAF_VID, SAF_PID, SAF_GUID_1, SAF_FIRMWARE_COMMIT_ID, SAF_PACKET_BYTES, SAF_ENDIAN

from pySympleAF.exceptions import SympleAFUninitialisedValue

# https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
def grouped(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return zip(*[iter(iterable)]*n)


READ_SIZE = 1024
READ_TIMEOUT = 5

with hid.Device(SAF_VID, SAF_PID) as h:
    saf = SympleAutoFocus(h.serial)

    print(f'Device manufacturer: {h.manufacturer}')
    print(f'Product: {h.product}')
    print(f'Serial Number: {h.serial}')

    read_command = (SAF_GUID_1 & 0x7FFFFFFF)
    read_command_int = read_command.to_bytes(SAF_PACKET_BYTES, SAF_ENDIAN)

    h.write(read_command_int)

    while True:

        this_read = h.read(READ_SIZE, timeout=READ_TIMEOUT)

        for this_packet in grouped(this_read, 8):
            saf.handle_packet(this_packet)

        try:
            print(saf.driver_status, saf.target_position, saf.max_position, saf.command_status, saf.driver_type)
        except SympleAFUninitialisedValue:
            pass



