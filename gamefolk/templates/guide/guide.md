# Gamefolk's Guide to GBDK

## Preface

[GBDK] is a cross-platform compiler from C to Z80 assembly for the Nintendo
GameBoy. This tutorial assumes that you are comfortable with the command line
and the C programming language.

## Useful links

* [Pan Docs]: Extremely useful collection of technical documentation about the
  Gameboy.
* [GameBoy Programming Manual (pdf)][Programming Manual]: Complete specification
  of GameBoy registers and hardware behavior.
* [SDCC Manual]: Documentation for SDCC in the case that you would like to
  compile your code directly (that is, without use of the SDCC frontend).
* [GBDK Libraries Documentation]: Guide to GBDK library functions and various tips
* [GBDK page on GbdevWiki]: Some useful documentation of the compiler, assembler, and linker

## Installation
Before beginning, please ensure that you have installed the toolkit properly
from the link above.

There is an [AUR package] available for Arch Linux users, but the package is
unmaintained and installs binaries to the wrong directory. Use [this
PKGBUILD][PKGBUILD gist] instead.

## Gotchas

One of the main issues with GBDK is its toolchain. The compiler, lcc, doesn't
often emit errors during compilation, but the backed, SDCC, will fail miserably
when presented with the bad code. This can be very frustrating, as your program
will compile correctly yet fail. Here are a few issues that you might run into
when using GBDK:

### Beware C99 incompatibilities, use C89 if possible

When using lcc, you should write strict C89 (also known as ANSI C). While lcc
will accept many C99 constructs and GNU extensions, SDCC will not compile them
properly. This could cause parsing errors, link errors, or even segmentation
faults. Some limitations of C89 are as follows:

  * No inline variable declarations. Variables should be declared at the top of
    the function in which they reside.
  * No C++ style (`for (int i = 0;)`) for loops. Declare the index variable
    before the loop.
  * No C++ style `//` comments. Delimit all comments with `/*` and `*/`.

Consider using another C compiler such as gcc or clang to compile your code
before compiling it with lcc. I recommend using clang with the `-std=c89` and
`-pedantic` (or `-pedantic-errors`) flags to help catch bugs that stem from
compiling C99 with lcc.

*Note:* your compiler may have trouble compiling GBDK headers such as `gb/gb.h`
and complain about implicit declarations of GBDK library functions. Add the
following lines after the initial includes in that file to silence those errors.

```c
#if !defined(__LCC__) && !defined(SDCC_REVISION)
#define NONBANKED
#endif
```

### Static data should be declared `const`

Due to inefficiencies in how SDCC implements loads from ROM, static data such as
tiles and music should __always__ be declared `const`. If not, the data gets
copied into RAM *and* takes up about six times the ROM space.

### Do not use external linkage

Avoid using the `extern` keyword. SDCC does not implement external linkage
correctly, and thus will compile incorrect code and fail silently.

### Test on an accurate emulator

You should use as accurate an emulator as possible when testing your GBDK
program. I recommend [BGB]. Although it is a native Windows program, it runs
nicely under WINE. Many other documents recommend no$gmb, but this emulator does
not accurately reflect how GameBoy hardware will run your program.

### Converting images

Two programs that convert images files to GBDK-ready C code are [MegaMan_X's
GameBoy ToolKit][GBTK] (GBTK) and [PCX2GB]. GBTK allows one to choose between
several scaling and dithering algorithms and to visually manipulate the
resulting image, but does not optimize for empty space/ repeated tiles. PCX2GB
is relatively opaque but produces much smaller files. One solution to these
limitations is to use both programs:

1. Open your image with GBTK and manipulate it until you are satisfied.
2. Export the result as a BMP file.
3. Convert the BMP to a PCX with GIMP:
    * Image -> Mode -> Indexed
    * Generate optimum palette -> Convert
    * File -> Export As -> ZSoft PCX image
4. Run PCX2GB on your DOS platform of choice:
    * `pcx2gb o d myimage.pcx myimage.c myimage.map`

This will produce two files, one containing the image tile data ( `char
tiledata[]` ) and the other the tile map ( `char tilemap[]` ). You can combine
these arrays into one C source file (don't forget to replace the `char`s with
`const UBYTE`s!) and then display the image like this:

```c
disable_interrupts();
DISPLAY_OFF;
LCDC_REG = 0x01;
BGP_REG = 0xE4;
set_bkg_data(0, 255, tiledata);
set_bkg_tiles(0, 0, 20, 18, tilemap);
DISPLAY_ON;
enable_interrupts();
```

### Avoiding promotion

The GBDK compiler (lcc) assumes that expression parameters are signed, which can result in unnecessary overflow handling (promotion of variables to a larger size). To avoid this, explicitly label literals as unsigned by adding a trailing `U`:

```c
i = j+0x80U;
```

[GBDK]: http://gbdk.sourceforge.net
[BGB]: http://bgb.bircd.org
[AUR package]: http://aur.archlinux.org/packages/gbdk
[PKGBUILD gist]: https://gist.github.com/euclio/26fa5b6e76dc9f52bffd
[Pan Docs]: http://nocash.emubase.de/pandocs.htm
[Programming Manual]: http://students.washington.edu/fidelp/galp/megaguides/GameBoyProgrammingManual.pdf
[SDCC manual]: http://sdcc.sourceforge.net/doc/sdccman.pdf
[GBTK]: http://www.yvan256.net/projects/gameboy/#gbtk
[PCX2GB]: http://www.yvan256.net/projects/gameboy/#pcx2gb
[GBDK Libraries Documentation]: http://gbdk.sourceforge.net/doc/gbdk-doc.pdf
[GBDK page on GbdevWiki]: http://gbdev.gg8.se/wiki/articles/GBDK
