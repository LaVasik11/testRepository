import re
import time


last_action_time = 0
waiting_for_money = False
timesleep = 0.2


def try_upgrade(page, state):
    if not state.is_my_turn_now():
        return
    print("try upgrade...")
    

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
    print("\n===== SHOULD BUY START =====")

    if state.is_solo():
        print("SOLO MODE → BUY")
        return True

    field = state.get_my_field()
    if not field or field.get("type") != "field":
        print("NOT A FIELD")
        return False

    me = state.get_me()
    if not me:
        return False

    price = get_buy_amount(page)
    money = me["money"]

    print("PRICE(UI):", price, "MONEY:", money)

    if money < price:
        print("NOT ENOUGH MONEY")
        return False

    my_team = int(me.get("team"))
    print("MY TEAM:", my_team)

    group = field.get("group")
    print("GROUP:", group)

    fields = page.locator(f".table-body-board-fields-one[mnpl-group='{group}']")
    cards = page.locator(".table-body-players-card")

    owner_teams = []

    print("CHECKING GROUP FIELDS...")

    for i in range(fields.count()):
        f = fields.nth(i)

        logo = f.locator("._logo").get_attribute("style")

        is_car_group = False
        is_game_group = False

        if logo:
            if "brands/0/" in logo:
                is_car_group = True
            if "brands/9/" in logo:
                is_game_group = True

        if is_car_group or is_game_group:
            print(f"[FIELD {i}] SPECIAL GROUP DETECTED → FORCE BUY")
            return True

        owner = f.get_attribute("mnpl-owner")

        print(f"[FIELD {i}] owner:", owner)

        if owner is None:
            continue

        try:
            owner_id = int(owner)
        except:
            continue

        if owner_id >= cards.count():
            continue

        card = cards.nth(owner_id)
        team = card.get_attribute("mnpl-team")

        print(f" → owner id: {owner_id}, team:", team)

        if team is None:
            continue

        try:
            owner_teams.append(int(team))
        except:
            pass

    print("OWNER TEAMS:", owner_teams)

    if not owner_teams:
        print("NO OWNERS → BUY")
        return True

    has_enemy = any(t != my_team for t in owner_teams)
    has_teammate = any(t == my_team for t in owner_teams)

    print("HAS ENEMY:", has_enemy)
    print("HAS TEAMMATE:", has_teammate)

    if not has_enemy:
        print("ONLY TEAM → BUY")
        return True

    if has_enemy and not has_teammate:
        print("ONLY ENEMY → BUY")
        return True

    print("MIXED GROUP → SKIP")
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