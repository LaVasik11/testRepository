import json
from turtle import pos


class GameState:
    def __init__(self):
        self.me_id = None

        self.players = {}
        self.fields_state = {}
        self.board = []
        self.current_player = None
        self.owner_team_map = {}
        self.my_team = None

    # ---------- INIT ----------

    def set_me(self, user_id):
        self.me_id = user_id

    def init_from_packet(self, data):
        if not self.board:
            self.board = data["config"]["fields"]

    # ---------- UPDATE ----------

    def update(self, data):
        if "status" not in data:
            return

        status = data["status"]

        players = status.get("players", [])

        self.players_list = players  # ← важно
        self.players = {}

        for p in players:
            self.players[p["user_id"]] = p
            self.owner_team_map[p["user_id"]] = p.get("team")

            if p["user_id"] == self.me_id:
                self.my_team = p.get("team")

        self.current_player = status.get("action_player")


    # ---------- GETTERS ----------

    def is_solo(self):
        return self.my_team is None

    def get_me(self):
        return self.players.get(self.me_id)

    def get_player(self, user_id):
        return self.players.get(user_id)

    def get_teammate(self):
        if self.my_team is None:
            return None

        for p in self.players.values():
            if p.get("team") == self.my_team and p["user_id"] != self.me_id:
                return p
        return None

    def get_enemies(self):
        return [
            p for p in self.players.values()
            if p.get("team") != self.my_team
        ]

    def get_position(self, user_id):
        p = self.get_player(user_id)
        return p["position"] if p else None

    def get_my_position(self):
        return self.get_position(self.me_id)

    def get_field(self, pos):
        if pos is None or pos >= len(self.board):
            return None
        return self.board[pos]

    def get_my_field(self):
        return self.get_field(self.get_my_position())

    def get_owner(self, pos):
        return self.fields_state.get(str(pos), {}).get("owner")

    def get_owner_team(self, owner_id):
        return self.owner_team_map.get(owner_id)

    def get_field_state(self, pos):
        return self.fields_state.get(str(pos), {})

    def is_my_field(self, pos):
        return self.get_owner(pos) == self.me_id

    def is_teammate_field(self, pos):
        owner = self.get_owner(pos)
        teammate = self.get_teammate()
        return teammate and owner == teammate["user_id"]

    def is_enemy_field(self, pos):
        owner = self.get_owner(pos)
        return owner is not None and owner != self.me_id and not self.is_teammate_field(pos)
    
    def is_my_turn_now(self):
        return self.current_player == self.me_id

    # ---------- GROUP LOGIC ----------

    def get_group(self, pos):
        field = self.get_field(pos)
        return field.get("group") if field else None

    def get_group_fields(self, group_id):
        return [
            i for i, f in enumerate(self.board)
            if f.get("group") == group_id
        ]

    def get_group_owners(self, group_id):
        fields = self.get_group_fields(group_id)
        return [self.get_owner(pos) for pos in fields]

    def is_monopoly(self, group_id, owner_id):
        owners = self.get_group_owners(group_id)

        if not owners:
            return False

        for o in owners:
            if o != owner_id:
                return False

        return True

    def sync_fields_from_page(self, page):
        self.fields_state = {}

        fields = page.locator(".table-body-board-fields-one")

        for i in range(fields.count()):
            f = fields.nth(i)

            group = f.get_attribute("mnpl-group")
            owner = f.get_attribute("mnpl-owner")

            if group is None or owner is None:
                continue

            pos = str(i)

            self.fields_state[pos] = {
                "group": int(group),
                "owner": int(owner)
            }

    def build_owner_team_map(self, page):
        self.owner_team_map = {}

        cards = page.locator(".table-body-players-card")

        for i in range(cards.count()):
            card = cards.nth(i)

            order = card.get_attribute("mnpl-order")
            team = card.get_attribute("mnpl-team")

            if order is None or team is None:
                continue

            self.owner_team_map[int(order)] = int(team)

    # ---------- TURN ----------

    def is_my_turn(self, data):
        return data["status"]["action_player"] == self.me_id

    # ---------- DEBUG ----------

    def debug_print(self):
        me = self.get_me()
        if not me:
            return

        pos = me["position"]
        field = self.get_field(pos)
        owner = self.get_owner(pos)

        print("=== STATE ===")
        print("My pos:", pos)
        print("Field:", field.get("title"), "| group:", field.get("group"))
        print("Owner:", owner)
        print("Money:", me["money"])
