# Extract and Rename Ekahau Wireless Scan Photos

## How to Use:
1. Install Python version 3.10+ for your OS see [Python](https://www.python.org/).
2. Install requirements:
    `pip install -r requirements.txt`
3. Copy ESX file to script location:
    `cp Sonoco Pardeeville AP and IDF Information_Final.esx ekahau-extract-photos`
4. Run the script against the ESX file:
    `./extract_photos.py Sonoco Pardeeville AP and IDF Information_Final.esx`
    or
    `python extract_photos.py Sonoco Pardeeville AP and IDF Information_Final.esx`

## What will happen?
The script will extract the ESX file and use the contents.  It will create an
AP-Images folder move and rename photos according to the information available.
Then it will remove the extracted ESX folder leaving the modified AP-Images
folder.

## What if I already have an AP-Images folder?
It will be overwritten for each run.  Ensure you rename, move, or delete the
AP-Images folder prior to use.
