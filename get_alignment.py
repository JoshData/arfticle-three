import sys, json, csv, difflib

if len(sys.argv) < 2:
	print("Usage: python3 get_alignment.py 1x-xxx_yyyymmdd-argument.txt")
	sys.exit(1)

# Load the transcript data.
transcript = json.load(open(sys.argv[1].replace(".txt", ".json")))
tokens = []
for speaker in transcript:
	for line in speaker['tokens']:
		for word in line:
			tokens.append((word, speaker['speaker']))

# Load the alignment.
alignment = []
csv_file = sys.argv[1].replace(".txt", ".csv")
for row in csv.reader(open(csv_file)):
	row = dict(list(zip(('token', 'pronunciation', 'inserted', 'confidence', 'starttime', 'endtime'), row)))
	alignment.append(row)

# The alignment sometimes... drops tokens? I'm not sure. Do our
# best to line up the alignment and the original list of tokens.
last_speaker = None
turns = []
for i, j, n in difflib.SequenceMatcher(a=[t[0] for t in tokens], b=[a['token'] for a in alignment]).get_matching_blocks():
	for x in range(n):
		speaker = tokens[i+x][1]
		if speaker != last_speaker:
			last_speaker = speaker
			turns.append([speaker, alignment[j+x]['starttime'], alignment[j+x]['endtime']])
		else:
			turns[-1][2] = alignment[j+x]['endtime']

w = csv.writer(sys.stdout)
for turn in turns:
	w.writerow(turn)
