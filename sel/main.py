import os
import time
import requests
import requests_html
from urllib.parse import urlparse
from selenium import webdriver
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


USERNAME = os.environ.get("INSTA_USERNAME")
PASSWORD = os.environ.get("INSTA_PASSWORD")


browser = webdriver.Chrome()
browser.get("https://www.instagram.com")

time.sleep(1)
username_el = browser.find_element_by_name("username")
password_el = browser.find_element_by_name("password")

time.sleep(2)
username_el.send_keys(USERNAME)
password_el.send_keys(PASSWORD)

time.sleep(2)
# body_el = browser.find_element_by_css_selector("body")
# body_html = body_el.get_attribute("innerHTML")
submit_button_el = browser.find_element_by_css_selector(
    "button[type='submit']")
submit_button_el.click()


def click_to_follow(browser):
    # follow_btn_xpath = "//*[contains(text(), 'Follow')][not( contains(text(), 'Following') )]"
    # follow_btn_xpath = "//a[contains(text(), 'Follow')][not( contains(text(), 'Following') )]"
    follow_btn_xpath = "//button[contains(text(), 'Follow')][not( contains(text(), 'Following') )]"
    follow_btn_els = browser.find_elements_by_xpath(follow_btn_xpath)
    for btn in follow_btn_els:
        time.sleep(3)
        try:
            btn.click()
        except:
            pass


time.sleep(2)
user_profile = "https://www.instagram.com/leomessi/"
browser.get(user_profile)

# post_url_pattern = "https://www.instagram.com/p/<post-slug-id>"

post_xpath_string = "//a[contains(@href, /p/)]"
post_links = browser.find_elements_by_xpath(post_xpath_string)
post_link_el = None

if len(post_links) > 0:
    post_link_el = post_links[0]

if post_link_el != None:
    post_href = post_link_el.get_attribute("href")
    browser.get(post_href)

video_els = browser.find_elements_by_xpath("//video")
images_els = browser.find_elements_by_xpath("//img")

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)


def scrape_and_save(media_elements):
    for el in media_elements:
        url = el.get_attribute("src")
        base_url = urlparse(url).path
        filename = os.path.basename(base_url)
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            continue
        with requests.get(url, stream=True) as r:
            try:
                r.raise_for_status()
            except:
                continue
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)


def automate_comments(comment_content):
    time.sleep(5)
    comment_xpath_string = "//textarea[contains(@placeholder, 'Add a comment')]"
    comment_el = browser.find_elements_by_xpath(comment_xpath_string)
    comment_el.send_keys(comment_content)
    submit_btn_xpath = "button[type='submit']"
    submit_btn_els = browser.find_elements_by_css_selector(submit_btn_xpath)
    time.sleep(2)
    for btn in submit_btn_els:
        try:
            btn.click()
        except:
            pass


def automate_liking():
    like_heart_svg_xpath = "//*[contains(@aria-label, 'Like')]"
    all_heart_like_els = browser.find_elements_by_xpath(like_heart_svg_xpath)
    max_heart_h = -1
    for h_el in all_heart_like_els:
        height = h_el.get_attributes("height")
        current_height = int(height)
        if current_height > max_heart_h:
            max_heart_h = current_height

    all_heart_like_els = browser.find_elements_by_xpath(like_heart_svg_xpath)
    max_heart_h = -1
    for h_el in all_heart_like_els:
        height = h_el.get_attributes("height")
        if height == max_heart_h or height == f"{max_heart_h}":
            parent_element = h_el.find_elements_by_xpath("..")
            time.sleep(2)
            try:
                parent_element.click()
            except:
                pss
