import json
from playwright.sync_api import sync_playwright
from keylog import wait_for_start
from GameState import GameState
from logics import detect_actions, handle_actions, handle_contract


state = GameState()
started = False



def ui_loop(page):
    while True:
        try:
            if not state.me_id:
                page.wait_for_timeout(200)
                continue

            if handle_contract(page, state):
                page.wait_for_timeout(200)
                continue

            if not state.is_my_turn_now():
                page.wait_for_timeout(200)
                continue

            if page.locator(".TableAction").count() == 0:
                page.wait_for_timeout(200)
                continue

            print("=== MY TURN ===")

            actions = detect_actions(page)
            print("ACTIONS:", actions)

            handle_actions(page, state, actions)

            page.wait_for_timeout(200)

        except Exception as e:
            print("UI LOOP ERROR:", e)
            page.wait_for_timeout(500)


def handle_ws_message(raw):
    # ---------- AUTH ----------
    if raw.startswith("4auth"):
        try:
            data = json.loads(raw[5:])

            user_data = data.get("user_data")
            if user_data and "user_id" in user_data:
                state.set_me(user_data["user_id"])
                print("MY ID:", state.me_id)

        except Exception as e:
            print("AUTH PARSE ERROR:", e)

        return

    # ---------- PACKET ----------
    if not raw.startswith("4packet"):
        return

    try:
        data = json.loads(raw[7:])
    except:
        return

    if "status" not in data:
        return

    if "config" in data:
        state.init_from_packet(data)

    state.update(data)

    if state.me_id and state.is_my_turn(data):
        state.debug_print()


def handle_ws(ws):
    print("WS connected:", ws.url)

    def on_recv(frame):
        data = frame if isinstance(frame, str) else frame.decode("utf-8", errors="ignore")
        handle_ws_message(data)

    ws.on("framereceived", on_recv)


def handle_message(raw):
    # ---------- AUTH (получаем свой ID) ----------
    if raw.startswith("4auth"):
        data = json.loads(raw[5:])
        user_id = data["user_data"]["user_id"]

        state.set_me(user_id)
        print("MY ID:", user_id)
        return

    # ---------- ОСНОВНЫЕ ПАКЕТЫ ----------
    if raw.startswith("4packet"):
        data = json.loads(raw[7:])

        if not state.board:
            state.init_from_packet(data)

        state.update(data)

        # 👉 тут у тебя ВСЁ актуальное состояние
        print_state()


def print_state():
    me = state.get_me()
    if not me:
        return

    pos = state.get_my_position()
    field = state.get_my_field()
    owner = state.get_owner(pos)

    print("\n=== STATE ===")
    print("Position:", pos)

    if field:
        print("Field:", field.get("title"), "| group:", field.get("group"))

    print("Owner:", owner)
    print("Money:", me["money"])

    # --- пример: владельцы группы ---
    group = state.get_group(pos)
    if group is not None:
        owners = state.get_group_owners(group)
        print("Group owners:", owners)


def run():
    global started

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")

        context = browser.contexts[0]
        page = context.pages[0]

        page.on("websocket", handle_ws)

        page.goto("https://monopoly-one.com/games")

        wait_for_start()
        started = True
        print("STARTED")

        ui_loop(page)


if __name__ == "__main__":
    run()