import re
import time


last_action_time = 0


def get_pay_amount(page):
    try:
        text = page.locator("div._action:has-text('Заплатить')").inner_text()
        return parse_number(text)
    except:
        return 0
    
def open_contract_with_teammate(page, state):
    try:
        me = state.get_me()
        if not me:
            return

        my_id = me["user_id"]
        my_team = me["team"]

        cards = page.locator(".table-body-players-card-body")

        players = list(state.players.values())

        for i in range(cards.count()):
            card = cards.nth(i)

            if i >= len(players):
                continue

            player = players[i]

            # ищем тимейта (тот же team, но не я)
            if player.get("team") == my_team and player.get("user_id") != my_id:
                print("FOUND TEAMMATE:", player.get("user_id"))

                card.click()
                time.sleep(0.2)

                page.locator(".table-body-players-card-menu ._contract").click()
                return

        print("TEAMMATE NOT FOUND")

    except Exception as e:
        print("CONTRACT OPEN ERROR:", e)


def handle_contract(page, state):
    try:
        contract = page.locator(".TableContract")

        if contract.count() == 0:
            return False

        users = contract.locator("._info")

        sender_index = None

        # ищем кто "предлагает"
        for i in range(users.count()):
            block = users.nth(i)
            subtitle = block.locator("._subtitle").inner_text()

            if "предлагает" in subtitle:
                sender_index = i
                break

        if sender_index is None:
            return False

        # 👉 теперь определяем team через порядок игроков
        players = list(state.players.values())

        if sender_index >= len(players):
            print("CONTRACT: index mismatch")
            return False

        sender = players[sender_index]

        print("SENDER ID:", sender["user_id"], "TEAM:", sender["team"])

        if sender["team"] == state.my_team:
            print("CONTRACT: ACCEPT")
            time.sleep(0.3)
            contract.locator("._button:has-text('Принять')").click()
        else:
            print("CONTRACT: DECLINE")
            time.sleep(0.3)
            contract.locator("._button:has-text('Отклонить')").click()

        return True

    except Exception as e:
        print("CONTRACT ERROR:", e)
        return False
    

def should_buy(state):
    pos = state.get_my_position()
    field = state.get_my_field()


    if not field or field.get("type") != "field":
        return False

    owner = state.get_owner(pos)
    if owner is not None:
        return False

    price = field.get("price", 0)
    money = state.get_me()["money"]

    if money < price:
        return False

    group = field.get("group")
    group_fields = state.get_group_fields(group)
    owners = [state.get_owner(p) for p in group_fields]

    # убираем None
    owned = [o for o in owners if o is not None]


    print("---- BUY DEBUG ----")
    print("Money:", money)
    print("Price:", price)
    print("Group:", group)
    print("Owners:", owners)


    teammate = state.get_teammate()
    teammate_id = teammate["user_id"] if teammate else None

    # --- 1. никто не владеет ---
    if not owned:
        return True

    # --- 2. все свои / тимейт ---
    if all(o == state.me_id or o == teammate_id for o in owned):
        return True

    # --- 3. у врага есть (ломаем монополию) ---
    enemies = [o for o in owned if o != state.me_id and o != teammate_id]
    has_teammate = any(o == teammate_id for o in owned)

    if enemies and not has_teammate:
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

        return {
            "roll": exists(page.locator("div._action:has-text('Бросить кубики')")),
            "buy": exists(page.locator("div._action:has-text('Купить за')")),
            "auction": exists(page.locator("div._action:has-text('На аукцион')")),
            "pay": exists(page.locator("div._action:has-text('Заплатить')")),
            "decline": exists(page.locator("div._action:has-text('Отклонить')")),
            "refuse": exists(page.locator("div._action:has-text('Отказаться')")),
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
        time.sleep(0.3)
        click_button(page, "Бросить кубики")
        last_action_time = now
        return

    # --- 2. BUY ---
    if actions.get("buy"):
        decision = should_buy(state)

        if decision:
            print("DO: BUY")
            time.sleep(0.5)
            click_contains(page, "Купить за")
        else:
            print("DO: AUCTION")
            time.sleep(0.5)
            click_button(page, "На аукцион")
        last_action_time = now
        return

    # --- 3. PAY ---
    if actions.get("pay"):
        amount = get_pay_amount(page)
        money = state.get_me()["money"]

        print("PAY CHECK:", amount, "vs", money)

        if money >= amount:
            print("DO: PAY")
            time.sleep(0.3)
            click_contains(page, "Заплатить")
        else:
            print("NOT ENOUGH MONEY → OPEN CONTRACT")
            time.sleep(0.3)
            open_contract_with_teammate(page, state)

        last_action_time = now
        return

    # --- 4. decline contract ---
    if actions.get("decline"):
        print("DO: DECLINE")
        time.sleep(0.3)
        click_button(page, "Отклонить")
        last_action_time = now
        return
    
    # --- 5. casino ---
    if actions.get("refuse"):
        print("DO: REFUSE")
        time.sleep(0.3)
        click_button(page, "Отказаться")
        last_action_time = now
        return

    print("NO ACTION")
    time.sleep(0.3)