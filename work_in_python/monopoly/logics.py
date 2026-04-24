import re
import time


last_action_time = 0


def should_buy(state):
    pos = state.get_my_position()
    field = state.get_my_field()

    if not field or field["type"] != "field":
        return False

    owner = state.get_owner(pos)

    if owner is not None:
        return False

    money = state.get_me()["money"]


    if money > 3000:
        return True

    return False


def click_button(page, text):
    try:
        page.locator(f"div._action:has-text('{text}')").first.click(timeout=500)
    except:
        print("CLICK FAIL:", text)


def click_contains(page, text):
    try:
        page.locator(f"div._action:has-text('{text}')").first.click(timeout=500)
    except:
        print("CLICK FAIL:", text)


def exists(locator):
    try:
        return locator.first.is_visible(timeout=100)
    except:
        return False


def detect_actions(page):
    try:
        root = page.locator(".TableAction")

        if root.count() == 0:
            return {}

        text = root.inner_text()

        return {
            "roll": "Бросить кубики" in text,
            "buy": "Купить за" in text,
            "auction": "На аукцион" in text,
            "pay": "Заплатить" in text,
            "accept": "Принять" in text,
            "decline": "Отклонить" in text,
            "refuse": "Отказаться" in text
        }

    except:
        return {}
        

def parse_number(text):
    num = re.findall(r"[\d,]+", text)[0]
    return int(num.replace(",", ""))

def handle_actions(page, state, actions):
    global last_action_time

    if not state.is_my_turn_now():
        return

    now = time.time()

    # защита от спама (1.5 сек)
    if now - last_action_time < 1.5:
        return

    # --- 1. ROLL ---
    if actions.get("roll"):
        print("DO: ROLL")
        time.sleep(3)
        click_button(page, "Бросить кубики")
        last_action_time = now
        return

    # --- 2. BUY ---
    if actions.get("buy"):
        decision = should_buy(state)

        if decision:
            print("DO: BUY")
            time.sleep(3)
            click_contains(page, "Купить за")
        else:
            print("DO: AUCTION")
            time.sleep(3)
            click_button(page, "На аукцион")
        last_action_time = now
        return

    # --- 3. PAY ---
    if actions.get("pay"):
        print("DO: PAY")
        click_contains(page, "Заплатить")
        last_action_time = now
        return

    # --- 4. TRADE ---
    if actions.get("accept"):
        print("DO: ACCEPT")
        click_button(page, "Принять")
        last_action_time = now
        return

    if actions.get("decline"):
        print("DO: DECLINE")
        click_button(page, "Отклонить")
        last_action_time = now
        return

    print("NO ACTION")