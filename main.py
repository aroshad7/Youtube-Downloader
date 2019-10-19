import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import bs4
import time, os, sys


def get_playlist_videos(url, resolution):
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
        sys.exit();

    # --------------------------
    # Go to Playlist Page
    # --------------------------
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

    # WARNING: sometimes page loads w/o load more button and refresh is based on scrolling
    # --------------------------
    # Get Source Code
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

    for i in range(len(name_list)):
        try:
            print("Acquiring video: " + name_list[i])
            driver.get(yt_link_list[i])
            time.sleep(15)
            ss_link_list.append(bs4.BeautifulSoup(driver.page_source, 'html.parser').find_all("a", {"title": "video format: " + resolution})[0]['href'])
        except KeyboardInterrupt:
            ss_link_list.append("");
            print("Skipping...")
            continue
        except Exception:
            ss_link_list.append("");
            print("Acquiring failed! Resolution might not be available.")


    driver.close()
    return list_name, name_list, ss_link_list


title, name_list, link_list = get_playlist_videos(input("Enter playlist URL: "), input("Enter required resolution: "))

try:
    original_umask = os.umask(0)
    os.makedirs(title, 0o777)
except Exception:
    pass
finally:
    os.umask(original_umask)

for i in range(len(name_list)):
    print("Downloading: " + name_list[i])
    try:
        urllib.request.urlretrieve(link_list[i], title + "/" + name_list[i] + ".mp4")
    except KeyboardInterrupt:
        print("Skipping...")
        continue
    except Exception as e:
        print("Error occurred: " + e + "/nSkipping...")

