# HyperkinDukeBootanim
Xbox One Hyperkin Duke Controller - Info about changing bootanimation

## Demo
![Hyperkin Duke bootanimation](https://raw.githubusercontent.com/tuxuser/HyperkinDukeBootanim/master/demo_gc.gif)

## How to?
1. Disassemble controller
2. Desolder the flash chip
4. Dump the flash chip
5. Split out the FAT16 image from the flash dump
6. Copy your desired animation video to the filesystem
7. Inject the modified FAT16 image back into the flash image
8. Write the new data to flash chip
9. Resolder flash chip
11. Test functionality!
12. Assemble controller
13. Profit

PS: It might get a lot easier when SPI or UART is verified working.


## USB interface
USB VID: 0x2e24

USB PID: 0x0652

## Flash Chip

Chip used: BY25Q32A

Packaging: SOIC-8

Size: 4MB

Datasheet: http://www.trolink.cn/UploadFiles/Product/20160426174531_29979.pdf


## Dumping
MiniPro TL866II Plus supports it for parallel reading.

SPI is also an option according to the datasheet.

Heck, SoC even seems to support UART.

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
Apparently none for the FAT16 filesystem image.

## Mounting the FAT16 image for modification
### Linux/Unix
Simply use **mount** (with msdos-utils / vfat support installed ofc)
```
mkdir /tmp/fat16volume
mount image.bin /tmp/fat16volume
# Copy new bootanim
cp new_test.avi /tmp/fat16volume/test.avi
sync
# Unmount again
umount /tmp/fat16volume
```

### Windows
Use something like [OSFMount](https://www.osforensics.com/tools/mount-disk-images.html)

## Converting a video file
The original bootanimation is 7.96 seconds long, lets assume 8 seconds is also fine

In this example ffmpeg is used for the transcoding
```
ffmpeg \
  -i input.mp4 \         # Input video file
  -an \                  # Ditch audio stream
  -c:v mjpeg \           # Encode as MJPEG
  -vf "transpose=2" \    # Rotate 90 degress counter-clockwise
  -ss 00:00:02 -t 8 \    # Optional: Trim video (Start at second 2, duration of 8 seconds)
  -s 240x320 \           # Output resolution: 240x320
  -aspect 3:4 \          # Aspect ratio
  -filter:v fps=fps=25 \ # Frames per second
  test.avi               # Output filename
```
Check if resulting file looks nice and plays, then copy it into the FAT16 filesystem image.

## Credits
chron4 for providing a flashdump and doing all the hard work!
