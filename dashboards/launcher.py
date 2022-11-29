import sys
from time import sleep
from selenium import webdriver
from .auth import login, check_exists_by_xpath


def open_page(**params):
    if params['driver'] == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        # options.add_argument("disable-infobars")
        options.binary_location = "/usr/bin/chromium-browser"
        browser = webdriver.Chrome(chrome_options=options)
    elif params['driver'] == 'firefox':
        options = webdriver.FirefoxOptions()
        # options.add_argument("--kiosk")
        browser = webdriver.Firefox(firefox_options=options, log_path="/tmp/geckodriver.log")
    else:
        pass

    browser.set_window_position(params['x'], params['y'])
    if params['fullscreen']:
        browser.fullscreen_window()
    else:
        browser.set_window_size(params['width'], params['height'])

    try:
        if params['driver'] == 'chrome':
            browser.get('chrome://settings')
            browser.execute_script(
                'chrome.settingsPrivate.setDefaultZoom({zoom});'.format(zoom=(params['zoom'] / 100.0)))
        browser.get(params['url'])
        browser = login(browser, params)

        if params['tab']:  # Open link in new tab
            window_before = browser.window_handles[0]
            link = params['tab']
            browser.execute_script("window.open('{}');".format(link))
            window_after = browser.window_handles[1]
            # browser.close() # Close pervios tab
            browser.switch_to.window(window_after)

    except Exception:
        browser.quit()
        sys.exit(1)

    while True:
        try:
            sleep(params['refresh'])
            browser.refresh()
            if params['driver'] == 'chrome' and check_exists_by_xpath(browser,
                                                                      '//*[@id="error-information-popup-content"]/div[2]'):
                raise Exception("Something went wrong with network or so")
        except Exception as err:
            browser.quit()
            sys.exit(1)
