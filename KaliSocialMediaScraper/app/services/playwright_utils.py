import random
import asyncio
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

USER_AGENTS = [
    # A sample of common user agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
]

PROXIES = []  # Fill with proxy URLs if needed, or load from config/env

async def get_browser(proxy: Optional[str] = None) -> Browser:
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    return browser

async def get_context(browser: Browser, user_agent: Optional[str] = None, proxy: Optional[str] = None) -> BrowserContext:
    if not user_agent:
        user_agent = random.choice(USER_AGENTS)
    context_args = {"user_agent": user_agent}
    if proxy:
        context_args["proxy"] = {"server": proxy}
    context = await browser.new_context(**context_args)
    return context

async def get_page(context: BrowserContext) -> Page:
    page = await context.new_page()
    return page

async def random_delay(min_delay: float = 1.0, max_delay: float = 3.0):
    await asyncio.sleep(random.uniform(min_delay, max_delay)) 