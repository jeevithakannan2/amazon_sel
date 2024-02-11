import asyncio
import random
from time import sleep
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


class Amazon:
    def __init__(self):
        self.page = None

    #
    async def random_delay(self):
        # Introduce a random delay between 0.5 and 2 seconds
        return random.uniform(0.5, 2.5)

    async def captcha_inp(self, captcha):
        print("Input captcha")

        page = self.page

        await page.type("//input[@type='text']", captcha)
        await page.click('//*[@id="a-autoid-0"]/span/input')

        await page.wait_for_load_state("networkidle0")
        if 'captcha' in await page.content():
            return {"msg": "Wrong captcha"}
        else:
            return {"msg": "captcha entered"}

    async def captcha(self):
        page = self.page
        print("captcha")
        img = page.locator("//img[@alt='captcha']")

        await img.screenshot(path='captcha.png')
        url = page.url.strip()
        print(url)
        page.wait_for_timeout(20000)
        if 'captcha' in await page.content():
            await self.captcha()
        else:
            return

    async def run(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            # Apply stealth options to the context
            self.page = await context.new_page()
            page = self.page
            await stealth_async(page)

            # Navigate to a website
            await page.goto(url)
            await page.wait_for_load_state("load")
            await asyncio.sleep(await self.random_delay())
            await page.click("//input[@id='buy-now-button']")

            await page.type("//input[@type='email']", '9894789409', delay=1.5)

            await page.click("//input[@id='continue']")

            await asyncio.sleep(await self.random_delay())
            await page.type("//input[@type='password']", 'jeeva2005', delay=1.5)

            await page.click("//input[@id='signInSubmit']")
            await asyncio.sleep(await self.random_delay())

            await page.wait_for_timeout(10000)
            if 'captcha' in await page.content():
                await self.captcha()

            print("Sleep Over")

            if 'special delivery' in await page.content():
                print("Spl delivery option")
                await page.click("//span[contains(@data-a-tooltip-button-blocker,'options-continue-button')]")



            await page.wait_for_selector("//div[@aria-label='Other UPI Apps']")

            await asyncio.sleep(await self.random_delay())

            await page.click("//div[@aria-label='Other UPI Apps'][.//input[@type='radio']]")

            await page.type("//input[@placeholder='Enter UPI ID']", 'ksjeevithakannan123@okicici', delay=1)

            await page.click("//input[@name='ppw-widgetEvent:ValidateUpiIdEvent']")

            await asyncio.sleep(await self.random_delay())

            await page.click("//input[@name='ppw-widgetEvent:SetPaymentPlanSelectContinueEvent']")

            await page.wait_for_timeout(7500)
            if 'Prime' in await page.content():
                await page.click("//*[@id='prime-interstitial-nothanks-button']")


            await page.wait_for_selector("//span[@id='subtotals-marketplace-spp-bottom']")

            prices = {}
            try:
                items_price = await page.text_content(
                    "//tr[.//td[contains(., 'Items')]]//td[contains(@class, 'a-text-right')]", timeout=1000)
                delivery_price = await page.text_content(
                    "//tr[.//td[contains(., 'Delivery')]]//td[contains(@class, 'a-text-right')]", timeout=1000)
                total_price = await page.text_content(
                    "//tr[.//td[contains(., 'Total')]]//td[contains(@class, 'a-text-right')]", timeout=1000)
                promotion_price = await page.text_content(
                    "//tr[.//td[contains(., 'Promotion')]]//td[contains(@class, 'a-text-right')]", timeout=1000)
                order_total_price = await page.text_content(
                    "//tr[.//td[contains(., 'Order')]]//td[contains(@class, 'a-text-right')]", timeout=1000)
            except Exception:
                pass
            # adding prices to the dictionary
            try:
                prices['items'] = items_price.strip()
                prices['delivery'] = delivery_price.strip()
                prices['total'] = total_price.strip()
                prices['promotion applied'] = promotion_price.strip()
                prices['order total'] = order_total_price.strip()
            except Exception:
                pass

            print(prices)

            # Close the browser
            await browser.close()

            return prices
