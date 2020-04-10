### Usage

```
$ pip3 install -r requirements.txt
$ python3 main.py
Paste the URL of the tv-show/movie & press enter
once it is finished, the directory with all the music will be saved in tmp/[name-of-the-show]

* Windows users need to modify line 217 from "mkdir -p" to the Windows equivalent of that command, i'll probably do a version in the future where the OS will automatically be detected but for now the users are going to have to modify it themselves

```
### Known bugs
there might be a bug on some systems that shows this error<br>
``` http.cookiejar.LoadError: 'tmp/files/cookies.txt' does not look like a Netscape format cookies file ```<br>
and the only fix i can think of right now, is deleting this part<br>

``` --cookies tmp/files/cookies.txt``` 
from the line 218 in the main.py file <br>
i'll see if i can do anything about it some other time<br>

### To Do:
<s>*save the list to a file </s><br>
<s>*add the youtube-dl feature to download the songs</s><br>
*add the option to download the mp3 files into different directories that are sorted by season & episode<br>

## Original Authors:
https://github.com/SRG27/TuneFindToGMusic
* **LJ**<br>
message to LJ: i want to thank you for your script, i loved it and it served me well, but this is much better
<br>
<br>
https://github.com/joetats/youtube_search <br>
* **joetats** <br>
message to joetats: i wanted to thank you for your script, but i had to modify it a bit so it could better suit my script's needs
