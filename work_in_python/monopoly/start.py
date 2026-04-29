import json
from logics import detect_actions, handle_actions, handle_contract, try_upgrade


def ui_loop_step(page, state):
    try:
        if not state.me_id:
            page.wait_for_timeout(200)
            return

        if handle_contract(page, state):
            page.wait_for_timeout(200)
            return

        if not state.is_my_turn_now():
            page.wait_for_timeout(200)
            return

        if page.locator(".TableAction").count() == 0:
            page.wait_for_timeout(200)
            return

        print("=== MY TURN ===")

        try_upgrade(page, state)
        
        actions = detect_actions(page)
        print("ACTIONS:", actions)

        handle_actions(page, state, actions)

        page.wait_for_timeout(200)

    except Exception as e:
        print("UI LOOP ERROR:", e)
        page.wait_for_timeout(500)


def handle_ws_message(raw, state):
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


def handle_ws(ws, state):
    print("WS connected:", ws.url)

    def on_recv(frame):
        data = frame if isinstance(frame, str) else frame.decode("utf-8", errors="ignore")
        handle_ws_message(data, state)

    ws.on("framereceived", on_recv)