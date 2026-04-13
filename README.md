# simple_ps4_theme_json_url_grabber
A lightweight python based dns server and http server to grab ps4 theme json urls

# Why bother grabbing theme json URLs?
Once you have the theme json URL, it can be used to download the PKG, which then can be processed into a format JB PS4's can install

# What does it do?
It hosts a dns server and http server on your local network, you can then enter the ip it tells you into your PS4's DNS server, then go and delete and redownload the theme you want to URL grab, it then should fail to download, and in the window you ran `main.py` say it has put the theme json url into `themes_urls.txt`

# Dependencies
has [dnslib](https://github.com/paulc/dnslib/tree/e266b75fab4464350346200638dbd08c254b5b01) embedded to make running as easy as possible
