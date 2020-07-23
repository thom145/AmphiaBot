import datetime
import requests
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options


# text_file containing username and password
with open('Schedule/text_file.txt', 'r') as data:
    user_info = data.readlines()
    user_info = [info.strip() for info in user_info]


def download_schedule(get_month):
    """Download the schedule from https://extranet.amphia.nl and save file
    as csv in /Rooster """

    def log_in_first(element_name, element_id):
        """Log in to website with MobilePass."""
        # enters username(==user_info[0])
        driver.find_element_by_name(element_name[0]).send_keys(user_info[0])
        # enters password(==user_info[1])
        driver.find_element_by_name(element_name[1]).send_keys(user_info[1])
        # enters password check (==user_info[2])
        driver.find_element_by_name(element_name[2]).send_keys(user_info[1])
        # clicks log on button
        driver.find_element_by_id(element_id).click()

    def log_in(element_name, element_id):
        """Log in to website."""
        # enters username(==user_info[0])
        driver.find_element_by_name(element_name[0]).send_keys(user_info[0])
        # enters password(==user_info[1])
        driver.find_element_by_name(element_name[1]).send_keys(user_info[1])
        # clicks log on button
        driver.find_element_by_id(element_id).click()

    def set_month(path, month):
        """Set month and return schedule of that month in a pop-up frame."""
        # clear field
        driver.find_element_by_xpath(path).clear()
        time.sleep(2)
        # select field
        driver.find_element_by_xpath(path).click()
        time.sleep(2)
        # insert month in field
        driver.find_element_by_xpath(path).send_keys(month)
        time.sleep(2)
        # click random point to process month
        driver.find_element_by_id("ParametersGridReportViewer_ctl04").click()
        time.sleep(4)

    def create_url(url):
        """Create url with unique code and return url."""
        split_url_on_slash = url.split("/")  # splits current url on slash
        part1 = 'https://extranet.amphia.nl/' + split_url_on_slash[3]

        split_url_on_equal = url.split("=")  # splits current url on equal
        url_id = split_url_on_equal[1:3]
        url_id = '='.join(url_id)

        url_code = split_url_on_equal[2][:4]
        url_control_id = split_url_on_equal[7]
        part2 = "/Reserved.ReportViewerWebControl.axd?ReportSession=" + \
                url_id + \
                "=False&UICulture=" + \
                url_code + \
                "&UICultureOverrides=False&ReportStack=1&ControlID=" + \
                url_control_id + \
                "=Export&FileName=Master+schedule+ESS_nl-NL&ContentDisposition=OnlyHtmlInline&Format=EXCEL"

        url_to_download = part1 + part2
        return url_to_download

    # get current date
    now = datetime.datetime.now()
    # create a dictionary with the right month format
    months = {'januari': ["1-1-" + str(now.year + 1), "2-1-" + str(now.year + 1)],
              'februari': ["2-1-" + str(now.year), "3-1-" + str(now.year)],
              'maart': ["3-1-" + str(now.year), "4-1-" + str(now.year)],
              'april': ["4-1-" + str(now.year), "5-1-" + str(now.year)],
              'mei': ["5-1-" + str(now.year), "6-1-" + str(now.year)],
              'juni': ["6-1-" + str(now.year), "7-1-" + str(now.year)],
              'juli': ["7-1-" + str(now.year), "8-1-" + str(now.year)],
              'augustus': ["8-1-" + str(now.year), "9-1-" + str(now.year)],
              'september': ["9-1-" + str(now.year), "10-1-" + str(now.year)],
              'oktober': ["10-1-" + str(now.year), "11-1-" + str(now.year)],
              'november': ["11-1-" + str(now.year), "12-1-" + str(now.year)],
              'december': ["12-1-" + str(now.year), "1-1-" + str(now.year + 1)]}

    # get month format for specific month
    start_month = months[get_month][0]
    end_month = months[get_month][1]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    download_dir = "/Users/thomsuykerbuyk/GitHub/AmphiaBot/schedule_info"
    preferences = {"download.default_directory": download_dir,
                   "directory_upgrade": True,
                   "safebrowsing.enabled": True}
    chrome_options.add_experimental_option("prefs", preferences)

    # get chromedriver from current wd
    chrome_driver = "Schedule/chromedriver"
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)  # create instance driver
    driver.get('https://extranet.amphia.nl/default.aspx')  # go to webiste

    # first login https://auth.amphia.nl/vpn/tmindex.html
    log_in_first(['login', 'passwd', 'passwd1'], 'Log_On')
    # second login https://extranet.amphia.nl/(S(j2mbd3jwjpcgcnyku2z0lv45))/logon.aspx
    log_in(['ctl00$ContentPlaceHolder1$Username', 'ctl00$ContentPlaceHolder1$Password'],
           'ctl00_ContentPlaceHolder1_Button1')
    time.sleep(4)

    # click on "Rooster" so a menu will open
    element1 = driver.find_element_by_xpath("(//DIV[@qxselectable='off'])[29]")
    ActionChains(driver).move_to_element(element1).click().perform()
    time.sleep(3)

    # from the <ul> menu click "Master schedule ESS"
    element2 = driver.find_element_by_xpath("//DIV[@qxselectable='off'][text()='Master schedule ESS']")
    ActionChains(driver).move_to_element(element2).click().perform()
    time.sleep(5)

    # switch to the pop-up frame
    iframe = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div/div[2]/iframe")
    driver.switch_to.frame(iframe)
    time.sleep(2)

    # insert the start of the month into the field
    set_month("//INPUT[@id='ReportViewer_ctl04_ctl03_txtValue']", start_month)
    # insert the end of the month into the field
    set_month("//INPUT[@id='ReportViewer_ctl04_ctl05_txtValue']", end_month)

    # click to show the schedule for the desired month
    driver.find_element_by_xpath("//INPUT[@id='ReportViewer_ctl04_ctl00']").click()
    time.sleep(10)

    # get description from image (for url to download)
    img = driver.find_element_by_xpath("//IMG[@onload='this.fitproportional=true;this.pv=0;this.ph=0;']")
    # save the src of the image to the variable url
    url = img.get_attribute('src')

    # create the url from which to download
    new_url = create_url(url)

    # get cookies from current website
    cookies_list = driver.get_cookies()
    cookies_dict = {}
    for cookie in cookies_list:
        cookies_dict[cookie['name']] = cookie['value']

    # get the content from the website and store it in a new_file
    send_request = requests.get(url=new_url, cookies=cookies_dict, allow_redirects=True, stream=True)
    with open('Roosters/' + get_month + '/' + get_month + '.xls', 'wb') as file:
        file.write(send_request.content)

    driver.quit()
