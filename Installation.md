
# Binary Packages #

For Windows and Mac, application packages are available. This is the easiest way to run ComicTagger.

### Windows Binary Package ###

Download the installer .exe and run it.

### Mac OS X Binary Package ###

Download the DMG file, open it, and drag the app onto your Desktop or Applications folder.

# Source #

The source package is much smaller, and if you only want to run ComicTagger as a command-line app, you may want to install this way.

To run ComicTagger from the python source, you may need to install some pre-requisites:

  * Python 2.6 or 2.7
  * PyQt matching the Python version -- _(Only needed for GUI)_
  * Pillow, a fork of the Python Imaging Library -- _(Only need for automated matching)_
  * Beautiful Soup 4
  * configparser

See below for some platform-specific details

If you are downloading manually, extract the source zip file.  Run the file called "comictagger.py".

On certain systems, you have the option to use "pip" (or "easy\_install") to install ComicTagger:

```
pip install -U comictagger
```


If you used pip, then "comictagger.py" should be in your path.  ( On Windows, probably "C:\Python\Scripts" )

### Source on Mac OS X ###

##### CLI #####
For running in command-line mode, you will need to install the following python packages:

```
pil beautifulsoup4 configparser
```

This can be done with "easy\_install" or "pip".

##### GUI #####
To use the GUI requires PyQT, which can be tricky to configure right (at least in my experience) since you will very likely have to have Apple's compiler on your system.  If you do, it's probably easiest to install via "brew" (http://mxcl.github.com/homebrew/)

If you do use brew, you may have to install the above requirements in the context of the "python" that was installed via brew.  (Very confusing, I know.  I only have one 32-bit Intel Mac mini to test on.)

Once you have brew installed:
```
brew install python pyqt pil pip
pip install beautifulsoup4 configparser
```
(Depending on your system, this may take a **very** long time).

Another option for PyQT are the binaries here: : http://sourceforge.net/projects/pyqtx/  I think they are 32-bit Intel builds, but I've not tested them myself.

_If you have any success with running the GUI on OSX from source, please post here or on the CT forums._

### Source on Windows ###

  * Python - http://www.python.org/getit/releases/2.7.3/
  * PyQt - http://www.riverbankcomputing.com/software/pyqt/download
  * PIL - http://www.pythonware.com/products/pil/
  * Beautiful Soup - http://www.crummy.com/software/BeautifulSoup/

### Source on Linux ###
Use the system package manager and python tools to install the requirements.  For example, use `apt-get` on Debian/Ubuntu systems:


```
sudo apt-get install python-qt4 python-imaging python-bs4
sudo pip install configparser
```

and, then, as mentioned above, use pip to install ComicTagger:
```
sudo pip install -U comictagger
```

Note:  you may need to use "--pre" for newer versions of pip, as it doesn't trust packages with the "beta" tag by default:
```
sudo pip install -U --pre comictagger
```

Another note(!):  Event more recent versions of pip require more options:
```
sudo pip install -pre --allow-external comictagger --allow-unverified comictagger comictagger
```

Other systems might use yum.  _Please share if you have a installation process not detailed here._

## WebP Issues ##

ComicTagger now uses Pillow ( a PIL/Python Imaging fork) for WebP support.

For it to work properly, when running from source, you will have to have some dependencies install first.  For example, on Ubuntu:
```
sudo pip uninstall pillow 
sudo apt-get install python-dev libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms1-dev libwebp-dev
sudo pip install pillow 
```