# Youtube Downloader

This is a chrome driver based youtube video downloader with the help of savefrom.net.

  - Requires python 3, Selenium and Beautifulsoup.
  - Chrome driver executable should be placed in the same folder as the Youtube Downloader executable.
  - If the application continuously reports of a chrome driver missing, download the latest chrome driver version and replace the old one.
  - For linux use the respective Chrome driver.
  - Do not close the auto opening chrome window. The downloader will close it automatically when aquiring is completed.
  - You can use pyinstaller to create the executable for both linux and windows.

  -	When prompted for Resolution, enter a resolution available on the savefrom.net for the given video. Most of the time only 360 and 720 will be available.
  -	When prompted for the Acquire wait time make sure to give enough time required by savefrom.net to load the youtube video. Generally 10 will be a good value. If Acquiring fails even if the selected resolution is available, try a larger value for this.

