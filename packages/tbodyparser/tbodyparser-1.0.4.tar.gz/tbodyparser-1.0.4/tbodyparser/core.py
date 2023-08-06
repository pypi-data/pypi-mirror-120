from pyquery import PyQuery
from selenium.webdriver.remote.webdriver import WebDriver

from .base import Tbody


def parse_tbody(
        tbody_selector: str,
        driver: WebDriver = None,
        page_source: str = None
) -> Tbody:
    """Parse table body.

    Args:
        tbody_selector: css selector of target table element.
        driver: selenium web driver.
        page_source: parse table directly from page_source when given.

    Returns:
        a Tbody object.

    Usage:
        tbody = parse(tbody_selector="#tbody", driver=driver)
    """

    if not (driver or page_source):
        raise TypeError("expected at least one of these two arguments: 'driver', 'page_source'")
    if page_source:
        tbody_outer_html = PyQuery(page_source).find(tbody_selector).outer_html()
    else:
        tbody_outer_html = driver.find_element_by_css_selector(tbody_selector).get_attribute("outerHTML")
    tbody_element = PyQuery(tbody_outer_html)
    tbody = Tbody(selector=tbody_selector, element=tbody_element)
    return tbody
