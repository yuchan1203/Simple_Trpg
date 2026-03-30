'''
date: 2026-03-31
version 0.0.1
developer: ruan
discription: simple text-based game with python
'''

# 라이브러리 임포트
import random

# 현재 상태 초기화
player_max_health = 100
player_health = 100
player_experience = 0
player_experience_to_next_level = 1
player_level = 1
player_strength = 5
player_defense = 1
player_coins = 100
player_location = "마을 중심"

# 인벤토리 초기화
player_inventory = {
    
}
enemy_types = {
    "슬라임": {"health": 30, "damage": 10, "item": "슬라임의 이슬"},
    "고블린": {"health": 60, "damage": 15, "item": "고블린의 칼"},
    "오크": {"health": 100, "damage": 20, "item": "미스터리 아이템"},
}
enemy_drop_items = {
    "슬라임의 이슬": {"cost": 5, "effect": 10, "type": "heal potion"},
    "고블린의 칼": {"cost": 10, "effect": 19, "type": "weapon"},
    "미스터리 아이템": {"cost": 20, "effect": "랜덤 효과", "type": "mystery"},
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
    "나무 검": {"cost": 10, "effect": 10, "type": "weapon"},
    "소형 철 검": {"cost": 15, "effect": 15, "type": "weapon"},
    "철 검": {"cost": 20, "effect": 20, "type": "weapon"},
    "소형 나무 방패": {"cost": 5, "effect": 10, "type": "shield"},
    "나무 방패": {"cost": 10, "effect": 20, "type": "shield"},
    "소형 철 방패": {"cost": 15, "effect": 30, "type": "shield"},
    "철 방패": {"cost": 20, "effect": 40, "type": "shield"},
}
shoe_store_items = {
    "소형 가죽 신발": {"cost": 5, "effect": 10, "type": "shoe"},
    "가죽 신발": {"cost": 10, "effect": 20, "type": "shoe"},
    "소형 사슬 신발": {"cost": 15, "effect": 30, "type": "shoe"},
    "사슬 신발": {"cost": 20, "effect": 40, "type": "shoe"},
}
player_slot_items = {
    "무기 슬롯": {"name": "소형 나무 검", "effect": 5},
    "방패 슬롯": {"name": "소형 나무 방패", "effect": 10},
    "모자 슬롯": {"name": "", "effect": 0},
    "옷 슬롯": {"name": "", "effect": 0},
    "갑옷 슬롯": {"name": "", "effect": 0},
    "신발 슬롯": {"name": "소형 가죽 신발", "effect": 10},
    "액세서리 슬롯": {"name": "", "effect": 0},
}
store_items = {
    
}
store_items.update({item: weapon_store_items[item] for item in weapon_store_items})
store_items.update({item: potion_store_items[item] for item in potion_store_items})
store_items.update({item: shoe_store_items[item] for item in shoe_store_items})
store_items.update({item: enemy_drop_items[item] for item in enemy_drop_items})

potion_store_items_list = list(potion_store_items.keys())
weapon_store_items_list = list(weapon_store_items.keys())
shoe_store_items_list = list(shoe_store_items.keys())
enemy_drop_items_list = list(enemy_drop_items.keys())

# 이동 함수
def go_to(location, down_health):
    global player_location, player_health
    if player_health <= down_health:
        print(f"체력이 {down_health} 이하라 이동할 수 없습니다.")
        show_hp()
        return
    print(f"{location}으로 이동합니다..")
    player_location = location
    if down_health > 0:
        player_health -= down_health
        print(f"이동으로 {down_health}의 체력을 잃었습니다.")
        show_hp()

# 장비 표시 함수
def show_equipment():
    print("장비:")
    for slot, item in player_slot_items.items():
        if item["name"]:
            print(f"[{slot}: {item['name']}] [효과: {item['effect']}]")
        else:
            print(f"[{slot}: 없음]")

# 아이템 사용 함수
def use_item(item_name):
    global player_health, player_strength
    result = []
    if item_name in player_inventory and player_inventory[item_name] > 0:
        does_use = True
        if store_items[item_name]["type"] == "heal potion":
            if player_health + store_items[item_name]["effect"] >= player_max_health:
                choice = input(f"체력이 최대 체력을 초과하게 됩니다. [체력: {player_health}] [최대 체력: {player_max_health}] [회복량: {store_items[item_name]['effect']}] 아이템을 사용할까요? (y:1/n:2)")
                if choice != "1": does_use = False
            if does_use:
                print("체력을 성공적으로 회복하였습니다!",end=" ")
                recover_health(store_items[item_name]["effect"], 0)
        elif store_items[item_name]["type"] == "attack potion":
            choice = input(f"공격력을 증가시키겠습니까? [공격력: {player_strength}] [증가량: {store_items[item_name]['effect']}] [Y:1 / N:2]: ")
            if choice != "1": does_use = False
        if does_use:
            player_strength = int(player_strength * store_items[item_name]["effect"])
            print(f"공격 포션을 성공적으로 사용하였습니다! 앞으로 {store_items[item_name]['effect2']}턴 동안 공격력이 {store_items[item_name]['effect']}배 증가합니다.")
            result = [store_items[item_name]['effect2'], store_items[item_name]['effect']]
        else: invalid_input(); does_use = False
        if does_use: remove_item(item_name, 1)
    else: invalid_input()
    return result if does_use else [-1]

# 장비 해제 함수
def unequip_item(slot):
    global player_strength, player_defense
    if slot in player_slot_items and player_slot_items[slot]["name"]:
        print(f"{player_slot_items[slot]['name']}을(를) {slot}에서 해제했습니다.")
        if player_slot_items[slot]["name"] in player_inventory:
            player_inventory[player_slot_items[slot]["name"]] += 1
        else:
            player_inventory[player_slot_items[slot]["name"]] = 1
        if slot == "무기 슬롯": player_strength -= player_slot_items[slot]["effect"]
        elif slot == "방패 슬롯": player_defense -= player_slot_items[slot]["effect"]
        player_slot_items[slot]["name"] = ""
        player_slot_items[slot]["effect"] = 0
    else: invalid_input()

# 잘못된 입력 처리 함수
def invalid_input():
    print("잘못된 입력입니다. 다시 시도해 주세요.")
    
# 아이템 제거 함수
def remove_item(item_name, quantity=1):
    if item_name in player_inventory:
        player_inventory[item_name] -= quantity
        if player_inventory[item_name] <= 0:
            del player_inventory[item_name]

def open_equipment_menu():
    for idx, slot in enumerate(player_slot_items.keys(), 1):
        print(f"[{idx}] {slot} (현재 장착: {player_slot_items[slot]['name']})")
    slot_choice = input("장비를 관리할 슬롯을 선택하세요: ")
    print_divider(50)
    if slot_choice.isdigit() and 1 <= int(slot_choice) <= len(player_slot_items):
        selected_slot = list(player_slot_items.keys())[int(slot_choice) - 1]
        print(f"선택한 슬롯: {selected_slot} (현재 장착: {player_slot_items[selected_slot]['name']})")
        can_equip_items = []
        for item in player_inventory:
            if (selected_slot == "무기 슬롯" and "검" in item) or (selected_slot == "방패 슬롯" and "방패" in item) or (selected_slot == "신발 슬롯" and "신발" in item):
                can_equip_items.append(item)
        can_equip = len(can_equip_items) != 0
        can_unequip = player_slot_items[selected_slot]["name"] != ""
        if can_equip:
            for idx, item in enumerate(can_equip_items, 1):
                print(f"[{idx}] [{item} 장착하기] [수량: {player_inventory[item]}] [효과: {store_items[item]['effect']}]")
        if can_unequip:
            print("[8: 장비 해제하기]", end=" ")
        print("[9: 마을 중심으로 돌아가기]")
        action = input("원하는 행동을 선택하세요: ")
        print_divider(50)

        if action == "8" and can_unequip:
            unequip_item(selected_slot)
        elif action == "9":
            go_to("마을 중심", 0)
        elif can_equip and action.isdigit():
            action = int(action)
            if 1 <= action <= len(can_equip_items):
                selected_item = can_equip_items[action - 1]
                if player_slot_items[selected_slot]["name"]:
                    unequip_item(selected_slot)
                player_slot_items[selected_slot]["name"] = selected_item
                player_slot_items[selected_slot]["effect"] = store_items[selected_item]["effect"]
                remove_item(selected_item)
                print(f"{selected_item}을(를) {selected_slot}에 장착했습니다.")
            else:
                invalid_input()
                open_equipment_menu()
        else:
            invalid_input()
            open_equipment_menu()
    else:
        invalid_input()
        open_equipment_menu()
def show_hp():
    global player_health, player_max_health
    if player_health > player_max_health: player_health = player_max_health
    if player_health < 0: player_health = 0
    if player_health >= 70: hp_color = "\033[92m"
    elif player_health >= 30: hp_color = "\033[93m"
    else: hp_color = "\033[91m"
    if player_max_health >= 1000: div = 100
    elif player_max_health >= 100: div = 10
    else: div = 1
    print(f"체력: [{player_max_health}/{player_health}] {hp_color}[{'■' * (player_health // div)}{'□' * ((player_max_health - player_health) // div)}]\033[0m")

# 경험치 및 레벨 표시 함수
def show_experience():
    check_level_up()
    div = 1
    if player_experience_to_next_level >= 1000: div = 100
    if player_experience_to_next_level >= 100: div = 10
    if player_experience == 0: exp_bar = f"[{'□' * ((player_experience_to_next_level) // div)}]"
    elif player_experience >= player_experience_to_next_level: exp_bar = f"[{'■' * (player_experience_to_next_level // div)}]"
    else: exp_bar = f"[{'■' * (player_experience // div)}{'□' * ((player_experience_to_next_level - player_experience) // div)}]"
    print(f"레벨: [{player_level}] | 경험치: [{player_experience_to_next_level}/{player_experience}] {exp_bar}")

# 구분선 함수
def print_divider(separator_length):
    if separator_length >= 50: print("\n" * 20)
    print("-" * separator_length)

# 플레이어 상태 표시 함수
def show_status():
    show_hp()
    show_experience()
    print(f"[코인: {player_coins}] [공격력: {player_strength}] [방어력: {player_defense}]")
    
# 플레이어 인벤토리 표시 함수
def show_inventory():
    if not player_inventory: print("인벤토리가 비어 있습니다.")
    else:
        print("인벤토리:")
        for item, quantity in player_inventory.items(): print(f"[{item}] [수량: {quantity}] [효과: {store_items[item]['effect']}] [판매 가격: 5코인]")
    
# 아이템 구매 함수
def purchase_item(item_name, cost):
    global player_coins
    if player_coins >= cost:
        player_coins -= cost
        add_inventory_item(item_name)
        print(f"{item_name}을(를) 구매했습니다. 남은 코인: {player_coins}")
    else: print(f"코인이 부족합니다. 현재 코인: {player_coins}")

# 전투 시작 함수
def begin_battle(enemy_type):
    print(f"{enemy_type}(이)가 나타났습니다! 전투를 시작합니다.")
    run_battle(enemy_type, enemy_health=enemy_types[enemy_type]["health"], enemy_damage=enemy_types[enemy_type]["damage"], enemy_item=enemy_types[enemy_type]["item"], defense_active=False, stunned=False, attack_buff_turns=0, attack_buff_multiplier=1)

# 레벨업 확인 함수
def check_level_up():
    global player_level, player_experience, player_experience_to_next_level, player_strength, player_defense
    while player_experience >= player_experience_to_next_level:
        print(f"레벨업! 레벨 {player_level} -> {player_level + 1}")
        player_experience -= player_experience_to_next_level
        player_experience_to_next_level += player_level
        player_level += 1
        player_strength += 1
        player_defense += 1

# 아이템 추가 함수
def add_inventory_item(item_name, quantity=1):
    if item_name in player_inventory: player_inventory[item_name] += quantity
    else: player_inventory[item_name] = quantity

# 전투 진행 함수
def run_battle(enemy_type, enemy_health, enemy_damage, enemy_item, defense_active, stunned, attack_buff_turns, attack_buff_multiplier):
    global player_health, player_experience, player_coins, player_location, player_strength, player_level, player_experience_to_next_level, player_defense
    if attack_buff_turns > 0:
            attack_buff_turns -= 1
            if attack_buff_turns == 0:
                player_strength = int(player_strength / attack_buff_multiplier)
                print_divider(30)
                print("공격 버프 효과가 사라졌습니다.")
    if player_health > 0 and enemy_health > 0:
        print_divider(30)
        can_attack = True
        if player_slot_items["무기 슬롯"]["name"] == "": can_attack = False
        if can_attack: print("[1: 공격]", end=" ")
        can_parry = True
        if player_slot_items["방패 슬롯"]["name"] == "": can_parry = False
        if can_parry: print("[2: 패링]", end=" ")
        can_use_item = True
        if not player_inventory: can_use_item = False
        if can_use_item: print("[3: 아이템 사용]", end=" ")
        print("[9: 도망치기]")
        print_divider(30)
        action = input("원하는 행동을 선택하세요: ")
        print_divider(50)

        if action == '1' and can_attack: # 공격
            damage = player_strength + random.randint(0, player_level) + player_slot_items["무기 슬롯"]["effect"]
            enemy_health -= damage
            if enemy_health < 0: enemy_health = 0
            print(f"당신이 적에게 {damage}의 피해를 입혔습니다. 적의 남은 체력: {enemy_health}")
        elif action == '2' and can_parry: # 패링
            print(f"당신이 패링 자세를 취했습니다. 다음 공격의 피해를 {player_slot_items['방패 슬롯']['effect']}% 감소시키고 적을 한 턴 기절시킵니다.")
            defense_active = True
        elif action == '3' and can_use_item: # 아이템 사용
            for idx, item in enumerate(player_inventory, 1): print(f"[{idx}] [{item}] [수량: {player_inventory[item]}] [효과: {store_items[item]['effect']}]")
            item_choice = input("사용할 아이템 번호를 입력하세요: ")
            print_divider(30)
            result = use_item(list(player_inventory.keys())[int(item_choice) - 1]) if item_choice.isdigit() and 1 <= int(item_choice) <= len(player_inventory) else None
            if len(result) == 2:
                attack_buff_turns, attack_buff_multiplier = result
            elif result[0] == -1:
                print("아이템 사용이 취소되었습니다.")
                run_battle(enemy_type, enemy_health, enemy_damage, enemy_item, defense_active, stunned, attack_buff_turns, attack_buff_multiplier)
                return
            elif result[0] == 0:
                pass
            else:
                invalid_input()
                run_battle(enemy_type, enemy_health, enemy_damage, enemy_item, defense_active, stunned, attack_buff_turns, attack_buff_multiplier)
                return
        elif action == '9':
            print("도망치기를 시도합니다...(확률:{}%)".format(player_slot_items["신발 슬롯"]["effect"]))
            print_divider(30)
            random_chance = random.randint(1, 100)
            if random_chance <= player_slot_items["신발 슬롯"]["effect"]:
                print_divider(50)
                print("성공적으로 도망쳤습니다!")
                print_divider(30)
                print("마을로 이동합니다..")
                go_to("마을 중심", 1)
                return
            else: print("도망치기는 실패했습니다! 적이 당신을 공격합니다.")
        else:
            invalid_input()
            run_battle(enemy_type, enemy_health, enemy_damage, enemy_item, defense_active, stunned, attack_buff_turns, attack_buff_multiplier)
            return
        print_divider(30)
        if enemy_health > 0:
            if stunned:
                stunned = False
                print("적이 기절했습니다! 이번 턴에는 공격하지 않습니다.")
            else:
                if defense_active:
                    defense = player_defense + player_slot_items["방패 슬롯"]["effect"]
                    if defense > 100: defense = 100
                    enemy_damage = int(enemy_damage * (1 - defense / 100))
                    print(f"패링에 성공했습니다! 적의 공격을 {defense}% 감소시키고 다음 턴에 적이 기절합니다.")
                    defense_active = False
                    stunned = True
                player_health -= enemy_damage
                print(f"적이 당신에게 {enemy_damage}의 피해를 입혔습니다.")
                show_hp()
        run_battle(enemy_type, enemy_health, enemy_damage, enemy_item, defense_active, stunned, attack_buff_turns, attack_buff_multiplier)
        return
    else:
        if enemy_health <= 0 and player_health > 0:
            add_inventory_item(enemy_item)
            print(f"승리했습니다! {enemy_item}을(를) 획득했습니다.")
            print_divider(30)
            player_experience += 1
            check_level_up()
            show_status()
        elif player_health <= 0:
            print("패배했습니다... 다음에는 더 강해져서 도전해 주세요.")
        else: invalid_input()
        return

# 마을 중심 함수
def enter_main_village():
    print("[마을 중심] [1: 마을회관으로 이동] [4: 물약 상점으로 이동] [5: 무기 상점으로 이동] [6: 시장으로 이동] [7: 병원으로 이동] [8: 숲으로 이동] [9: 게임 종료]")
    print_divider(30)
    action = input("원하는 행동을 선택하세요: ")
    print_divider(50)
    if action == '1': go_to("마을회관", 0)
    elif action == '4': go_to("물약 상점", 0)
    elif action == '5': go_to("무기 상점", 0)
    elif action == '6': go_to("시장", 0)
    elif action == '7': go_to("병원", 0)
    elif action == '8': go_to("숲", 1)
    elif action == '9': print("게임이 종료되었습니다."); exit()
    else: invalid_input()

# 숲 함수
def enter_forest():
    print("[숲] [1: 전투 시작] [9: 마을 중심으로 돌아가기]")
    print_divider(30)
    action = input("원하는 행동을 선택하세요: ")
    print_divider(50)
    if action == '1': begin_battle("슬라임")
    elif action == '9': go_to("마을 중심", 1)
    else: invalid_input()

# 물약 상점 함수
def enter_potion_store():
    print("[물약 상점]")
    for idx, item in enumerate(potion_store_items_list, 1):
        print(f"[{idx}: {item} 구매 ({potion_store_items[item]['cost']}코인)]")
    print("[9: 마을 중심으로 돌아가기]")
    print_divider(30)
    action = int(input("원하는 행동을 선택하세요: "))
    print_divider(50)
    if 1 <= action <= len(potion_store_items_list):
        current_item_name = potion_store_items_list[action-1]
        current_item_cost = potion_store_items[current_item_name]["cost"]
        purchase_item(current_item_name, current_item_cost)
    elif action == 9: go_to("마을 중심", 0)
    else: invalid_input()

# 무기 상점 함수
def enter_weapon_store():
    print("[무기 상점]")
    for idx, item in enumerate(weapon_store_items_list, 1):
        print(f"[{idx}: {item} ({weapon_store_items[item]['cost']}코인)]")
    print("[9: 마을 중심으로 돌아가기]")
    print_divider(30)
    action = int(input("원하는 행동을 선택하세요: "))
    print_divider(50)
    if 1 <= action <= len(weapon_store_items_list):
        current_item_name = weapon_store_items_list[action-1]
        current_item_cost = weapon_store_items[current_item_name]["cost"]
        purchase_item(current_item_name, current_item_cost)
    elif action == 9: go_to("마을 중심", 0)
    else: invalid_input()

# 아이템 판매 함수
def sell_inventory_item(item_name, cost, quantity=1):
    global player_coins
    if item_name in player_inventory and player_inventory[item_name] > 0:
        player_coins += cost * quantity
        player_inventory[item_name] -= quantity
        if player_inventory[item_name] == 0:
            del player_inventory[item_name]
        print(f"{item_name}을(를) 판매했습니다. 현재 코인: {player_coins}")
    else:
        print("판매할 수 있는 아이템이 없습니다.")

# 인벤토리에 판매할 물건이 있는지 확인하는 함수
def has_sellable_items():
    cs = False
    if player_inventory:
        cs = True
        print("1: 아이템 판매", end=" ")
    return cs

# 시장 함수
def enter_market():
    print("[시장]", end=" ")
    can_sell = has_sellable_items()
    print("[9: 마을 중심으로 돌아가기]")
    print_divider(30)
    action = input("원하는 행동을 선택하세요: ")
    print_divider(50)
    if action == '1' and can_sell:
        for idx, item in enumerate(player_inventory, 1):
            if idx < 9: print(f"[{idx}] {item} (수량: {player_inventory[item]})")
        print("[9] 판매 취소")
        item_choice = input("판매할 아이템 번호를 입력하세요: ")
        print_divider(50)
        if item_choice.isdigit() and 1 <= int(item_choice) <= len(player_inventory):
            selected_item = list(player_inventory.keys())[int(item_choice) - 1]
            sell_inventory_item(selected_item, 5, 1)
        elif item_choice == '9': print("판매를 취소했습니다.")
        else: invalid_input()
    elif action == '9': go_to("마을 중심", 0)
    else: invalid_input()

# 체력 회복 함수
def recover_health(healing_amount, cost):
    global player_health, player_coins
    if player_health >= player_max_health: print(f"체력이 이미 최대입니다.",end=" "); show_hp()
    elif player_coins >= cost:
        player_coins -= cost
        player_health += healing_amount
        if player_health > player_max_health: player_health = player_max_health
        print(f"체력을 {healing_amount}만큼 회복했습니다.",end=" ")
        if cost > 0: print(f"남은 코인: {player_coins}")
        else: show_hp()
    else: print(f"코인이 부족합니다. 현재 코인: {player_coins}")

# 병원 함수
def enter_hospital(): 
    global player_health, player_coins
    print("[병원] [1: 체력 10 회복하기 (1코인)] [2: 체력 전부 회복하기 (3코인)] [9: 마을 중심으로 돌아가기]")
    show_hp()
    print_divider(30)
    action = input("원하는 행동을 선택하세요: ")
    print_divider(50)
    if action == '1': recover_health(10, 1)
    elif action == '2': recover_health(player_max_health - player_health, 3)
    elif action == '9': go_to("마을 중심", 0)
    else: invalid_input()
    
# 마을회관 함수
def enter_village_hall():
    print("[마을회관] [1: 스테이터스 확인] [2: 인벤토리 확인] [3: 장비 확인] [4: 장비 교체] [9: 마을 중심으로 돌아가기]")
    print_divider(30)
    action = input("원하는 행동을 선택하세요: ")
    print_divider(50)
    if action == '1': show_status()
    elif action == '2': show_inventory()
    elif action == '3': show_equipment()
    elif action == '4': open_equipment_menu()
    elif action == '9': go_to("마을 중심", 0)
    else: invalid_input()

# 게임 시작
player_name = input("플레이어 이름을 입력하세요: ")
print_divider(50)
if player_name == "admin": print("관리자 모드로 진입합니다. 모든 아이템과 최대 체력을 부여합니다."); player_health = 1000; player_max_health = 1000; player_experience = 50; player_coins = 1000
else: print(f"안녕하세요 {player_name}님, 게임의 세계에 오신 것을 환영합니다. 당신은 이 세계를 구하기 위해 모험을 떠납니다.")

# 메인 게임 루프
while True:
    print_divider(30)
    if player_location == "마을 중심": enter_main_village()
    elif player_location == "숲": enter_forest()
    elif player_location == "물약 상점": enter_potion_store()
    elif player_location == "무기 상점": enter_weapon_store()
    elif player_location == "시장": enter_market()
    elif player_location == "병원": enter_hospital()
    elif player_location == "마을회관": enter_village_hall()
    else: print("알 수 없는 위치입니다. 마을 중심으로 이동합니다."); player_location = "마을 중심"
    if player_health <= 0:
        print("게임 오버! 다음에는 더 강해져서 도전해 주세요.")
        break
