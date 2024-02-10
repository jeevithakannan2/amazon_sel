import asyncio
import random
from time import sleep
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


class Amazon:
    async def random_delay(self):
        # Introduce a random delay between 0.5 and 2 seconds
        return random.uniform(0.5, 2.5)
    
    def captcha(self,url,captcha):
        
        print("Input captcha")
        await page.type("//input[@type='text']", input("Captcha: "))

        await page.click('//*[@id="a-autoid-0"]/span/input')
        self.run(url)
        
    async def run(self,url):

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            # Apply stealth options to the context
            page = await context.new_page()

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
            await page.wait_for_load_state("load")
                  
            if 'captcha' in await page.content():
                print("captcha")
                img = page.locator("//img[@alt='captcha']")

                await img.screenshot(path='captcha.png')

                return self.captcha()

            await page.wait_for_selector("//div[@aria-label='Other UPI Apps']")

            await asyncio.sleep(await self.random_delay())

            await page.click("//div[@aria-label='Other UPI Apps'][.//input[@type='radio']]")

            await page.type("//input[@placeholder='Enter UPI ID']",'ksjeevithakannan123@okicici', delay=1)

            await page.click("//input[@name='ppw-widgetEvent:ValidateUpiIdEvent']")

            await asyncio.sleep(await self.random_delay())

            await page.click("//input[@name='ppw-widgetEvent:SetPaymentPlanSelectContinueEvent']")

            await page.wait_for_selector("//span[@id='subtotals-marketplace-spp-bottom']")

            prices = {}
            items_price = await page.text_content("//tr[.//td[contains(., 'Items')]]//td[contains(@class, 'a-text-right')]")
            delivery_price = await page.text_content("//tr[.//td[contains(., 'Delivery')]]//td[contains(@class, 'a-text-right')]")
            total_price = await page.text_content("//tr[.//td[contains(., 'Total')]]//td[contains(@class, 'a-text-right')]")
            promotion_price = await page.text_content("//tr[.//td[contains(., 'Promotion')]]//td[contains(@class, 'a-text-right')]")
            order_total_price = await page.text_content("//tr[.//td[contains(., 'Order')]]//td[contains(@class, 'a-text-right')]")

            # adding prices to the dictionary
            prices['items'] = items_price.strip()
            prices['delivery'] = delivery_price.strip()
            prices['total'] = total_price.strip()
            prices['promotion applied'] = promotion_price.strip()
            prices['order total'] = order_total_price.strip()

            print(prices)

            # Close the browser
            await browser.close()

            return prices