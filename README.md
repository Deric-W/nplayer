# nplayer
Python script wich plays notes stored in a json file with mpg123.

## How it works:
 - the script is called with the file to play
 - additional parameters: -d = debug mode, -p playerpath = set custom path to mpg123.
 - the file is encoded in json and contains a header with the base (seconds/tact), tact (dezimal tact, like 4/4 = 1) and includes (list of packs wich will be used).
 - the file also contains a notes section with the values sounds (list of files to play together from pack), types (list of note types like 1/4 = 4, 1/8 = 8), packs (list of packs of the sounds) and wait (if True, wait for notes to finish).
  - Note: each value in sounds needs a value with the same index in types and packs.
 
## Packs:
 - a Pack is a directory in ` <directory with nplayer.py>/packs/` with sounds and a pack.json
 - the pack.json contains the samplerate and the file extension of the files in the directory.
 - for examples take a look in "packs".
