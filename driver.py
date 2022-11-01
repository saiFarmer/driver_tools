import zipfile
import io
import re
import logging

import requests
import xmltodict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.getLogger()


class DriverTools:
    @classmethod
    def update_driver(self, e: str, version_list: list = None) -> None:
        logging.info(e)
        version_list = version_list
        try:
            version = re.findall("is ((!?.*?) )", str(e))[1][1]
            logging.info(version)
            v_lookup = [x for x in version_list if version[:3] in x[:3]]
            logging.info(f"v found {v_lookup[-1]}")
            url = f"https://chromedriver.storage.googleapis.com/{v_lookup[-1]}/chromedriver_win32.zip"
            logging.info(f"requesting zip from: {url}")
            r = requests.get(url, allow_redirects=True)
            zip_file_object = zipfile.ZipFile(io.BytesIO(r.content))
            first_file = zip_file_object.namelist()[0]

            open("./chromedriver.exe", "wb+").write(
                zip_file_object.open(first_file).read()
            )
            logging.info("successfully added driver")
        except Exception as e:
            logging.info(f"failed to get chrome driver{e}")

    @classmethod
    def start_driver(self, version_list: list = None):
        # sets local variables
        path = r"./chromedriver.exe"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = False
        try:
            driver = webdriver.Chrome(executable_path=path, options=chrome_options)
            return driver
        except Exception as e:
            if driver:
                driver.close()
            self.update_driver(e, version_list=version_list)
            return self.start_driver(version_list=version_list)
        

    @classmethod
    def get_driver_versions(self):
        driver_versions = requests.get("https://chromedriver.storage.googleapis.com/")
        data_dict = xmltodict.parse(driver_versions.text)
        versions = [x["Key"] for x in data_dict["ListBucketResult"]["Contents"]]
        version_list = [
            x.split("/")[0] for x in versions if x[0] in [str(y) for y in range(0, 10)]
        ]
        return version_list
        
        
        
        
        
if __name__ == "__main__":
    version_list = DriverTools.get_driver_versions()
    driver = DriverTools.start_driver(version_list=version_list)
    print(driver)
    if driver == None:
        logging.info("error")