#!/usr/bin/python3

import sys, json, os.path, re

if len(sys.argv) < 2:
	print("Usage: python3 parse_transcript.py 1x-xxx_yyyymmdd-argument.txt")
	sys.exit(1)

if not sys.argv[1].endswith('.txt'):
	print("Transcript file name should end with .txt.")
	sys.exit(1)

# Let the user override the list of speakers.
speakers_file = sys.argv[1].replace(".txt", ".speakers.txt")
speakers = None
if os.path.exists(speakers_file):
	print("Using speaker list in %s." % speakers_file)
	with open(speakers_file) as f:
		speakers = set(line.strip() for line in f if not line.startswith("#"))

# Read the transcript and segment by speaker.
turns = []
with open(sys.argv[1]) as f:
	for line in f:
		# Trim newline characters, skip blank lines.
		line = line.strip()
		if line == "": continue

		# See if the line is like "Speaker: text text text"
		parts = line.split(': ', 1)
		if len(parts) == 2 and (len(parts[0]) < 50 if not speakers else parts[0] in speakers):
			speaker, text = parts
		else:
			text = line

		# Add.
		if len(turns) == 0 or speaker != turns[-1]['speaker']:
			turns.append({
				"speaker": speaker,
				"text": [text],
			})
		else:
			turns[-1]['text'].append(text)

# Tokenize.
# We want to tokenize the transcript into words. Although cmusphinx can do tokenization,
# we will need to line the tokens up back with the speaker segmentation later, so it is better for
# everyone to be on the same page by tokenizing here.
def tokenize(line):
	return [tok.lower() for tok in re.split(r"\W*\s+\W*|\W$|[\(\)\[\]\-]+", line) if tok.strip() != ""]
for turn in turns:
	turn['tokens'] = [tokenize(line) for line in turn['text']]

# Write out a list of speakers so the user can remove junk and re-run if
# our autodetection of speakers (before colons) picked up incorrect content.
if not speakers:
	print("Writing a speaker list to %s. Put hash-marks before misparsed 'speakers' to remove them and then re-run this script." % speakers_file)
	speakers = sorted(set(t['speaker'] for t in turns))
	with open(speakers_file, 'w') as f:
		f.write(''.join(s+'\n' for s in speakers))

# Write out a JSON file of the speaker-segmented transcript.
with open(sys.argv[1].replace(".txt", ".json"), 'w') as f:
	json.dump(turns, f, indent=2, sort_keys=True)

# Write out a flat text file of just the spoken words, to pass
# into the aligner.
output_file = sys.argv[1].replace(".txt", ".words.txt")
print("Wrote %s." % output_file)
with open(output_file, 'w') as f:
	for turn in turns:
		for line in turn['tokens']:
			for token in line:
				f.write(token + '\n')
