import os
import traceback
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import uuid

class Amazon:
    def __init__(self):
        self.page = None
        self.count = None
        self.uuidn = str(uuid.uuid4())
        self.captcha_count = 0
    async def captcha_inp(self, captcha):
        print("Input captcha")

        page = self.page

        await page.fill("//input[@type='text']", captcha)
        await page.click('//*[@id="a-autoid-0"]/span/input')

        if 'captcha' in await page.content():
            return {"msg": "Wrong captcha"}
        else:
            return {"msg": "captcha entered"}

    async def captcha(self):
        page = self.page
        print("captcha")
        img = page.locator("//img[@alt='captcha']")
        with open(f'captcha_{self.uuidn}.txt', 'w', ) as f:
            f.write(str(self.captcha_count))

        await img.screenshot(path=f'captcha_{self.uuidn}.png')
        print("Saved captcha")
        await page.wait_for_selector("//*[@id='a-autoid-0']/span/input", state='attached')
        await page.wait_for_function('() => document.readyState === "complete"')

        if 'captcha' in await page.content():
            self.captcha_count += 1
            await self.captcha()
        else:
            return

    async def run(self, url):
        async with async_playwright() as p:

            try:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()

                self.page = await context.new_page()
                page = self.page
                await stealth_async(page)

                await page.goto(url, wait_until='domcontentloaded')
                await page.click("//input[@id='buy-now-button']")

                await page.fill("//input[@type='email']", '9894789409')

                await page.click("//input[@id='continue']")

                await page.fill("//input[@type='password']", 'jeeva2005')

                await page.click("//input[@id='signInSubmit']")
                await page.wait_for_timeout(2000)
                await page.wait_for_function('() => document.readyState === "complete"')
                
                if 'captcha' in await page.content():
                    await self.captcha()

                if 'Choose special delivery options' in await page.content():
                    print("Spl delivery option")
                    await page.click("//span[contains(@data-a-tooltip-button-blocker,'options-continue-button')]")

                # await page.wait_for_selector("//input[@type='password']")
                #
                # await page.fill("//input[@type='password']", '123')
                # await page.set_checked("//input[@type='checkbox']", True)

                await page.wait_for_selector("//div[@aria-label='Other UPI Apps']")

                await page.click("//div[@aria-label='Other UPI Apps'][.//input[@type='radio']]")

                await page.fill("//input[@placeholder='Enter UPI ID']", 'ksjeevithakannan123@okicici')

                await page.click("//input[@name='ppw-widgetEvent:ValidateUpiIdEvent']")

                await page.click("//input[@name='ppw-widgetEvent:SetPaymentPlanSelectContinueEvent']", delay=5)

                try:
                    await page.wait_for_selector("//*[@id='prime-interstitial-nothanks-button']", state='visible', timeout=5000)
                    await page.evaluate('document.querySelector("#prime-interstitial-nothanks-button").click()')

                except Exception:
                    pass
                await page.wait_for_selector("//span[@id='subtotals-marketplace-spp-bottom']", timeout=45000)

                data = {}
                rows = await page.query_selector_all("//*[@id='subtotals-marketplace-table']/tbody/tr")
                for row in rows:
                    cells = await row.query_selector_all("td")

                    if len(cells) == 2:
                        key = await cells[0].inner_text()
                        key.replace('\n', '', ).strip()

                        value = await cells[1].inner_text()
                        value.replace('\n', '').strip()

                        data[key] = value

                print(data)

                await browser.close()

                return data



            # prices = {}

            # input()
            # try:
            #     items_price = await page.text_content(
            #         "//tr[.//td[contains(., 'Items')]]//td[contains(@class, 'a-text-right')]", timeout=1)
            #     order_total_price = await page.text_content(
            #         "//tr[.//td[contains(., 'Order')]]//td[contains(@class, 'a-text-right')]", timeout=1)
            #     delivery_price = await page.text_content(
            #         "//tr[.//td[contains(., 'Delivery')]]//td[contains(@class, 'a-text-right')]", timeout=1)
            #     total_price = await page.text_content(
            #         "//tr[.//td[contains(., 'Total')]]//td[contains(@class, 'a-text-right')]", timeout=1)
            #     promotion_price = await page.text_content(
            #         "//tr[.//td[contains(., 'Promotion')]]//td[contains(@class, 'a-text-right')]", timeout=1)
            #
            # except Error:
            #     pass
            # # adding prices to the dictionary
            # try:
            #     prices['items'] = items_price.strip()
            #     prices['delivery'] = delivery_price.strip()
            #     prices['total'] = total_price.strip()
            #     prices['promotion applied'] = promotion_price.strip()
            #     prices['order total'] = order_total_price.strip()
            # except Exception:
            #     pass
            #
            # print(prices)

            # Close the browser


            except Exception as e:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Error")
                html = await page.content()
                with open('error.html', 'w', encoding='UTF-8') as f:
                    f.write(html)
                with open('error.txt', 'a') as f1:
                    f1.write(f"\n{timestamp} : " + str(e) + '\n')
                    traceback.print_exc(file=f1)


    def __del__(self):
        try:
            os.remove(f'captcha_{self.uuidn}.txt')
            os.remove(f'captcha_{self.uuidn}.png')
        except FileNotFoundError:
            pass
