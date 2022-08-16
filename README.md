# pySympleAF

This represents a basic Python wrapper for interfacing with the [SympleAstroFocus Project](https://github.com/AlistairSymonds/SympleAstroFocus/).

It's presently in early stages but includes defined data types and bit fields, as well as converters for driver current settings and status.

## Example Usage

Refer to [demo.py](demo.py) for details on usage, but the rough summary is:

```python
with hid.Device(SAF_VID, SAF_PID) as h:
    saf = SympleAutoFocus(h.serial)

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
```