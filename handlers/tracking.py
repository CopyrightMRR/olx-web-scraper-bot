import logging
import html
import random

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
import aiohttp

import asyncio
from database.repositories.tracker import TrackerRepo
from handlers.tracker_state import tracker_tasks, redis_client

router = Router()

SEEN_TTL_SECOND = 60 * 60 * 24 * 30

PAGE_LIMIT = 40
MAX_PAGES_PER_POLL = 5
BASE_BACKOFF_SECONDS = 30
MAX_BACKOFF_SECONDS = 60 * 60



async def check_offer(tracker_id: int, offer_id: str):
    key = f"tracker:{tracker_id}:seen"

    is_new = await redis_client.sadd(key, offer_id) == 1

    await redis_client.expire(key, SEEN_TTL_SECOND)
    return is_new


class Forms(StatesGroup):
    query = State()


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:152.0) Gecko/20100101 Firefox/152.0',
    'Accept': 'application/json',
    'Accept-Language': 'uk',
    'Content-Type': 'application/json',
    'Origin': 'https://www.olx.ua',

}

def build_query_payload(query: str, offset: int) -> dict:
    return {'query': 'query ListingSearchQuery(\n  $searchParameters: [SearchParameter!] = []\n  $fetchPayAndShip: Boolean = false\n  $searchOptions: SearchOptions\n) {\n  clientCompatibleListings(searchParameters: $searchParameters, searchOptions: $searchOptions) {\n    __typename\n    ... on ListingSuccess {\n      __typename\n      data {\n        _nodeId\n        id\n        location {\n          city {\n            id\n            name\n            normalized_name\n            _nodeId\n          }\n          district {\n            id\n            name\n            normalized_name\n            _nodeId\n          }\n          region {\n            id\n            name\n            normalized_name\n            _nodeId\n          }\n        }\n        last_refresh_time\n        delivery {\n          rock {\n            active\n            mode\n            offer_id\n          }\n        }\n        created_time\n        category {\n          id\n          type\n          _nodeId\n        }\n        contact {\n          courier\n          chat\n          name\n          negotiation\n          phone\n        }\n        business\n        omnibus_pushup_time\n        photos {\n          link\n          height\n          rotation\n          width\n        }\n        promotion {\n          highlighted\n          top_ad\n          options\n          premium_ad_page\n          urgent\n          b2c_ad_page\n          seller_badge_x_years_with_olx\n        }\n        protect_phone\n        shop {\n          subdomain\n        }\n        title\n        status\n        url\n        user {\n          id\n          uuid\n          _nodeId\n          about\n          b2c_business_page\n          banner_desktop\n          banner_mobile\n          company_name\n          created\n          is_online\n          last_seen\n          logo\n          logo_ad_page\n          name\n          other_ads_enabled\n          photo\n          seller_type\n          social_network_account_type\n          verification {\n            status\n          }\n          businessProfiles {\n            services {\n              icon {\n                url\n                id\n              }\n              location {\n                city\n              }\n              businessName\n              foundationYear\n              templateName\n            }\n          }\n        }\n        offer_type\n        params {\n          key\n          name\n          type\n          value {\n            __typename\n            ... on GenericParam {\n              key\n              label\n            }\n            ... on CheckboxesParam {\n              label\n              checkboxParamKey: key\n            }\n            ... on PriceParam {\n              value\n              type\n              negotiable\n              label\n              currency\n              converted_value\n              converted_currency\n              arranged\n              budget\n            }\n            ... on SalaryParam {\n              from\n              to\n              arranged\n              converted_currency\n              converted_from\n              converted_to\n              currency\n              gross\n              type\n            }\n            ... on DynamicMultiChoiceCompatibilityListParam {\n              __typename\n            }\n            ... on ErrorParam {\n              message\n            }\n          }\n        }\n        description\n        external_url\n        partner {\n          code\n        }\n        map {\n          lat\n          lon\n          radius\n          show_detailed\n          zoom\n        }\n        safedeal {\n          allowed_quantity\n          weight_grams\n        }\n        valid_to_time\n        isGpsrAvailable\n        payAndShip @include(if: $fetchPayAndShip) {\n          sellerPaidDeliveryEnabled\n        }\n      }\n      metadata {\n        filter_suggestions {\n          clear_on_change\n          break_line\n          category\n          label\n          name\n          type\n          unit\n          values {\n            label\n            value\n          }\n          constraints {\n            type\n          }\n          search_label\n          option {\n            ranges\n            order\n            orderForSearch\n            fakeCategory\n          }\n        }\n        filters {\n          clear_on_change\n          break_line\n          category\n          label\n          name\n          type\n          unit\n          values {\n            label\n            value\n          }\n          constraints {\n            type\n          }\n          search_label\n          option {\n            ranges\n            order\n            orderForSearch\n            fakeCategory\n          }\n        }\n        x_request_id\n        search_id\n        total_elements\n        visible_total_count\n        source\n        search_suggestion {\n          url\n          type\n          changes {\n            category_id\n            city_id\n            distance\n            district_id\n            query\n            region_id\n            strategy\n            excluded_category_id\n          }\n        }\n        facets {\n          category {\n            id\n            count\n            label\n            url\n          }\n          category_id_1 {\n            count\n            id\n            label\n            url\n          }\n          category_id_2 {\n            count\n            id\n            label\n            url\n          }\n          category_without_exclusions {\n            count\n            id\n            label\n            url\n          }\n          category_id_3_without_exclusions {\n            id\n            count\n            label\n            url\n          }\n          city {\n            count\n            id\n            label\n            url\n          }\n          district {\n            count\n            id\n            label\n            url\n          }\n          owner_type {\n            count\n            id\n            label\n            url\n          }\n          region {\n            id\n            count\n            label\n            url\n          }\n          scope {\n            id\n            count\n            label\n            url\n          }\n        }\n        new\n        promoted\n      }\n      links {\n        first {\n          href\n        }\n        next {\n          href\n        }\n        previous {\n          href\n        }\n        self {\n          href\n        }\n      }\n    }\n    ... on ListingError {\n      __typename\n      error {\n        code\n        detail\n        status\n        title\n        validation {\n          detail\n          field\n          title\n        }\n      }\n    }\n  }\n}\n',
        'variables': {
            'searchParameters': [
                {
                    'key': f'{offset}',
                    'value': '0',
                },
                {
                    'key': 'limit',
                    'value': f'{PAGE_LIMIT}',
                },
                {
                    'key': 'query',
                    'value': f'{query}',
                },
                {
                    'key': 'sl',
                    'value': '19ef43213a1x71404155',
                },
            ],
            'fetchPayAndShip': True,
            'searchOptions': None,
        },
    }

def format_offer_message(offer: dict) -> str:
    title = html.escape(offer.get("title") or "")
    status = html.escape(offer.get("status") or "")
    url = offer.get("url") or ""

    price_label = "N/A"
    for param in offer.get("params") or []:
        value = param.get("value") or {}
        if value.get("__typename") == "PriceParam" and value.get("label"):
            price_label = html.escape(value["label"])
            break

    city = "N/A"
    location = offer.get("location") or {}
    city_data = location.get("city") or {}
    if city_data.get("name"):
        city = html.escape(city_data["name"])

    return (
        f"<ins>🚨 New Announcement 📜</ins>\n"
            f"<i>{title}</i>\n\n"
            f"<b>{status}</b>\n"
            f"<b>Price: {price_label}</b>\n"
            f"<b>Location: {city}</b>\n\n"
            f"{url}"
    )

async def fetch_offer_page(session: aiohttp.ClientSession, query: str, offset: int):
    payload = build_query_payload(query, offset)
    async with session.post('https://www.olx.ua/apigateway/graphql', json=payload, headers=headers) as response:
        response = await response.json()

        return response["data"]["clientCompatibleListings"]["data"] or []

async def pull_once(bot: Bot, chat_id: int, query: str, tracker_id: int, session: aiohttp.ClientSession):
    offset = 0
    for i in range(MAX_PAGES_PER_POLL):
        offers = await fetch_offer_page(session, query, offset)
        if not offers:
            break

        hit_seen_offer = False
        for offer in offers:
            is_new = await check_offer(tracker_id, offer["id"])
            if not is_new:
                hit_seen_offer = True
                break

            await bot.send_message(
                chat_id=chat_id,
                text=format_offer_message(offer),
                parse_mode="HTML"
                )
        if hit_seen_offer or len(offers) < PAGE_LIMIT:
            break

        offset += PAGE_LIMIT

async def tracker_loop(bot: Bot, chat_id: int, query: str, tracker_id: int):
    backoff = BASE_BACKOFF_SECONDS
    async with aiohttp.ClientSession() as session:
        while True:
            await asyncio.sleep(5)
            try:
                await pull_once(bot, chat_id, query, tracker_id, session)
                backoff = BASE_BACKOFF_SECONDS
            except Exception as exception:
                logging.error(exception)
                await bot.send_message(chat_id=chat_id, text="Site has some problem. Waiting before retry.")
                jitter = random.uniform(0, backoff * 0.25)
                await asyncio.sleep(jitter + backoff)
                backoff = min(backoff * 2, BASE_BACKOFF_SECONDS)







@router.message(F.text.lower() == "+ tracking")
async def start_tracker_query(message: Message, state: FSMContext):
    await message.answer("Write what you want to track")
    await state.set_state(Forms.query)

@router.message(Forms.query)
async def making_tracker(message: Message, tracker_repo: TrackerRepo, state: FSMContext):
    await state.update_data(query=message.text)
    await state.clear()
    await message.answer('Tracking added. You can see track, touch button "View tracker list"')
    query = str(message.text)
    chat_id = message.chat.id
    await tracker_repo.add_tracker(query, chat_id)


async def create_task(bot: Bot, tracker):
    if tracker.id in tracker_tasks:
        return

    task = asyncio.create_task(
        tracker_loop(bot, tracker.chat_id, tracker.query, tracker.id)
    )
    tracker_tasks[tracker.id] = task

