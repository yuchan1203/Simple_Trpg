'''
date: 2026-03-31
time: AM 05:14
version 0.0.4
developer: ruan
description: simple text-based game with python
'''
import random
from copy import deepcopy

class Player:
    def __init__(self, name):
        self.name = name
        self.max_health = 100
        self.health = 100
        self.experience = 0
        self.experience_to_next_level = 1
        self.level = 1
        self.strength = 5
        self.defense = 1
        self.coins = 100
        self.location = "마을 중심"
        self.inventory = {}
        self.slot_items = deepcopy(DEFAULT_SLOT_ITEMS)
        self.attack_buff_turns = 0
        self.attack_buff_multiplier = 1

    def get_slot_effect(self, slot):
        return self.slot_items.get(slot, {}).get("effect", 0)

    def get_total_attack(self):
        total_attack = self.strength + self.get_slot_effect("무기 슬롯")
        if self.attack_buff_turns > 0:
            total_attack = int(total_attack * self.attack_buff_multiplier)
        return total_attack

    def get_total_defense(self):
        return self.defense + self.get_slot_effect("방패 슬롯")

    def get_escape_chance(self):
        return self.get_slot_effect("신발 슬롯")

    def clamp_health(self):
        if self.health > self.max_health:
            self.health = self.max_health
        if self.health < 0:
            self.health = 0

    def take_damage(self, damage):
        self.health -= damage
        self.clamp_health()

    def heal(self, amount):
        self.health += amount
        self.clamp_health()

    def add_inventory_item(self, item_name, quantity=1):
        self.inventory[item_name] = self.inventory.get(item_name, 0) + quantity

    def remove_inventory_item(self, item_name, quantity=1):
        if item_name not in self.inventory:
            return
        self.inventory[item_name] -= quantity
        if self.inventory[item_name] <= 0:
            del self.inventory[item_name]

    def check_level_up(self):
        while self.experience >= self.experience_to_next_level:
            print(f"레벨업! 레벨 {self.level} -> {self.level + 1}")
            self.experience -= self.experience_to_next_level
            self.experience_to_next_level += self.level
            self.level += 1
            self.strength += 1
            self.defense += 1

    def apply_attack_buff(self, multiplier, turns):
        self.attack_buff_turns = turns
        self.attack_buff_multiplier = multiplier

    def tick_attack_buff(self):
        if self.attack_buff_turns > 0:
            self.attack_buff_turns -= 1
            if self.attack_buff_turns == 0:
                self.attack_buff_multiplier = 1
                print_divider(30)
                print("공격 버프 효과가 사라졌습니다.")

    def go_to(self, location, down_health):
        if self.health <= down_health:
            print(f"체력이 {down_health} 이하라 이동할 수 없습니다.")
            self.show_hp()
            return
        print(f"{location}으로 이동합니다..")
        self.location = location
        if down_health > 0:
            self.take_damage(down_health)
            print(f"이동으로 {down_health}의 체력을 잃었습니다.")
            self.show_hp()

    def show_hp(self):
        self.clamp_health()
        if self.health >= 70:
            hp_color = "\033[92m"
        elif self.health >= 30:
            hp_color = "\033[93m"
        else:
            hp_color = "\033[91m"
        if self.max_health >= 1000:
            div = 100
        elif self.max_health >= 100:
            div = 10
        else:
            div = 1
        current_bar = "■" * (self.health // div)
        empty_bar = "□" * ((self.max_health - self.health) // div)
        print(f"체력: [{self.health}/{self.max_health}] {hp_color}[{current_bar}{empty_bar}]\033[0m")

    def show_experience(self):
        self.check_level_up()
        div = 1
        if self.experience_to_next_level >= 1000:
            div = 100
        elif self.experience_to_next_level >= 100:
            div = 10
        if self.experience == 0:
            exp_bar = f"[{'□' * (self.experience_to_next_level // div)}]"
        elif self.experience >= self.experience_to_next_level:
            exp_bar = f"[{'■' * (self.experience_to_next_level // div)}]"
        else:
            exp_bar = f"[{'■' * (self.experience // div)}{'□' * ((self.experience_to_next_level - self.experience) // div)}]"
        print(f"레벨: [{self.level}] | 경험치: [{self.experience}/{self.experience_to_next_level}] {exp_bar}")

    def show_status(self):
        self.show_hp()
        self.show_experience()
        status_parts = [
            f"[코인: {self.coins}]",
            f"[공격력: {self.get_total_attack()}]",
            f"[방어력: {self.get_total_defense()}]",
        ]
        if self.attack_buff_turns > 0:
            status_parts.append(
                f"[공격 버프: {self.attack_buff_multiplier}배/{self.attack_buff_turns}턴]"
            )
        print(" ".join(status_parts))

    def show_inventory(self):
        if not self.inventory:
            print("인벤토리가 비어 있습니다.")
            return
        print("인벤토리:")
        for item, quantity in self.inventory.items():
            effect = store_items.get(item, {}).get("effect", "없음")
            print(f"[{item}] [수량: {quantity}] [효과: {effect}] [판매 가격: 5코인]")

    def show_equipment(self):
        for slot, item in self.slot_items.items():
            if item["name"]:
                print(f"[{slot}: {item['name']}] [효과: {item['effect']}]")
            else:
                print(f"[{slot}: 없음]")

    def unequip_item(self, slot):
        if slot not in self.slot_items or not self.slot_items[slot]["name"]:
            invalid_input()
            return False
        item_name = self.slot_items[slot]["name"]
        print(f"{item_name}을(를) {slot}에서 해제했습니다.")
        self.add_inventory_item(item_name)
        self.slot_items[slot]["name"] = ""
        self.slot_items[slot]["effect"] = 0
        return True

    def equip_item(self, slot, item_name):
        if slot not in self.slot_items:
            invalid_input()
            return False
        if self.slot_items[slot]["name"]:
            self.unequip_item(slot)
        self.slot_items[slot]["name"] = item_name
        self.slot_items[slot]["effect"] = store_items[item_name]["effect"]
        self.remove_inventory_item(item_name)
        print(f"{item_name}을(를) {slot}에 장착했습니다.")
        return True

    def recover_health(self, healing_amount, cost):
        if self.health >= self.max_health:
            print("체력이 이미 최대입니다.", end=" ")
            self.show_hp()
            return
        if self.coins < cost:
            print(f"코인이 부족합니다. 현재 코인: {self.coins}")
            return
        self.coins -= cost
        self.heal(healing_amount)
        print(f"체력을 {healing_amount}만큼 회복했습니다.", end=" ")
        if cost > 0:
            print(f"남은 코인: {self.coins}")
        else:
            self.show_hp()

    def purchase_item(self, item_name, cost):
        if self.coins >= cost:
            self.coins -= cost
            self.add_inventory_item(item_name)
            print(f"{item_name}을(를) 구매했습니다. 남은 코인: {self.coins}")
        else:
            print(f"코인이 부족합니다. 현재 코인: {self.coins}")

    def sell_inventory_item(self, item_name, cost, quantity=1):
        if item_name not in self.inventory or self.inventory[item_name] <= 0:
            print("판매할 수 있는 아이템이 없습니다.")
            return
        self.coins += cost * quantity
        self.remove_inventory_item(item_name, quantity)
        print(f"{item_name}을(를) 판매했습니다. 현재 코인: {self.coins}")


class Enemy:
    def __init__(self, name, health, damage, drop_item):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.drop_item = drop_item

    @classmethod
    def from_type(cls, enemy_type):
        enemy_data = enemy_types[enemy_type]
        return cls(
            enemy_type,
            enemy_data["health"],
            enemy_data["damage"],
            enemy_data["item"],
        )

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0


# 현재 상태 정의
DEFAULT_SLOT_ITEMS = {
    "무기 슬롯": {"name": "소형 나무 검", "effect": 5},
    "방패 슬롯": {"name": "소형 나무 방패", "effect": 10},
    "모자 슬롯": {"name": "", "effect": 0},
    "옷 슬롯": {"name": "", "effect": 0},
    "갑옷 슬롯": {"name": "", "effect": 0},
    "신발 슬롯": {"name": "소형 가죽 신발", "effect": 10},
    "액세서리 슬롯": {"name": "", "effect": 0},
}

enemy_types = {
    "슬라임": {"health": 30, "damage": 10, "item": "슬라임의 이슬"},
    "고블린": {"health": 60, "damage": 15, "item": "고블린의 칼"},
    "오크": {"health": 100, "damage": 20, "item": "오크의 살점"},
}
enemy_drop_items = {
    "슬라임의 이슬": {"cost": 5, "effect": 10, "type": "heal potion"},
    "고블린의 칼": {"cost": 10, "effect": 19, "type": "weapon"},
    "오크의 살점": {"cost": 20, "effect": 2, "type": "attack potion"},
}
potion_store_items = {
    "소형 체력 포션": {"cost": 5, "effect": 25, "type": "heal potion"},
    "중형 체력 포션": {"cost": 10, "effect": 50, "type": "heal potion"},
    "대형 체력 포션": {"cost": 15, "effect": 75, "type": "heal potion"},
    "소형 공격 포션": {"cost": 5, "effect": 1.5, "effect2": 3, "type": "attack potion"},
    "중형 공격 포션": {"cost": 10, "effect": 2, "effect2": 4, "type": "attack potion"},
    "대형 공격 포션": {"cost": 15, "effect": 2.5, "effect2": 5, "type": "attack potion"},
}
weapon_store_items = {
    "소형 나무 검": {"cost": 5, "effect": 5, "type": "weapon"},
    "중형 나무 검": {"cost": 10, "effect": 10, "type": "weapon"},
    "소형 철제 검": {"cost": 15, "effect": 15, "type": "weapon"},
    "중형 철제 검": {"cost": 20, "effect": 20, "type": "weapon"},
    "소형 나무 방패": {"cost": 5, "effect": 10, "type": "shield"},
    "중형 나무 방패": {"cost": 10, "effect": 20, "type": "shield"},
    "소형 철제 방패": {"cost": 15, "effect": 30, "type": "shield"},
    "중형 철제 방패": {"cost": 20, "effect": 40, "type": "shield"},
}
shoe_store_items = {
    "소형 가죽 신발": {"cost": 5, "effect": 10, "type": "shoe"},
    "가죽 신발": {"cost": 10, "effect": 20, "type": "shoe"},
    "소형 사슬 신발": {"cost": 15, "effect": 30, "type": "shoe"},
    "사슬 신발": {"cost": 20, "effect": 40, "type": "shoe"},
}
store_items = {}
store_items.update({item: weapon_store_items[item] for item in weapon_store_items})
store_items.update({item: potion_store_items[item] for item in potion_store_items})
store_items.update({item: shoe_store_items[item] for item in shoe_store_items})
store_items.update({item: enemy_drop_items[item] for item in enemy_drop_items})

potion_store_items_list = list(potion_store_items.keys())
weapon_store_items_list = list(weapon_store_items.keys())
shoe_store_items_list = list(shoe_store_items.keys())
enemy_drop_items_list = list(enemy_drop_items.keys())


def invalid_input():
    print("잘못된 입력입니다. 다시 시도해 주세요.")


def print_divider(separator_length):
    if separator_length >= 50:
        print("\n" * 20)
    print("-" * separator_length)


def has_sellable_items(player):
    if player.inventory:
        print("[1] [아이템 판매]")
        return True
    return False


def get_usable_battle_items(player):
    usable_types = {"heal potion", "attack potion"}
    return [
        item_name
        for item_name in player.inventory
        if store_items.get(item_name, {}).get("type") in usable_types
    ]


def use_item(player, item_name):
    if item_name not in player.inventory or player.inventory[item_name] <= 0:
        invalid_input()
        return False

    item_data = store_items[item_name]

    if item_data["type"] == "heal potion":
        if player.health + item_data["effect"] >= player.max_health:
            choice = input(
                f"체력이 최대 체력을 초과하게 됩니다. [체력: {player.health}] [최대 체력: {player.max_health}] "
                f"[회복량: {item_data['effect']}] [1: 아이템 사용] [2: 취소]"
            ).strip()
            if choice != "1":
                print("아이템 사용을 취소했습니다.")
                return False
        print("체력을 성공적으로 회복하였습니다!", end=" ")
        player.recover_health(item_data["effect"], 0)
    elif item_data["type"] == "attack potion":
        choice = input(
            f"공격력을 증가시키겠습니까? [현재 공격력: {player.get_total_attack()}] "
            f"[증가 배율: {item_data['effect']}] [1: 아이템 사용] [2: 취소]: "
        ).strip()
        if choice != "1":
            print("아이템 사용을 취소했습니다.")
            return False
        player.apply_attack_buff(item_data["effect"], item_data["effect2"])
        print(
            f"공격 포션을 성공적으로 사용하였습니다! 앞으로 {item_data['effect2']}턴 동안 공격력이 {item_data['effect']}배 증가합니다."
        )
    else:
        print("지금은 사용할 수 없는 아이템입니다.")
        return False

    player.remove_inventory_item(item_name, 1)
    return True


def open_equipment_menu(player):
    while True:
        slot_names = list(player.slot_items.keys())
        for idx, slot in enumerate(slot_names, 1):
            if player.slot_items[slot]['name'] == "":
                print(f"[{idx}] [{slot}] [현재 장착: 없음]")
            else:
                print(f"[{idx}] [{slot}] [현재 장착: {player.slot_items[slot]['name']}]")
        print("[9] [마을회관으로 돌아가기]")
        print_divider(30)
        slot_choice = input("장비를 관리할 슬롯을 선택하세요: ").strip()
        print_divider(50)
        if slot_choice == "9":
            player.go_to("마을회관", 0)
            return
        elif not slot_choice.isdigit() or not (1 <= int(slot_choice) <= len(slot_names)):
            invalid_input()
            continue
        selected_slot = slot_names[int(slot_choice) - 1]
        if player.slot_items[selected_slot]['name'] == "":
            print(f"[선택한 슬롯: {selected_slot}] [현재 장착: 없음]")
        else:
            print(f"[선택한 슬롯: {selected_slot}] [현재 장착: {player.slot_items[selected_slot]['name']}]")
        can_equip_items = []
        for item in player.inventory:
            if (
                (selected_slot == "무기 슬롯" and "검" in item)
                or (selected_slot == "방패 슬롯" and "방패" in item)
                or (selected_slot == "신발 슬롯" and "신발" in item)
            ):
                can_equip_items.append(item)

        can_equip = len(can_equip_items) != 0
        can_unequip = player.slot_items[selected_slot]["name"] != ""

        if can_equip:
            for idx, item in enumerate(can_equip_items, 1):
                print(f"[{idx}] [{item} 장착하기] [수량: {player.inventory[item]}] [효과: {store_items[item]['effect']}]")
        if can_unequip:
            print("[8] [장비 해제하기]")
        print("[9] [마을회관으로 돌아가기]")

        action = input("원하는 행동을 선택하세요: ").strip()
        print_divider(50)

        if action == "8" and can_unequip:
            player.unequip_item(selected_slot)
            return
        if action == "9":
            player.go_to("마을회관", 0)
            return
        if can_equip and action.isdigit():
            action_num = int(action)
            if 1 <= action_num <= len(can_equip_items):
                selected_item = can_equip_items[action_num - 1]
                player.equip_item(selected_slot, selected_item)
                return

        invalid_input()


def begin_battle(player, enemy_type):
    enemy = Enemy.from_type(enemy_type)
    print(f"{enemy.name}(이)가 나타났습니다! 전투를 시작합니다.")
    run_battle(player, enemy)


def run_battle(player, enemy):
    defense_active = False
    stunned = False

    while player.health > 0 and enemy.is_alive():
        print_divider(30)
        can_attack = player.slot_items["무기 슬롯"]["name"] != ""
        can_parry = player.slot_items["방패 슬롯"]["name"] != ""
        usable_inventory_items = get_usable_battle_items(player)
        can_use_item = bool(usable_inventory_items)
        buff_applied_this_turn = False

        if can_attack:
            print("[1: 공격]", end=" ")
        if can_parry:
            print("[2: 패링]", end=" ")
        if can_use_item:
            print("[3: 아이템 사용]", end=" ")
        print("[9: 도망치기]")
        print_divider(30)

        action = input("원하는 행동을 선택하세요: ").strip()
        print_divider(50)

        if action == "1" and can_attack:
            damage = player.get_total_attack() + random.randint(0, player.level)
            enemy.take_damage(damage)
            print(f"당신이 적에게 {damage}의 피해를 입혔습니다. 적의 남은 체력: {enemy.health}")
        elif action == "2" and can_parry:
            defense = min(player.get_total_defense(), 100)
            print(
                f"당신이 패링 자세를 취했습니다. 다음 공격의 피해를 {defense}% 감소시키고 적을 한 턴 기절시킵니다."
            )
            defense_active = True
        elif action == "3" and can_use_item:
            for idx, item in enumerate(usable_inventory_items, 1):
                print(f"[{idx}] [{item}] [수량: {player.inventory[item]}] [효과: {store_items[item]['effect']}]")
            item_choice = input("사용할 아이템 번호를 입력하세요: ").strip()
            print_divider(30)
            if item_choice.isdigit() and 1 <= int(item_choice) <= len(usable_inventory_items):
                selected_item = usable_inventory_items[int(item_choice) - 1]
                if not use_item(player, selected_item):
                    continue
                buff_applied_this_turn = store_items[selected_item]["type"] == "attack potion"
            else:
                invalid_input()
                continue
        elif action == "9":
            escape_chance = player.get_escape_chance()
            print(f"도망치기를 시도합니다...(확률:{escape_chance}%)")
            print_divider(30)
            random_chance = random.randint(1, 100)
            if random_chance <= escape_chance:
                print_divider(50)
                print("성공적으로 도망쳤습니다!")
                print_divider(30)
                print("마을로 이동합니다..")
                if player.attack_buff_turns > 0 and not buff_applied_this_turn:
                    player.tick_attack_buff()
                player.go_to("마을 중심", 1)
                return
            else:
                print("도망치기는 실패했습니다! 적이 당신을 공격합니다.")
        else:
            invalid_input()
            continue

        if player.attack_buff_turns > 0 and not buff_applied_this_turn:
            player.tick_attack_buff()

        print_divider(30)
        if not enemy.is_alive():
            break

        if stunned:
            stunned = False
            print("적이 기절했습니다! 이번 턴에는 공격하지 않습니다.")
            continue

        enemy_damage = enemy.damage
        if defense_active:
            defense = player.get_total_defense()
            if defense > 100:
                defense = 100
            enemy_damage = int(enemy_damage * (1 - defense / 100))
            print(f"패링에 성공했습니다! 적의 공격을 {defense}% 감소시키고 다음 턴에 적이 기절합니다.")
            defense_active = False
            stunned = True

        player.take_damage(enemy_damage)
        print(f"적이 당신에게 {enemy_damage}의 피해를 입혔습니다.")
        player.show_hp()

    if enemy.health <= 0 and player.health > 0:
        player.add_inventory_item(enemy.drop_item)
        print(f"승리했습니다! {enemy.drop_item}을(를) 획득했습니다.")
        print_divider(30)
        player.experience += 1
        player.check_level_up()
        player.show_status()
    elif player.health <= 0:
        print("패배했습니다... 다음에는 더 강해져서 도전해 주세요.")


def enter_main_village(player):
    print("[마을 중심]\n[1] [마을회관으로 이동]\n[4] [물약 상점으로 이동]\n[5] [무기 상점으로 이동]\n[6] [시장으로 이동]\n[7] [병원으로 이동]\n[8] [숲으로 이동]\n[9] [게임 종료]")
    print_divider(30)
    action = input("원하는 행동을 선택하세요: ").strip()
    print_divider(50)
    if action == "1":
        player.go_to("마을회관", 0)
    elif action == "4":
        player.go_to("물약 상점", 0)
    elif action == "5":
        player.go_to("무기 상점", 0)
    elif action == "6":
        player.go_to("시장", 0)
    elif action == "7":
        player.go_to("병원", 0)
    elif action == "8":
        player.go_to("숲", 1)
    elif action == "9":
        print("게임이 종료되었습니다.")
        exit()
    else:
        invalid_input()


def enter_forest(player):
    print("[숲] [1: 전투 시작] [9: 마을 중심으로 돌아가기]")
    print_divider(30)
    action = input("원하는 행동을 선택하세요: ").strip()
    print_divider(50)
    if action == "1":
        begin_battle(player, "슬라임")
    elif action == "9":
        player.go_to("마을 중심", 1)
    else:
        invalid_input()


def enter_potion_store(player):
    print("[물약 상점]")
    for idx, item in enumerate(potion_store_items_list, 1):
        print(f"[{idx}] [{item} 구매하기] [{potion_store_items[item]['cost']} 코인]")
    print("[9] [마을 중심으로 돌아가기]")
    print_divider(30)
    action = input("원하는 행동을 선택하세요: ").strip()
    print_divider(50)
    if action.isdigit() and 1 <= int(action) <= len(potion_store_items_list):
        current_item_name = potion_store_items_list[int(action) - 1]
        current_item_cost = potion_store_items[current_item_name]["cost"]
        player.purchase_item(current_item_name, current_item_cost)
    elif action == "9":
        player.go_to("마을 중심", 0)
    else:
        invalid_input()


def enter_weapon_store(player):
    print("[무기 상점]")
    for idx, item in enumerate(weapon_store_items_list, 1):
        print(f"[{idx}] [{item} 구매하기] [{weapon_store_items[item]['cost']} 코인]")
    print("[9] [마을 중심으로 돌아가기]")
    print_divider(30)
    action = input("원하는 행동을 선택하세요: ").strip()
    print_divider(50)
    if action.isdigit() and 1 <= int(action) <= len(weapon_store_items_list):
        current_item_name = weapon_store_items_list[int(action) - 1]
        current_item_cost = weapon_store_items[current_item_name]["cost"]
        player.purchase_item(current_item_name, current_item_cost)
    elif action == "9":
        player.go_to("마을 중심", 0)
    else:
        invalid_input()


def enter_market(player):
    print("[시장]", end=" ")
    can_sell = has_sellable_items(player)
    print("[9] [마을 중심으로 돌아가기]")
    print_divider(30)
    action = input("원하는 행동을 선택하세요: ").strip()
    print_divider(50)
    if action == "1" and can_sell:
        inventory_items = list(player.inventory.keys())
        for idx, item in enumerate(inventory_items, 1):
            print(f"[{idx}] {item} (수량: {player.inventory[item]})")
        print("[9] 판매 취소")
        item_choice = input("판매할 아이템 번호를 입력하세요: ").strip()
        print_divider(50)
        if item_choice.isdigit() and 1 <= int(item_choice) <= len(inventory_items):
            selected_item = inventory_items[int(item_choice) - 1]
            player.sell_inventory_item(selected_item, 5, 1)
        elif item_choice == "9":
            print("판매를 취소했습니다.")
        else:
            invalid_input()
    elif action == "9":
        player.go_to("마을 중심", 0)
    else:
        invalid_input()


def enter_hospital(player):
    print("[병원]")
    player.show_hp()
    can_recover = player.health < player.max_health
    if can_recover:
        print("[1] [체력 10 회복하기] [1 코인]")
        print("[2] [체력 전부 회복하기] [3 코인]")
    print("[9] [마을 중심으로 돌아가기]")
    print_divider(30)
    action = input("원하는 행동을 선택하세요: ").strip()
    print_divider(50)
    if action == "1":
        player.recover_health(10, 1)
    elif action == "2":
        player.recover_health(player.max_health - player.health, 3)
    elif action == "9":
        player.go_to("마을 중심", 0)
    else:
        invalid_input()


def enter_village_hall(player):
    print("[마을회관]\n[1] [스테이터스 확인]\n[2] [인벤토리 확인]\n[3] [장비 확인]\n[4] [장비 교체]\n[9] [마을 중심으로 돌아가기]")
    print_divider(30)
    action = input("원하는 행동을 선택하세요: ").strip()
    print_divider(50)
    if action == "1":
        player.show_status()
    elif action == "2":
        player.show_inventory()
    elif action == "3":
        player.show_equipment()
    elif action == "4":
        open_equipment_menu(player)
    elif action == "9":
        player.go_to("마을 중심", 0)
    else:
        invalid_input()


def run_game(player):
    while True:
        print_divider(30)
        if player.location == "마을 중심":
            enter_main_village(player)
        elif player.location == "숲":
            enter_forest(player)
        elif player.location == "물약 상점":
            enter_potion_store(player)
        elif player.location == "무기 상점":
            enter_weapon_store(player)
        elif player.location == "시장":
            enter_market(player)
        elif player.location == "병원":
            enter_hospital(player)
        elif player.location == "마을회관":
            enter_village_hall(player)
        else:
            print("알 수 없는 위치입니다. 마을 중심으로 이동합니다.")
            player.location = "마을 중심"

        if player.health <= 0:
            print("게임 오버! 다음에는 더 강해져서 도전해 주세요.")
            break


def main():
    player_name = input("플레이어 이름을 입력하세요: ")
    player = Player(player_name)
    print_divider(50)
    if player_name == "admin":  # admin mode
        print("관리자 모드로 진입합니다. 최대 체력을 부여합니다.")
        player.max_health = 1000
        player.health = 1000
        player.experience = 50
        player.coins = 1000
    else:
        print(
            f"안녕하세요 {player_name}님, 게임의 세계에 오신 것을 환영합니다. 당신은 이 세계를 구하기 위해 모험을 떠납니다."
        )

    run_game(player)


if __name__ == "__main__":
    main()
