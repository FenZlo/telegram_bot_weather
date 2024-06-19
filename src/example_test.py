from httpx import request
from playwright.sync_api import Playwright, sync_playwright


MY_LOGIN = "119998271"


def run(pw: Playwright):
    chrome = pw.chromium
    browser = chrome.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.gismeteo.ru", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    page.locator(".search-label").locator("input").fill("Екатеринбург")
    page.wait_for_timeout(1000)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3000)
    weather = (
        page.locator(".weathertab-wrap")
        .first.locator(".weather")
        .locator(".weather-value")
        .locator(".unit_temperature_c")
        .text_content()
    )
    browser.close()
    request(
        method="post",
        url="https://api.telegram.org/bot7258804911:AAE5vr8rWl2eexJq4aS1gUmyMmry-P5ODCI/sendMessage",
        json={"chat_id": MY_LOGIN, "text": f"Погода в Екатеринбурге: {weather}°C"},
    )


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
