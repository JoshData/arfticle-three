arfticlethree
=============

* Follow my [cmusphinx-alignment-example](https://github.com/JoshData/cmusphinx-alignment-example) instructions to get cmusphinx set up with my driver class and `align.sh`.
* Get an oral argument audio file (MP3) and transcript text from Oyez.org (e.g. [here](http://www.oyez.org/cases/2010-2019/2014/2014_13_553). From the case page, click on the Argument audio link. Download the MP3, and then click Full Transcript Text and copy and paste the transcript into a similarly named text file. You should have files like `13-553_20141209-argument.mp3` and `13-553_20141209-argument.txt`.
* Convert the MP3 to a 16khz 16bit mono WAV:

    sox 13-553_20141209-argument.mp3 -b 16 13-553_20141209-argument.wav channels 1 rate 16k

* Run the transcript parser to segment the transcript by speaker:

	python3 parse_transcript.py 13-553_20141209-argument.txt

* It won't necessarily get the speakers right. Look at `13-553_20141209-argument.speakers.txt` and put #-marks before any line that is not actually a speaker. If you made any change, re-run the script above (it'll look for this file this time and use the list of speakers in the file). The script will write out `13-553_20141209-argument.words.txt` which contains just the spoken words.

* Run the aligner. This part will take about 2-3 times as long as real time. If the oral argument was an hour, expect the alignment process to take 2-3 hours to finish.

	path/to/align.sh 13-553_20141209-argument.wav 13-553_20141209-argument.words.txt > 13-553_20141209-argument.csv

* Extract the speaker turn times by running the last script:

	python3 get_alignment.py 13-553_20141209-argument.txt > 13-553_20141209-argument.turns.csv

You'll get `13-553_20141209-argument.turns.csv`, which is a CSV file where the first column is the name of a speaker and the second and third columns are the start and end times (in miliseconds) of when that speaker was speaking.
