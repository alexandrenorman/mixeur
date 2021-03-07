# -*- coding: utf-8 -*-
import json
import base64

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from django.http import HttpResponse


def get_pdf_in_base64(browser, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % browser.session_id
    url = browser.command_executor._url + resource
    body = json.dumps({"cmd": cmd, "params": params})
    response = browser.command_executor._request("POST", url, body)
    if "status" in response and response["status"]:
        raise Exception(response.get("value"))
    return response.get("value")


def build_pdf_stream_from(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--user-data=/home/django/tmp/ChromeProfile")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=PdfGenerator")
    options.add_argument("--no-margins")

    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    # TODO: Add header caption to catch and send 403 error and avoid blank pdf response
    # https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
    timeout = 10
    try:
        element_is_present = EC.presence_of_element_located((By.ID, "pdfLoaded"))
        WebDriverWait(browser, timeout).until(element_is_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    # return the generated pdf
    # https://chromedevtools.github.io/devtools-protocol/tot/Page#method-printToPDF
    result = get_pdf_in_base64(
        browser,
        "Page.printToPDF",
        {
            "landscape": False,
            "printBackground": True,
            "marginTop": 0,
            "marginBottom": 0,
            "marginLeft": 0,
            "marginRight": 0,
            "preferCSSPageSize": True,
            "displayHeaderFooter": True,
            "headerTemplate": "",
            # Use css top directive to offset the footer because of a weird behavior of the margin
            "footerTemplate": '<div style="position: relative; width:100%; top: 3.5mm; margin: 0; padding: 1mm 3mm; color: #666666; text-align: right; font-size: 2mm;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',  # noqa E501
        },
    )
    browser.close()

    response = HttpResponse(
        base64.b64decode(result["data"]), content_type="application/pdf"
    )
    response["Content-Disposition"] = 'attachment; filename="diagnostic.pdf"'

    return response
