from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def check_exists_by_xpath(browser,xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def login(browser, params):
    if not params.get('application'):
        params['application'] = 'default'

    if params['application'] == 'grafana':
        browser.find_element_by_xpath("//input[@name='user']").send_keys(params['user'])
        browser.find_element_by_xpath("//input[@name='password']").send_keys(params['password'])
        # browser.find_element_by_xpath("//button[@type='submit']").click()
        browser.execute_script("document.querySelector('#login-view > form > div.login-button-group > button').click()")

    elif params['application'] == 'jenkins':        
        browser.find_element_by_xpath("//input[@name='j_username']").send_keys(params['user'])
        browser.find_element_by_xpath("//input[@name='j_password']").send_keys(params['password'])
        sleep(2)
        browser.find_element_by_xpath("//input[@type='submit']").click()
        sleep(2)
        try:  # Collapse sidebar
           browser.find_element_by_class_name('side-nav__collapse').click()
           sleep(2)
        except NoSuchElementException:
            pass
        # Hide div block
        # element = browser.find_element_by_class_name('app__nav') 
        # browser.execute_script("arguments[0].style.display = 'none';",element) 
               

    elif params['application'] == 'monitor':
        # browser.find_element_by_xpath("//div[@class='user-menu__title']").click()
        browser.execute_script("document.querySelector('#app > div > header > div > div.header__controls > div > div').click()")
        browser.find_element_by_xpath("//input[@type='text']").send_keys(params['user'])
        browser.find_element_by_xpath("//input[@type='password']").send_keys(params['password'])
        # browser.find_element_by_xpath("//button[@class='btn btn--primary ']").click()
        browser.execute_script("document.querySelector('#modal-root > div > div.modal > div > div > div.modal__body.modal__body--no-padding > div > div.form__footer > div > div > button.btn.btn--primary').click()")
        sleep(5)
        # browser.find_element_by_xpath("//button[@class='header__theme-switcher']").click()
        browser.execute_script("document.querySelector('#app > div > header > div > div.header__controls > button').click()")

    elif params['application'] == 'hdb':
        while check_exists_by_xpath(browser,"//div[@class='md-title'][contains(text(),'Login')]"):
            browser.find_element_by_xpath("//input[@placeholder='Username']").send_keys(params['user'])
            browser.find_element_by_xpath("//input[@type='password']").send_keys(params['password'])
            # browser.find_element_by_xpath("//button[@type='submit']").click()
            browser.execute_script("document.querySelector('#YG_App > div > form > div > div.md-card-actions.md-alignment-right > button').click()")
            sleep(2)
        browser.get(params['url'])

    elif params['application'] == 'bareos-dir':
        browser.find_element_by_xpath("//input[@name='consolename']").send_keys(params['user'])
        browser.find_element_by_xpath("//input[@name='password']").send_keys(params['password'])
        # browser.find_element_by_xpath("//input[@name='password']").send_keys(Keys.ENTER)
        browser.execute_script("document.querySelector('#submit').click()")

    elif params['application'] == 'targetprocess':
        browser.find_element_by_xpath("//input[@name='Username']").send_keys(params['user'])
        browser.find_element_by_xpath("//input[@name='Password']").send_keys(params['password'])
        # browser.find_element_by_xpath("//input[@type='submit']").click()
        browser.execute_script("document.querySelector('#loginPanel > div > div.login-fields > div.login-controls-wrap > div:nth-child(1) > input').click()")

        while not check_exists_by_xpath(browser,"//button[@class='i-role-board-tooltip tau-v-collapser']"):
          sleep(2)
        # browser.find_element_by_xpath("//button[@class='i-role-board-tooltip tau-v-collapser']").click()
        browser.execute_script("document.querySelector('body > div.tau-app.i-role-application.i-browser_engine_webkit > div > aside > div:nth-child(1) > div.tau-pane-collapser > button').click()")

    elif params['application'] == 'default':
        pass

    return browser
