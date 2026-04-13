# simple_ps4_theme_json_url_grabber
A lightweight python based dns server and http server to grab ps4 theme json urls

# Why bother grabbing theme json URLs?
Once you have the theme json URL, it can be used to download the PKG, which then can be processed into a format JB PS4's can install

# How to process the json URL into a JB PS4 theme
Just give to me XD, I currently have a tool which packages everything up into one nice zip! If you do not want to do that, I highly recommened that you archive the url alongside the 2 pkgs youll make following this [guide](https://www.psxhax.com/threads/making-permanent-ps4-themes-with-official-pkgs-guide-by-panzah1488.5872/).

# What does it do?
It hosts a dns server and http server on your local network, you can then enter the ip it tells you into your PS4's DNS server, then go and delete and redownload the theme you want to URL grab, it then should fail to download, and in the window you ran `main.py` say it has put the theme json url into `themes_urls.txt`

# How to use?
# If you cannot delete and redownload the theme, you cannot continue with getting the URL!
## Check if you can delete and redownload the theme
go to your themes in the settings page, and delete the theme (press Options/start on the theme then Delete), the theme might disapear, if so go to the bottom of the theme and it should be there, if it is not, then sign into the account that purchased the theme, it should be at the bottom there <br><br>

after you have found the theme, a small download icon should be in the bottom right corner of the theme, now just press on the theme and it should start downloading again
## hosting the server
either git clone or download and extract the code zip file, then open a terminal/cmd in the folder containing the `main.py` file, then run the command
### Windows
```
python main.py
```
### Linux
```
python3 main.py
```
If you have python installed, it should print in the window (it should not print anything else yet)
```
Please enter ... on your PS4's primary and secondary DNS
```
(of course it will show your local ip here)
## PS4 setup
### Network setup
Follow this video https://youtu.be/-lg5CH8hpjs <br>
but put in the ip the command told you to instead <br>
When testing the internet connection, it should say `Successful` for `PlayStation Network Sign-In`, it might say `An error has occured` but as long as `PlayStation Network Sign-In` was `Successful` then it is good <br><br>

look at the window, it should now have printed
```
DNS server is working!
```
if not something is not working
### Theme setup
delete and redownload the theme as explained eariler, but this time, the theme download should fail, making a  `Cannot download.` notification and the download bar with a small cross on it (you can do mutiple themes at once here), but if you look at the window, it should say
```
new theme url THEME URL HERE in .../themes_urls.txt
```
Now if you look in the folder with `main.py` in it, you should see a `themes_urls.txt` file, in there will be all the theme json URLs you redownloaded!
# Dependencies
has [dnslib](https://github.com/paulc/dnslib/tree/e266b75fab4464350346200638dbd08c254b5b01) embedded to make running as easy as possible
