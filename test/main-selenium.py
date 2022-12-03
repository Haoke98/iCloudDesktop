import requests
from selenium.webdriver.chrome import webdriver

__HOME_ENDPOINT__ = "https://www.icloud.com.cn"
__SETUP_ENDPOINT__ = f"{__HOME_ENDPOINT__}/setup/ws/1"
driver = webdriver.WebDriver()
if __name__ == '__main__':
    driver.get(__HOME_ENDPOINT__)
    input("等待用户登陆，登陆完成以后，请按回车确认.....")
    driver.get(f"{__HOME_ENDPOINT__}/photos/")
    __params__ = {
        'clientBuildNumber': '17DHotfix5',
        'clientMasteringNumber': '17DHotfix5',
        'ckjsBuildVersion': '17DProjectDev77',
        'ckjsVersion': '2.0.5',
        'clientId': '49AEE93C-72CB-11ED-BF93-0E17666B02AF',
        'dsid': '20293379486'
    }
    __cookies__ = {
        "X-APPLE-WEBAUTH-HSA-LOGIN": driver.get_cookie("X-APPLE-WEBAUTH-HSA-LOGIN"),
        "X-APPLE-WEBAUTH-USER": driver.get_cookie("X-APPLE-WEBAUTH-USER")
    }
    resp = requests.get(f"{__SETUP_ENDPOINT__}/listDevices", )

    # driver.find_elements(by=By.XPATH, value='//div[@class="grid-item"]')
    print("结束了")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
