import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        # Login
        await page.goto("http://127.0.0.1:8000/login/")
        await page.fill('input[name="username"]', "testuser")
        await page.fill('input[name="password"]', "password123")
        await page.click('button[type="submit"]')
        await page.wait_for_url("**/game/**")

        # Home (Novice Hall or Square)
        await page.screenshot(path="novice_hall.png", full_page=True)
        print("Saved novice_hall.png")

        # Character page
        await page.goto("http://127.0.0.1:8000/game/users/character/")
        await page.screenshot(path="character_page_v2.png", full_page=True)
        print("Saved character_page_v2.png")

        # Inventory
        await page.goto("http://127.0.0.1:8000/game/items/inventory/")
        await page.screenshot(path="inventory_v2.png", full_page=True)
        print("Saved inventory_v2.png")

        # Market
        await page.goto("http://127.0.0.1:8000/game/items/market/")
        await page.screenshot(path="market_v2.png", full_page=True)
        print("Saved market_v2.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
