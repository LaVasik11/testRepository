import re
import time


last_action_time = 0
waiting_for_money = False
timesleep = 0.3

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
        print("SOLO → SKIP CONTRACT")
        return
    
    try:
        me = state.get_me()
        if not me:
            return

        my_id = me["user_id"]

        cards = page.locator(".table-body-players-card")

        my_team = None

        # --- находим свою карточку и команду ---
        for i in range(cards.count()):
            card = cards.nth(i)

            card_id = card.get_attribute("id")
            if not card_id:
                continue

            if str(my_id) in card_id:
                my_team = card.get_attribute("mnpl-team")
                break

        if my_team is None:
            print("MY TEAM NOT FOUND IN UI")
            return

        print("MY TEAM (UI):", my_team)

        # --- ищем тимейта ---
        for i in range(cards.count()):
            card = cards.nth(i)

            card_id = card.get_attribute("id")
            team = card.get_attribute("mnpl-team")

            if not card_id or not team:
                continue

            # пропускаем себя
            if str(my_id) in card_id:
                continue

            # 🔥 КЛЮЧ: тот же mnpl-team
            if team == my_team:
                print("FOUND TEAMMATE CARD:", card_id)

                waiting_for_money = True

                body = card.locator(".table-body-players-card-body")
                body.click()
                page.wait_for_timeout(300)

                menu = card.locator(".table-body-players-card-menu")
                menu.locator("._contract").click()

                # --- ждём окно ---
                page.wait_for_selector(".TableContract", timeout=2000)
                contract = page.locator(".TableContract")

                # --- правая колонка (мы даём деньги) ---
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

                print("CONTRACT SENT TO TEAMMATE:", need)

                waiting_for_money = False
                return

        print("TEAMMATE NOT FOUND (UI)")

    except Exception as e:
        waiting_for_money = False
        print("CONTRACT OPEN ERROR:", e)


def handle_contract(page, state):
    try:
        contract = page.locator(".TableContract")

        if not contract.is_visible():
            return False

        if state.is_solo():
            print("SOLO GAME → DECLINE ALL")
            contract.locator("._button:has-text('Отклонить')").click()
            return True
    
        me = state.get_me()
        if not me:
            return False

        my_team = me.get("team")

        # 1. берём ник sender из контракта
        sender_nick = None

        users = contract.locator("._info")

        for i in range(users.count()):
            block = users.nth(i)

            subtitle = block.locator("._subtitle").inner_text().lower()

            if "предлагает" in subtitle:
                sender_nick = block.locator("._nick").inner_text().strip()
                break

        if not sender_nick:
            print("NO SENDER NICK")
            return False

        print("SENDER NICK:", sender_nick)
        if sender_nick == "Вы":
            print("IGNORE OWN CONTRACT")
            return True

        # 2. ищем этого игрока в таблице игроков
        players = page.locator(".table-body-players-card")

        sender_team = None

        for i in range(players.count()):
            card = players.nth(i)

            nick = card.locator("._nick").inner_text().strip()

            if nick == sender_nick:
                sender_team = card.get_attribute("mnpl-team")
                break

        if sender_team is None:
            print("SENDER NOT FOUND IN PLAYER LIST")
            return False

        sender_team = int(sender_team)

        print("SENDER TEAM:", sender_team, "MY TEAM:", my_team)

        # 3. логика решения
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
    
    pos = state.get_my_position()
    field = state.get_my_field()

    if not field or field.get("type") != "field":
        return False

    if state.get_owner(pos) is not None:
        return False

    me = state.get_me()
    if not me:
        return False

    price = field.get("price", 0)
    money = me["money"]

    if money < price:
        return False

    # ---------- получаем МОЮ команду из UI ----------
    my_id = me["user_id"]
    cards = page.locator(".table-body-players-card")

    my_team = None

    for i in range(cards.count()):
        card = cards.nth(i)
        cid = card.get_attribute("id")

        if cid and str(my_id) in cid:
            my_team = card.get_attribute("mnpl-team")
            break

    if my_team is None:
        print("MY TEAM NOT FOUND (UI)")
        return False

    # ---------- получаем команды владельцев ----------
    group = field.get("group")
    group_fields = state.get_group_fields(group)

    owners = [state.get_owner(p) for p in group_fields]
    owned = [o for o in owners if o is not None]

    owner_teams = []

    for owner_id in owned:
        team = None

        # ищем в DOM по id
        for i in range(cards.count()):
            card = cards.nth(i)
            cid = card.get_attribute("id")

            if cid and str(owner_id) in cid:
                team = card.get_attribute("mnpl-team")
                break

        if team is not None:
            owner_teams.append(team)

    print("---- BUY DEBUG ----")
    print("Money:", money)
    print("Price:", price)
    print("Group:", group)
    print("Owners:", owners)
    print("Owner teams (UI):", owner_teams)
    print("My team (UI):", my_team)

    # ---------- ЛОГИКА ----------

    if not owner_teams:
        return True

    has_enemy = any(team != my_team for team in owner_teams)
    has_teammate = any(team == my_team for team in owner_teams)

    # ✅ только свои → покупаем
    if not has_enemy:
        return True

    # ✅ только враги → ломаем монополию
    if has_enemy and not has_teammate:
        return True

    # ❌ смешанная группа → НЕ покупаем
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

    # защита от спама (1.5 сек)
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

        print("BUY CHECK:", price, "vs", money)

        # --- хватает денег ---
        if money >= price:
            print("DO: BUY")
            waiting_for_money = False
            time.sleep(timesleep)
            click_contains(page, "Купить за")
            last_action_time = now
            return

        # --- не хватает ---
        need = price - money

        if not waiting_for_money:
            print("NOT ENOUGH MONEY → NEED:", need)

            if has_teammate(state):
                open_contract_with_teammate(page, state, need)
                waiting_for_money = True
            else:
                print("SOLO MODE → SKIP (no money)")

        last_action_time = now
        return

    # --- 3. PAY ---
    if actions.get("pay"):
        amount = get_pay_amount(page)
        money = state.get_me()["money"]

        print("PAY CHECK:", amount, "vs", money)
        if not actions.get("buy"):
            waiting_for_money = False
        if money >= amount:
            click_contains(page, "Заплатить")
        else:
            need = amount - money
            print("NEED:", need)
            print("CALLING CONTRACT FUNCTION")
            if has_teammate(state):
                open_contract_with_teammate(page, state, need)
            else:
                print("SOLO MODE → CANNOT PAY (no teammate)")

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