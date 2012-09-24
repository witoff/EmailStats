EmailStats
==========

Crunch and visualize stats from your local Apple Mail email accounts.

## Requirements:
* OS X
* Email accounts created in Apple Mail (IMAP or Exchange)
* Python
* _(Optional)_ Gource to create pretty animations
* _(Optional)_ FFMPEG to save those pretty animations to an mp4 file

## Dependency Installation:
* Gource installation via [homebrew](http://code.google.com/p/gource/wiki/MacSupport)
* FFMPEG for video capture via [this script](http://hunterford.me/compiling-ffmpeg-on-mac-os-x/)

## Scripts:
1. Extract: Extract each local Apple Mail email accounts into a .json storage file
  * running: ./1extract.py
2. Analyze: Analyze an extracted email account to print your DOD and other interesting information to the console
  * running: ./2analyze.py email_file.json [s,o,t] 
    * _email_file.json_: A json storage file of an email account
    * _s_: Additionally analyze sender data
    * _o_: Additionally analyze organizational data
    * _t_: Additionally analyze thread data
3. FormatForGource: Takes a .json file and produces a gource formatted output file of the same name as the input json file.
  * running: ./3formatForGource.py email_file.json
    * _email_file.json_: A json storage file of an email account
4. Visualize: Takes a .gource file and visualizes your email!
  * running: ./4visualize.sh email_file.gource
    * _email_file.gource_: A gource formatted file of an email account
5.  Record.sh: Takes a .gource file and creates an output mp4 file for uploading to youtube and showing your friends
  * running: ./5record.sh email_file.gource
    * _email_file.gource_: A gource formatted file of an email account

