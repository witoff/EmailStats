EmailStats
==========

Crunch and visualize stats about your email files.


Requirements:
- OS X
- Email accounts created in Apple Mail (IMAP or Exchange)
- Python
- (Optional) Gource to create pretty animations
- (Optional) FFMPEG to save those pretty animations to an mp4 file

Installation:
- Gource installation suggested via homebrew, linked through here: http://code.google.com/p/gource/wiki/MacSupport
- FFMPEG for video capture via this tutorial: http://hunterford.me/compiling-ffmpeg-on-mac-os-x/

Scripts:
- 1extract.py: Extract all email files into a local .json storage files
  - no arguments
- 2analyze.py: Analyze a .json files to print your DOD and other interesting information to the console
  - 1st argument is a json file
  - (optional) 2nd argument can be any combination of 's', 'o', or 't' to print additional sender, organizational or thread data.
- 3gource.py: Takes a .json file and produces a gource formatted output file of the same name as the input json file.
  - 1st argument is a .json file
- 4visualize.sh: Takes a .gource file and visualizes your email!
  - 1st argument is a .gource file
-  5record.sh: Takes a .gource file and creates an output mp4 file for uploading to youtube and showing your friends!
  - 1st argument is a .gource file 

