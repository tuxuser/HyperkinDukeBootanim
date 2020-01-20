# HyperkinDukeBootanim
Xbox One Hyperkin Duke Controller - Info about changing bootanimation

## USB interface
USB VID: 0x2e24
USB PID: 0x0652

## Flash Chip

Chip used: BY25Q32A

Packaging: SOIC-8

Size: 4MB

Datasheet: http://www.trolink.cn/UploadFiles/Product/20160426174531_29979.pdf


## Dumping
MiniPro TL866II Plus supports it for parallel reading
SPI is also an option according to the datasheet

## Memory content
```
0x00000000-0x0010D000 Bootloader
0x0010D000-0x00400000 FAT16 Filesystem image
```

### Bootloader
ALOT of debug strings, bootloader referenced as "GPDV" / "GP DV"

### FAT16 filesystem image
Contains a single file, **test.avi**.
```
Input #0, avi, from 'test.avi':
  Metadata:
    encoder         : Lavf57.41.100
  Duration: 00:00:07.96, start: 0.000000, bitrate: 1229 kb/s
    Stream #0:0: Video: mjpeg (MJPG / 0x47504A4D), yuvj420p(pc, bt470bg/unknown/unknown), 240x320 [SAR 1:1 DAR 3:4], 1225 kb/s, 25 fps, 25 tbr, 25 tbn, 25 tbc
```

### Checksums
Unknown

## Credits
chron4 for providing a flashdump and gettin me interested
