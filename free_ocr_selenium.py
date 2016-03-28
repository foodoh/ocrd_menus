#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @Date:   2016-03-26
# @Last Modified by:   Tasdik Rahman
# @Last Modified time: 2016-03-28 11:07:07
# @MIT License
# @http://tasdikrahman.me
# @https://github.com/prodicus

"""
Automates the task of uploading a menu image to http://free-ocr.com and get
OCR'd menu text.

References
==========

[1]:  http://stackoverflow.com/a/33691162/3834059
"""

import os
import json

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

PATH = os.path.abspath(os.path.join("."))
MENU_PATH = os.path.join(PATH, "menu_images")
RESULT_PATH = os.path.join(PATH, "menu_text")
URL = "http://www.free-ocr.com/"


# Selenium constants
EXTENSIONS_PATH = '/home/tasdik/.mozilla/firefox/6c4s1jlx.Nightly/extensions/{0}'
# loading the extension which allows us to disable images and styles
DEVERLOPER_TOOLS = EXTENSIONS_PATH.format(
    '{c45c406e-ab73-11d8-be73-000a95be3b12}.xpi')
FIREBUG = EXTENSIONS_PATH.format('firebug@software.joehewitt.com.xpi')
JAVA_EXT = EXTENSIONS_PATH.format(
                '{E6C1199F-E687-42da-8C24-E7770CC3AE66}.xpi')
UBLOCK = EXTENSIONS_PATH.format('uBlock0@raymondhill.net.xpi')


def clean_raw_text(raw_text):
    """
    cleans the raw_text of empty strings and integers

    :param raw_text: the text to be cleaned and returned back to 
                     make_hotel_file()
    :returns: A iterable list of the menu items

    Example
    =======

    >>>raw_text

    'SALADS\n\nClassical caesar salad with parmesan shaving: and garlic \
    bread\n\nCandied walnuts, orange segments and mixed greens tossed \
    in\norange sesame dressing\n\nCherry tomatoes, olives and cheese with \
    mixed greens and\nlemon oregano dressing\n\nGrilled aubergine with wild \
    rocket and balsamic vinaigrette\n\nSteamed potato, orange segments, \
    hordboiled egg and\nconfit base with olive oil dressing\n\nYoppings non \
    veg: chickenf‘prawn\n\nSOUPS\n\nWild mushroom creamy soup gamlilied with \
    garlic toast\nCreamed broccoli soup garnished with garlic cheese \
    toast\n\nTraditional Spanish gazpocho, cold tomato soup topped\nwith \
    basil and olive oil\n\nBURGERS: Served With Fries And House Salad\n\nBeef\
    party cooked to perfection topped with sliced cheese,\nsauteed onion,\
    mushrooms, ialapenos and tomatoes\n\nChicken patty topped with sliced \
    cheese, cucumber, onion\nand coiun mayonnaise \
    \n\n300\n\n300\n\n300\n\n350\n\n400\n\n90\n\n200\n200\n\n250\n350\n\n350'

    >>> filter_cleaned
    ['SALADS', 'Classical caesar salad with parmesan shaving and garlic bread',\
     'Candied walnuts, orange segments and mixed greens tossed in',\
     'orange sesame dressing', 'Cherry tomatoes, olives and cheese with mixed\
      greens and', 'lemon oregano dressing', 'Grilled aubergine with wild \
      rocket and balsamic vinaigrette', 'Steamed potato, orange segments, \
      hordboiled egg and', 'confit base with olive oil dressing', 'Yoppings \
      non veg: chickenf‘prawn', 'SOUPS', 'Wild mushroom creamy soup gamlilied \
      with garlic toast', 'Creamed broccoli soup garnished with garlic cheese\
      toast', 'Traditional Spanish gazpocho, cold tomato soup topped', \
      'with basil and olive oil', 'BURGERS: Served With Fries And House \
      Salad', 'Beef party cooked to perfection topped with sliced cheese,',\
      'sauteed onion, mushrooms, ialapenos and tomatoes', 'Chicken patty \
      topped with sliced cheese, cucumber, onion', 'and coiun mayonnaise']
    """
    # loads the raw_text and cleans the empty strings from the list
    filter_cleaned = [x for x in filter(bool, raw_text.split('\n'))]
    # cleaning the integers in the list
    return [x for x in filter_cleaned if not x.isdigit()]


def get_raw_ocr_text(menu, driver):
    """
    Opens selenium web driver, uploads image and returns the raw orcd text
    from the image to `make_hotel_file()`

    Tries to wait for the whole webpage to load up

    :param menu: one single image from the list of images in the hotel menu
                 list
    :param driver: the webdriver instance being passed around
    :returns: the ocrd text in uncleaned format
    """
    try:
        # passes full path to img file to webdriver to upload to free-ocr.com
        driver.find_element_by_id("fileupfield").send_keys(menu)

        # clicks the submit button to start the OCR process
        driver.find_element_by_id("fbut").click()

        # get the raw uncleaned text from the page
        raw_text = driver.find_element_by_id("resultarea").text

        # return the webdriver to the home page
        driver.find_element_by_id("back-start-button").click()
        if raw_text:
            return raw_text
        else:
            return None
    except TimeoutException as e:
        print(e)
        return


def make_hotel_file(hotel, menu_list, driver):
    """
    Will create the hotel directory inside the 'RESULT_PATH' and store the
    OCR'd text inside it. 

    :param hotel: the name of the hotel for which the list of images is to
                  be uploaded
    :param menu_list: the menu images for the hotel with absolute paths to it
    :param driver: the webdriver instance being passed around
    """
    hotel_menu_path = os.path.join(RESULT_PATH, hotel)
    hotel_file_name = "{0}.txt".format(hotel_menu_path)
    cleaned_menu = []  # stores all the ocr'd menu of the hotel

    # create the directory, if it does not exists for storing the ocrd menus
    with open(hotel_file_name, 'w') as f:
        for menu in menu_list:
            # calling selenium to upload that image and get the raw_text back
            raw_text = get_raw_ocr_text(menu, driver)
            if raw_text:
                # clean this raw text and append to the menu content
                cleaned_menu.extend(clean_raw_text(raw_text))
            else:
                continue

        # converting the list to JSON format for easy readability
        json_dict = {
            "menu_items": cleaned_menu,
            "restaurant_name": hotel
        }

        # writing this JSON to the hotel_file
        json.dump(json_dict, f, sort_keys=True, indent=4, ensure_ascii=False)


def get_image_list(hotel, menus):
    """
    Gets the image list (full path) for each hotel and returns that list

    Example
    =======

    For a file 

    menu_images
        │   ├── 3-kings-kafe-kitchen-marathahalli-listing
        │   │   ├── 3-kings-kafe-kitchen-marathahalli-listing_0.jpg

    Returns something like
    ======================

    /home/tasdik/Documents/github/foodoh/ocrd_menus/menu_images/ \
    3-kings-kafe-kitchen-marathahalli-listing/ \
    3-kings-kafe-kitchen-marathahalli-listing_3.jpg'

    :param hotel: the name of the hotel for which the list of images is to
                  be uploaded
    :param menus: returns the list of images with its absolute path in the
                  file system
    :returns: the menu_list with it's absolute path for that particular hotel

    """
    menu_list = [menu for menu in map(lambda x: os.path.join(
        MENU_PATH, hotel, x), menus)]
    return menu_list

def initialize_webdriver():
    """
    Creates a web profile for the firefox driver for loading specific
    extensions and configs

    :returns: the web_driver profile
    """
    # create the firefox webdriver instance
    firefox_profile = webdriver.FirefoxProfile()

    # Loading the extensions in firefox profile
    firefox_profile.add_extension(extension=JAVA_EXT)
    firefox_profile.add_extension(extension=UBLOCK)

    # ===== Load the page fast by disabling a crap load of stuff =======
    # Reference: [1]

    firefox_profile.set_preference("network.http.pipelining", True)
    firefox_profile.set_preference("network.http.proxy.pipelining", True)
    firefox_profile.set_preference("network.http.pipelining.maxrequests", 8)
    firefox_profile.set_preference("content.notify.interval", 500000)
    firefox_profile.set_preference("content.notify.ontimer", True)
    firefox_profile.set_preference("content.switch.threshold", 250000)
    # Increase the cache capacity.
    firefox_profile.set_preference("browser.cache.memory.capacity", 65536)
    firefox_profile.set_preference("browser.startup.homepage", "about:blank")
    # Disable reader, we won't need that.
    firefox_profile.set_preference("reader.parse-on-load.enabled", False)
    # Duck pocket too!
    firefox_profile.set_preference("browser.pocket.enabled", False)
    firefox_profile.set_preference("loop.enabled", False)
    # Text on Toolbar instead of icons
    firefox_profile.set_preference("browser.chrome.toolbar_style", 1)
    # Don't show thumbnails on not loaded images.
    firefox_profile.set_preference(
        "browser.display.show_image_placeholders", False)
    # Don't show document colors.
    firefox_profile.set_preference(
        "browser.display.use_document_colors", False)
    # Don't load document fonts.
    firefox_profile.set_preference("browser.display.use_document_fonts", 0)
    # Use system colors.
    firefox_profile.set_preference("browser.display.use_system_colors", True)
    # Autofill on forms disabled.
    firefox_profile.set_preference("browser.formfill.enable", False)
    # Delete temprorary files.
    firefox_profile.set_preference(
        "browser.helperApps.deleteTempFileOnExit", True)
    firefox_profile.set_preference("browser.shell.checkDefaultBrowser", False)
    firefox_profile.set_preference("browser.startup.homepage", "about:blank")
    # blank
    firefox_profile.set_preference("browser.startup.page", 0)
    # Disable tabs, We won't need that.
    firefox_profile.set_preference("browser.tabs.forceHide", True)
    # Disable autofill on URL bar.
    firefox_profile.set_preference("browser.urlbar.autoFill", False)
    # Disable autocomplete on URL bar.
    firefox_profile.set_preference(
        "browser.urlbar.autocomplete.enabled", False)
    # Disable list of URLs when typing on URL bar.
    firefox_profile.set_preference("browser.urlbar.showPopup", False)
    # Disable search bar.
    firefox_profile.set_preference("browser.urlbar.showSearch", False)
    # Addon update disabled
    firefox_profile.set_preference("extensions.checkCompatibility", False)
    firefox_profile.set_preference("extensions.checkUpdateSecurity", False)
    firefox_profile.set_preference(
        "extensions.update.autoUpdateEnabled", False)
    firefox_profile.set_preference("extensions.update.enabled", False)
    firefox_profile.set_preference("general.startup.browser", False)
    firefox_profile.set_preference("plugin.default_plugin_disabled", False)
    # Image load disabled again
    firefox_profile.set_preference("permissions.default.image", 2)
    firefox_profile.set_preference("permissions.default.stylesheet", 2)

    # ===== Load the page fast by disabling crap load of stuff  =======
    return firefox_profile

def run(firefox_profile):
    """
    Starts the Firefox web driver with the decided configuration files

    :param firefox_profile: Takes the config file returned by 
                            initialize_webdriver()
    """
    # starting the web driver
    driver = webdriver.Firefox(firefox_profile=firefox_profile)

    # retrieving the URL
    driver.get(URL)
    driver.implicitly_wait(100)
    driver.set_page_load_timeout(100)

    for hotel in os.listdir(MENU_PATH):
        # return the list of menus in the hotel dir

        # skipping the hotel if it has already been processed
        hotel_menu = os.path.join(RESULT_PATH, hotel)
        hotel_menu += '.txt'
        if os.path.exists(hotel_menu):
            continue

        else:
            menu_list = get_image_list(
                hotel, os.listdir(os.path.join(MENU_PATH, hotel)))
            """
            feed this list to a helper function which makes the hotel dir and
            calls selenium
            """
            make_hotel_file(hotel, menu_list, driver)


def main():
    firefox_profile = initialize_webdriver()
    run(firefox_profile)


if __name__ == "__main__":
    main()
