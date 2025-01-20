from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
import csv
from RPA.PDF import PDF
import time

@task
def order_robots_from_RobotSpareBin():
    """Insert the function's here to call"""
    browser.configure(
        slowmo=100,
    )
    open_robot_order_website()
    close_annoying_modal()
    # download_csv_file()
    fill_form_with_csv_data()
    # collect_results()
    # export_as_pdf()
    # log_out()
    time.sleep(20)

def open_robot_order_website():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order/")
    
def close_annoying_modal():
    page = browser.page()
    page.click("text=OK")

def fill_and_submit_sales_orders(sales_rep):
    """Fills in the sales data and click the 'Submit' button"""
    page = browser.page()
    page.fill('xpath=//label[contains(text(), "Legs")]/following-sibling::input', str(sales_rep["Legs"]))
    page.fill("#address", sales_rep["Address"])
    page.select_option("#head", str(sales_rep["Head"]))
    page.click(f'xpath=//input[@name="body"][contains(@value, "{sales_rep["Body"]}")]')
    page.click("text=preview")
    page.click("text=order")


def download_csv_file():
    """Downloads csv file from the given URL"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)

def fill_form_with_csv_data():
    """Load the CSV file into a table"""
    # Open the CSV file
    with open("orders.csv", mode="r") as file:
        # Create a CSV reader object
        reader = csv.DictReader(file)
        
        # Loop through each row
        for row in reader:
            fill_and_submit_sales_orders(row)  # Pass the row as a dictiona

def collect_results():
    """Take a screenshot of the page"""
    page = browser.page()
    page.screenshot(path="output/sales_summary.png")

def export_as_pdf():
    """Export the data to a pdf file"""
    page = browser.page()
    sales_results_html = page.locator("#sales-results").inner_html()

    pdf = PDF()
    pdf.html_to_pdf(sales_results_html, "output/sales_results.pdf")

def log_out():
    """Presses the 'Log out' button"""
    page = browser.page()
    page.click("text=Log out")