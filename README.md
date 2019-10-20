# Youtube Downloader

This is a chrome driver based youtube video downloader with the help of savefrom.net.

  - Requires python 3, Selenium and Beautifulsoup
  - Chrome driver executable should be placed in the same folder as the Youtube Downloader executable
  - For linux use the respective Chrome driver
  - Do not close the auto opening chrome window. You can close it once the downloading is started.
  - You can use pyinstaller to create the executable for both linux and windows

  -	When prompted fro Resolution, enter a resolution available on the savefrom.net for the given video. Most of the time only 360 and 720 will be available
  -	When prompted for the Acquire wait time make sure to give enough time required by savefrom.net to load the youtube video. Generally 10 will be a good value. If Acquiring fails even if the selected resolution is available, try a larger value for this

