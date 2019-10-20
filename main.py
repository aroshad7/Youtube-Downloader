import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import bs4
import time, os, sys, string

#Vaild characters for file name creation
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

#######################################################################################################################################################################################################################################################
def get_playlist_videos(url, resolution, aquire_wait_time, starting_video, ending_video):
    # --------------------------
    # Start Browser Service
    # --------------------------
    driver_path = os.getcwd() + '/chromedriver'
    try:
        service = ChromeService(driver_path)
        service.start()
        options = {}
        driver = webdriver.Remote(service.service_url, options)
        driver.implicitly_wait(3)
    except:
        print("Error occurred. Probably the chromedriver is missing. Keep the executable chromedriver file in the same directory as the Youtube Downloader!")
        while(1):
        	time.sleep(1)

    # --------------------------
    # Go to Playlist Page
    # --------------------------
    print("Indexing video list...")
    list_url = 'https://www.youtube.com/playlist?list=' + url[(url.index("list=")+5):]
    driver.get(list_url)
    time.sleep(3)

    # --------------------------
    # Click to Load Content
    # --------------------------
    there_is_more_to_load = True
    while there_is_more_to_load:
        try:
            load_more = driver.find_element_by_class_name("load-more-text")
            driver.implicitly_wait(5)
            load_more.click()
            time.sleep(3)
        except:
            there_is_more_to_load = False

    # --------------------------
    # Get Page Source
    # --------------------------
    page = bs4.BeautifulSoup(driver.page_source, 'html.parser')

    # --------------------------
    # Extract Video Info
    # --------------------------
    list_name = page.select('a[class="yt-simple-endpoint style-scope yt-formatted-string"]')[0].text
    yt_link_list = []
    ss_link_list = []
    name_list = []
    second_inner = page.find_all("div", {"id": "contents", "class": "style-scope ytd-playlist-video-list-renderer"})
    last_div = second_inner[0].find_all("div", {"class": "style-scope ytd-playlist-video-renderer", "id": "content"});

    for video in last_div:
        name_list.append(video.find_all("span", id="video-title")[0].text[17:-15])
        yt_link_list.append("http://ssyoutube.com" + video.find_all("a")[0]['href'])
    starting_video = int(starting_video) - 1
    ending_video = int(ending_video)
    if ending_video > len(name_list):
    	ending_video = len(name_list)

    for i in range(0, len(name_list)):
        if (i>=starting_video) and (i<ending_video):                
            try:
                print("Acquiring video: " + name_list[i])
                driver.get(yt_link_list[i])
                time.sleep(int(aquire_wait_time))
                ss_link_list.append(bs4.BeautifulSoup(driver.page_source, 'html.parser').find_all("a", {"title": "video format: " + resolution})[0]['href'])
            except KeyboardInterrupt:
                ss_link_list.append("");
                print("Skipping...")
                continue
            except Exception:
                ss_link_list.append("");
                print("Acquiring failed! Resolution might not be available.")
        else:
            ss_link_list.append("")

    driver.close()
    return list_name, name_list, ss_link_list, starting_video, ending_video
#######################################################################################################################################################################################################################################################
#######################################################################################################################################################################################################################################################
def get_download_path():
    """Returns the default downloads path for linux or windows"""
    try:
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'downloads')
    except Exception:
            return ""
#######################################################################################################################################################################################################################################################

title, name_list, link_list, start, end = get_playlist_videos(input("Enter playlist URL: "), input("Enter required resolution: "), input("Enter wait time for acquiring: "), input("Starting video number: "), input("Ending video number: "))
downloads_path = ""
	
try:
    original_umask = os.umask(0)
    title = ''.join(c for c in title if c in valid_chars)
    downloads_path = get_download_path() + "/" + title
    os.makedirs(downloads_path, 0o777)
except Exception as e:
    print("Folder creating problem: " + str(e))
    pass
finally:
    os.umask(original_umask)

for i in range(start, end):
    print("Downloading: " + name_list[i])
    try:
        urllib.request.urlretrieve(link_list[i], downloads_path + "/" + ''.join(c for c in name_list[i] if c in valid_chars) + ".mp4")
    except KeyboardInterrupt:
        print("Skipping...")
        continue
    except Exception as e:
        print("Error occurred: " + str(e) + "\nSkipping...")


print("Downloading completed")
while(1):
	time.sleep(1)
