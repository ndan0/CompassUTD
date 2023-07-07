import io
import re

import fitz
import requests
from bs4 import BeautifulSoup


def extract_course_description(course_id: str) -> str:
    """

    Args:
        course_id (str): 2-4 letter and 4 digits course id

    Returns:
        text data (str): content of the website in string format.
    """
    # Remove non-alphanumeric characters
    course = "".join(e for e in course_id if e.isalnum())
    # Make a request to the course catalog
    response = requests.get(
        f"https://catalog.utdallas.edu/2023/undergraduate/courses/{course}"
    )
    soup = BeautifulSoup(response.content, "html.parser")

    div_element = soup.find(
        "div", id="bukku-page"
    )  # The description in <div id="bukku-page">
    combined_desc = ""
    if div_element:
        # Extract the text content from the div element
        combined_desc += div_element.text.strip()

    if len(combined_desc) <= 1:
        return "The course is not offered in 2023."

    return combined_desc


def extract_text_from_html(html) -> str:
    # Extract text from HTML
    soup = BeautifulSoup(html, "html.parser")
    # Remove header, footer, nav, breadcrumb
    elements_to_remove = ["header", "footer", "nav", "div.breadcrumb"]

    for element_selector in elements_to_remove:
        try:
            elements = soup.find_all(element_selector)
            for element in elements:
                element.decompose()
        except AttributeError:
            pass

    # Remove div with class or id containing "nav", "header", "footer", "breadcrumb"
    for element in soup.find_all(
            re.compile(r"div"), class_=re.compile(r"nav|head|foot|breadcrumb")
    ):
        element.decompose()

    for element in soup.find_all(
            re.compile(r"div"), id=re.compile(r"nav|head|foot|breadcrumb")
    ):
        element.decompose()

    return soup.get_text()


def extract_text_from_pdf(pdf) -> str:
    pdf_file = io.BytesIO(pdf)
    text = ""
    with fitz.open(stream=pdf_file, filetype="pdf") as doc:
        for page in doc:
            text.join(" ".join(page.get_text()))
    return text


def extract_text_from_website(url: str) -> str:
    """_summary_

    Args:
        url (str): link contain utdallas.edu website

    Raises:
        ValueError: Invalid URL if the URL is not from utdallas.edu
        HTTPException: Error occurred while accessing URL.

    Returns:
        text data (str): content of the website in string format.

    """

    if not re.search(r"utdallas.edu", url):
        # Raise an error if the URL is not from utdallas.edu
        raise ValueError("Invalid URL")

    if re.search(r"catalog.utdallas.edu", url):
        # Check if the url contain catalog.utdallas.edu, then append /makepdf to the url to turn it into pdf

        if not re.search(r"makepdf", url):
            url += "/makepdf"

    response = requests.get(url, verify=False)

    if not response:
        raise "Error occurred while accessing content"

    text = ""
    if response.headers.get("Content-Type") == "application/pdf":
        # Extract text from PDF
        text = extract_text_from_pdf(response.content)
    else:
        text = extract_text_from_html(response.content)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)
    # Remove underscores
    text = re.sub(r"_", "", text)

    return text[: 8192 * 2]  # Limit the text to 16KB due to the limit of PaLM 2 token
