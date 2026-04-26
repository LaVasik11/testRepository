import re
import time


last_action_time = 0
waiting_for_money = False

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
    

waiting_for_money = False


def open_contract_with_teammate(page, state, need):
    global waiting_for_money

    try:
        me = state.get_me()
        if not me:
            return

        my_id = me["user_id"]
        my_team = me["team"]

        cards = page.locator(".table-body-players-card-body")
        players = list(state.players.values())

        for i in range(cards.count()):
            if i >= len(players):
                continue

            player = players[i]
            card = cards.nth(i)

            if player.get("team") == my_team and player.get("user_id") != my_id:
                print("FOUND TEAMMATE:", player.get("user_id"))

                waiting_for_money = True

                # --- открыть меню ---
                card.click()
                time.sleep(0.3)

                menu = card.locator("xpath=following-sibling::div[contains(@class, 'table-body-players-card-menu')]")
                menu.locator("._contract").click()

                # --- ждём окно ---
                page.wait_for_selector(".TableContract", timeout=2000)
                contract = page.locator(".TableContract")

                # --- ПРАВАЯ колонка (мы даём деньги) ---
                cash_block = contract.locator(".TableContract-content-list > div").nth(1)

                cash_block.locator("._one._cash").click()
                time.sleep(0.3)

                # --- ввод ---
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type(str(need))

                time.sleep(0.2)

                page.keyboard.press("Enter")   # 🔥 КЛЮЧЕВОЕ

                time.sleep(0.3)

                contract.locator("._button:has-text('Предложить')").click()

                print("CONTRACT SENT:", need)

                time.sleep(1)

                waiting_for_money = False
                return

        print("TEAMMATE NOT FOUND")

    except Exception as e:
        waiting_for_money = False
        print("CONTRACT OPEN ERROR:", e)


def handle_contract(page, state):
    try:
        contract = page.locator(".TableContract")

        if not contract.is_visible():
            return False

        me = state.get_me()
        if not me:
            return False

        my_team = me["team"]

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
            time.sleep(2)
            contract.locator("._button:has-text('Принять')").click()
        else:
            print("CONTRACT: DECLINE")
            time.sleep(2)
            contract.locator("._button:has-text('Отклонить')").click()
            send_message(page, "С террористами переговоры не ведём")

        return True

    except Exception as e:
        print("CONTRACT ERROR:", e)
        return False
    

def should_buy(state):
    pos = state.get_my_position()
    field = state.get_my_field()

    if not field or field.get("type") != "field":
        return False

    if state.get_owner(pos) is not None:
        return False

    price = field.get("price", 0)
    me = state.get_me()

    if not me:
        return False

    money = me["money"]
    my_team = me["team"]

    if money < price:
        return False

    group = field.get("group")
    group_fields = state.get_group_fields(group)

    owners = [state.get_owner(p) for p in group_fields]
    owned = [o for o in owners if o is not None]

    owner_teams = []

    for o in owned:
        player = state.get_player(o)
        if player:
            owner_teams.append(player["team"])

    print("---- BUY DEBUG ----")
    print("Money:", money)
    print("Price:", price)
    print("Group:", group)
    print("Owners:", owners)
    print("Owner teams:", owner_teams)

    # --- 1. никто не владеет ---
    if not owner_teams:
        return True

    # есть ли враги / тиммейты
    has_enemy = any(team != my_team for team in owner_teams)
    has_teammate = any(team == my_team for team in owner_teams)

    # --- 2. нет врагов ---
    if not has_enemy:
        return True

    # --- 3. только враги ---
    if has_enemy and not has_teammate:
        return True

    # --- 4. смешанная группа (и враг и союзник) ---
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

    if not page.locator(".TableContract").is_visible():
        waiting_for_money = False

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

        if not decision:
            print("DO: AUCTION")
            time.sleep(0.5)
            click_button(page, "На аукцион")
            last_action_time = now
            return

        # --- получаем цену ---
        price = get_buy_amount(page)
        money = state.get_me()["money"]

        print("BUY CHECK:", price, "vs", money)

        # --- хватает денег ---
        if money >= price:
            waiting_for_money = False
            print("DO: BUY")
            time.sleep(0.5)
            click_contains(page, "Купить за")

        # --- не хватает денег ---
        else:
            need = price - money
            if not waiting_for_money:
                print("NOT ENOUGH MONEY → NEED:", need)
                open_contract_with_teammate(page, state, need)
                waiting_for_money = True

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
            open_contract_with_teammate(page, state, need)

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