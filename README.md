# AmIptvPlayer

A simple IPTV player written in python wit gtk

## Requirements

* python3.6+
* pygtk3+
* vlc

## Install
### Linux (Distro with apt as package manager ex. Ubuntu, Linux Mint)
```bash
apt-get install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0
apt-get install vlc
```

### Windows

[PyGobect](https://pygobject.readthedocs.io/en/latest/getting_started.html#windows-getting-started)

1. Go to [msys2](http://www.msys2.org/) and download the x86_64 installer
2. Follow the instructions on the page for setting up the basic environment
3. Run C:\msys64\mingw64.exe - a terminal window should pop up
4. Execute pacman -Suy
5.  Execute pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3 mingw-w64-x86_64-python3-gobject

## Run
### Linux
```bash
./iptv.py
```
or

```bash
./iptv.sh
```

### Windows
Execute the file iptv.bat


## Thanks
I used the m3uparser from that repository [M3uParser](https://github.com/Timmy93/M3uParser)
