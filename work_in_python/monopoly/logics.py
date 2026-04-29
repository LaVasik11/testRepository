import re
import time


last_action_time = 0
waiting_for_money = False
timesleep = 0.2


def get_monopoly_group(page, state):
    if not state.is_my_turn_now():
        return False

    me = state.get_me()
    if not me:
        return False

    my_id = str(me["user_id"])

    cards = page.locator(".table-body-players-card")

    my_team = None

    # --- находим свою команду (как у тебя уже работает) ---
    for i in range(cards.count()):
        card = cards.nth(i)

        card_id = card.get_attribute("id")
        if not card_id:
            continue

        if my_id in card_id:
            my_team = card.get_attribute("mnpl-team")
            break

    if my_team is None:
        return False

    try:
        my_team = int(my_team)
    except:
        return False

    fields = page.locator(".table-body-board-fields-one")

    groups = {}

    # --- собираем группы ---
    for i in range(fields.count()):
        f = fields.nth(i)

        group = f.get_attribute("mnpl-group")
        if group is None:
            continue

        group = int(group)

        owner = f.get_attribute("mnpl-owner")

        team = None

        if owner is not None:
            owner_id = str(owner)

            for j in range(cards.count()):
                card = cards.nth(j)

                card_id = card.get_attribute("id")
                team_attr = card.get_attribute("mnpl-team")

                if not card_id or not team_attr:
                    continue

                if owner_id in card_id:
                    try:
                        team = int(team_attr)
                    except:
                        team = None
                    break

        if group not in groups:
            groups[group] = []

        groups[group].append(team)

    # --- проверка монополии ---
    for group_id, teams in groups.items():

        if group_id in (0, 9):
            continue

        if any(t is None for t in teams):
            continue

        if all(t == my_team for t in teams):
            return group_id

    return False
    

def has_teammate(state):
    me = state.get_me()
    if not me:
        return False

    my_team = me.get("team")

    teammates = [
        p for p in state.players.values()
        if p.get("team") == my_team and p["user_id"] != me["user_id"]
    ]

    return len(teammates) > 0


def get_pay_amount(page):
    try:
        text = page.locator("div._action:has-text('Заплатить')").inner_text()
        return parse_number(text)
    except:
        return 0

def get_buy_amount(page):
    try:
        text = page.locator("div._action:has-text('Купить за')").inner_text()
        return parse_number(text)
    except:
        return 0


def send_message(page, text):
    try:
        input_box = page.locator("input[placeholder='Введите сообщение']")

        if not input_box.is_visible():
            print("CHAT INPUT NOT FOUND")
            return False

        input_box.click()
        input_box.fill(text)

        page.keyboard.press("Enter")

        print("MESSAGE SENT:", text)
        return True

    except Exception as e:
        print("SEND MESSAGE ERROR:", e)
        return False
    


def open_contract_with_teammate(page, state, need):
    global waiting_for_money

    if state.is_solo():
        return
    
    try:
        me = state.get_me()
        if not me:
            return

        my_id = me["user_id"]

        cards = page.locator(".table-body-players-card")

        my_team = None

        for i in range(cards.count()):
            card = cards.nth(i)

            card_id = card.get_attribute("id")
            if not card_id:
                continue

            if str(my_id) in card_id:
                my_team = card.get_attribute("mnpl-team")
                break

        if my_team is None:
            return

        for i in range(cards.count()):
            card = cards.nth(i)

            card_id = card.get_attribute("id")
            team = card.get_attribute("mnpl-team")

            if not card_id or not team:
                continue

            if str(my_id) in card_id:
                continue

            if team == my_team:

                waiting_for_money = True

                body = card.locator(".table-body-players-card-body")
                body.click()
                page.wait_for_timeout(300)

                menu = card.locator(".table-body-players-card-menu")
                menu.locator("._contract").click()

                page.wait_for_selector(".TableContract", timeout=2000)
                contract = page.locator(".TableContract")

                cash_block = contract.locator(".TableContract-content-list > div").nth(1)

                cash_block.locator("._one._cash").click()
                page.wait_for_timeout(300)
                time.sleep(timesleep)
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type(str(need))

                page.wait_for_timeout(200)
                time.sleep(timesleep)
                page.keyboard.press("Enter")
                time.sleep(timesleep)
                page.wait_for_timeout(300)

                contract.locator("._button:has-text('Предложить')").click()


                waiting_for_money = False
                return


    except Exception as e:
        waiting_for_money = False
        print("CONTRACT OPEN ERROR:", e)


def handle_contract(page, state):
    try:
        contract = page.locator(".TableContract")

        if not contract.is_visible():
            return False

        if state.is_solo():
            contract.locator("._button:has-text('Отклонить')").click()
            return True
    
        me = state.get_me()
        if not me:
            return False

        my_team = me.get("team")

        sender_nick = None

        users = contract.locator("._info")

        for i in range(users.count()):
            block = users.nth(i)

            subtitle = block.locator("._subtitle").inner_text().lower()

            if "предлагает" in subtitle:
                sender_nick = block.locator("._nick").inner_text().strip()
                break

        if not sender_nick:
            return False

        if sender_nick == "Вы":
            return True

        players = page.locator(".table-body-players-card")

        sender_team = None

        for i in range(players.count()):
            card = players.nth(i)

            nick = card.locator("._nick").inner_text().strip()

            if nick == sender_nick:
                sender_team = card.get_attribute("mnpl-team")
                break

        if sender_team is None:
            return False

        sender_team = int(sender_team)


        if sender_team == my_team:
            print("CONTRACT: ACCEPT")
            time.sleep(timesleep)
            contract.locator("._button:has-text('Принять')").click()
        else:
            print("CONTRACT: DECLINE")
            time.sleep(timesleep)
            contract.locator("._button:has-text('Отклонить')").click()
            send_message(page, "С террористами переговоры не ведём")

        return True

    except Exception as e:
        print("CONTRACT ERROR:", e)
        return False
    
def should_buy(page, state):
    if state.is_solo():
        return True

    field = state.get_my_field()
    if not field or field.get("type") != "field":
        return False

    me = state.get_me()
    if not me:
        return False

    price = get_buy_amount(page)
    money = me["money"]


    if money < price:
        print("NOT ENOUGH MONEY")
        return False

    my_team = int(me.get("team"))

    group = field.get("group")

    fields = page.locator(f".table-body-board-fields-one[mnpl-group='{group}']")
    cards = page.locator(".table-body-players-card")

    owner_teams = []


    for i in range(fields.count()):
        f = fields.nth(i)

        logo = f.locator("._logo").get_attribute("style")

        if logo:
            if "brands/0/" in logo or "brands/9/" in logo:
                print(f"[FIELD {i}] SPECIAL GROUP → FORCE BUY")
                return True

        owner = f.get_attribute("mnpl-owner")

        if owner is None:
            continue

        owner_id = str(owner)

        team = None

        for j in range(cards.count()):
            card = cards.nth(j)

            card_id = card.get_attribute("id")
            if not card_id:
                continue

            if card_id == f"player_card_{owner_id}":
                team_attr = card.get_attribute("mnpl-team")
                if team_attr is not None:
                    team = int(team_attr)
                break


        if team is not None:
            owner_teams.append(team)


    if not owner_teams:
        return True

    has_enemy = any(t != my_team for t in owner_teams)
    has_teammate = any(t == my_team for t in owner_teams)


    if not has_enemy:
        return True

    if has_enemy and not has_teammate:
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
    global waiting_for_money


    if not state.is_my_turn_now():
        return

    now = time.time()

    if now - last_action_time < 1.5:
        return

    # --- 1. ROLL ---
    if actions.get("roll"):
        print("DO: ROLL")
        time.sleep(timesleep)
        click_button(page, "Бросить кубики")
        last_action_time = now
        return

    # --- 2. BUY ---
    if actions.get("buy"):
        decision = should_buy(page, state)

        if not decision:
            print("DO: AUCTION")
            time.sleep(timesleep)
            click_button(page, "На аукцион")
            last_action_time = now
            return

        price = get_buy_amount(page)
        money = state.get_me()["money"]


        if money >= price:
            print("DO: BUY")
            waiting_for_money = False
            time.sleep(timesleep)
            click_contains(page, "Купить за")
            last_action_time = now
            return

        need = price - money

        if not waiting_for_money:
            if has_teammate(state):
                open_contract_with_teammate(page, state, need)
                waiting_for_money = True
            else:
                print("SOLO MODE → SKIP")

        last_action_time = now
        return

    # --- 3. PAY ---
    if actions.get("pay"):
        amount = get_pay_amount(page)
        money = state.get_me()["money"]

        if not actions.get("buy"):
            waiting_for_money = False
        if money >= amount:
            click_contains(page, "Заплатить")
        else:
            need = amount - money
            if has_teammate(state):
                open_contract_with_teammate(page, state, need)
            else:
                print("SOLO MODE → SKIP")

        last_action_time = now
        return

    # --- 4. decline contract ---
    if actions.get("decline"):
        print("DO: DECLINE")
        time.sleep(timesleep)
        click_button(page, "Отклонить")
        last_action_time = now
        return
    
    # --- 5. casino ---
    if actions.get("refuse"):
        print("DO: REFUSE")
        time.sleep(timesleep)
        click_button(page, "Отказаться")
        last_action_time = now
        return

    print("NO ACTION")
    time.sleep(timesleep)