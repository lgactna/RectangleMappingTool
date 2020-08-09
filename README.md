# RectangleMappingTool
RectangleMappingTool is a dedicated rectangle plotting and coordinate exporting tool. It is built on PyQt5 and packaged with [fbs](https://github.com/mherrmann/fbs).

Its intended purpose for the AACT Telemetry project is to simplify the creation of rectangular bounding regions from the [HERC course map](https://www.nasa.gov/sites/default/files/atoms/files/edu_herc-map-2020.pdf). With it, we can easily create non-overlapping regions for each obstacle and task, giving us insight on what tasks take the longest, are point-inefficient, and so on. The conversion and export functionality of the program makes defining the equivalent GPS coordinates much easier and gives us flexibility on what we can do with the data.

- [RectangleMappingTool](#rectanglemappingtool)
  - [Installation](#installation)
    - [Windows](#windows)
    - [Everywhere else](#everywhere-else)
  - [Features](#features)
    - [Rectangle drawing/artistic expression](#rectangle-drawingartistic-expression)
    - [Data representation](#data-representation)
    - [Coordinate conversion](#coordinate-conversion)
    - [Overlap detection](#overlap-detection)
    - [CSV export](#csv-export)
    - [F-string (like) export](#f-string-like-export)
    - [Customizability](#customizability)
  - [What's next?](#whats-next)
  - [Packaging](#packaging)
    - [On Python 3.8](#on-python-38)
    - [On Python 3.6+](#on-python-36)
  - [BSD license reproduction](#bsd-license-reproduction)

## Installation

### Windows
Click on [Releases](https://github.com/aacttelemetry/RectangleMappingTool/releases) for an installer of the latest version. **Do heed the warnings** - check that the install directory is exactly where you want it to be. That means clicking on "Browse" when it prompts you for the install directory and explicitly clicking on your target install location.

I'm not sure how unlucky I was when it decided (and I let it) write 6 million files totalling over 10 GB, with the installer seeming to uninstall one of my Autodesk programs and my Git settings with it...

### Everywhere else
Building on any other platform requires that you build from source, since fbs will only build an installer for the platform of the current computer - I currently only have access to a Windows installation.

This project was written with Python 3.8; however, Python 3.6+ should work (if not better than on Python 3.8 with regards to building the installer).

There are only two Python dependencies for running the app:
- PyQt5
- fbs

Clone this repo to your working directory. In the terminal of your choice, execute `fbs run`. This should open the application.

If you choose to create a virtual environment with these two dependencies installed, ensure that you have activated the virtual environment beforehand.

Please note that `drawex.py` (the original Scribble example) and `main copy.py` can be deleted - they are reference files that were not removed during development.

## Features

### Rectangle drawing/artistic expression
The core feature of RectangleMappingTool (referred to as RMT from here onward) is the ability to draw rectangles on top of an image.

### Data representation

Really, you could do the drawing part much more easily in a regular graphics program (particularly an SVG editor, where rectangles and their coordinates are obviously defined and can easily be parsed out). However, it takes additional effort to actually view such data, and it can't easily be done in real-time. This is the primary reason RMT was created - to make the data processing more direct and oriented around rectangle drawing. 

(Actually, it was because my Google searches of "rectangle drawing tool" and "coordinate mapper" and "bounding region drawer" returned either nothing useful or relatively restrictive tools that didn't fit my needs.)

RMT gives you a table and other information that updates in real-time to

### Coordinate conversion

### Overlap detection

### CSV export

### F-string (like) export

### Customizability

## What's next?
As of August 2020, RMT runs on a single Python file (importing three different pyuic-generated .ui files). It's pretty clear that it wasn't designed with another developer in mind, and the current processes for generating the table, calculating/returning overlapping rectangles, and drawing the canvas are resource-taxing due to their redundant nature. Furthermore, there is little separation of business logic and the UI, making it incredibly difficult to maintain and extend. Future development should focus on separating these concerns and reducing ambiguity throughout the code (and attempt to find a fix for the rather taxing methods used for core functionality.)

See [Issues](https://github.com/aacttelemetry/RectangleMappingTool/issues) for planned development (which may or may not happen). It outlines other issues that currently exist within the program as well as planned feature additions.

It wasn't until the final days of this project that I started looking into PyQt best practices - it finally occurred to me that *"oh, maybe having 40 methods of varying purpose and size isn't a great idea."* In other words, the code sucks.

Also it doesn't conform to PEP conventions. That'll be fixed as well someday, when I (or, someone else) comes back to this project.

## Packaging

### On Python 3.8
In order to generate an installer for RMT on Python 3.8, a great deal of duct tape is required. PyInstaller is a requirement of fbs, but the public release does not currently support Python 3.8. However, PyInstaller 4.0.dev0 *does* support Python 3.8.

1. Clone the latest [fbs repo](https://github.com/mherrmann/fbs).
2. In `requirements.txt`, remove `PyInstaller==3.4`.
3. In `setup.py`, remove `install_requires=['PyInstaller==3.4']`.
4. Install this modified version of fbs to a virtual environment (activate it, then navigate to `fbs-x.x.x`; there, run `pip install .`).
5. Install PyInstaller with `pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz`.

This should resolve any problems executing `pip freeze` or `pip installer` on Python 3.8.

### On Python 3.6+
By default, fbs will install `PyInstaller==3.4`. As of writing, fbs supports Python 3.5 and 3.6; however, the use of f-strings in this program makes 3.5 unusable. You can edit `main.py` to make it 3.5-compatible. 

I have not attempted to generate an installer or run RMT on Python 3.5+, but it should otherwise work. You may have to resolve issues on Python 3.7.

## BSD license reproduction
*This program is a modified version of the PyQt Scribble example. As such, the following notice has been reproduced:*

Copyright (C) 2013 Riverbank Computing Limited.
Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
All rights reserved.

This file is part of the examples of PyQt.

$QT_BEGIN_LICENSE:BSD$
You may use this file under the terms of the BSD license as follows:

"Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
- Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in
the documentation and/or other materials provided with the
distribution.
- Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
$QT_END_LICENSE$
