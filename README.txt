install chord extractor
   
   - Installation
	
	The package is hosted on PyPI, but prior to installing that there are a few prerequisite 		steps. The following instructions assume the latest versions of Ubuntu, and it is 		recommended to use a modern 64-bit Linux system. That said, equivalent steps should work 		if you are using another OS.

	sudo apt-get install libsndfile1 - To read sound files.
	
	(OPTIONAL) sudo apt-get install timidity - If wanting to extract chords from MIDIs 		(timidity converts midi to wav files).
	
	(OPTIONAL) sudo apt-get install ffmpeg - If wanting to extract from mp3s
	
	pip install numpy - numpy needs to be installed in your Python environment prior to 	installing chord-extractor. This is necessary as one of the package dependencies (vamp) 		requires it in its setup.py.
	
	After that you are ready to run
	pip install chord-extractor

install PySimpleGUI

   - Installation
	
	The current suggested way of invoking the pip command is by running it as a module using 		Python. Previously the command pip or pip3 was directly onto a command-line / shell. The 		suggested way

	- Initial install for Windows:

		python -m pip install PySimpleGUI

	- Initial install for Linux and MacOS:

		python3 -m pip install PySimpleGUI

install ShazamAPI

   - Installation
   
	pip3 install ShazamAPI
	Also you need to install ffmpeg and ffprobe then add it to path

install bs4

   - Installation
   	
   	pip install beautifulsoup4
	
install pychord

   - Installation
   	
   	pip install pychord
