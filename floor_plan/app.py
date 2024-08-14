with open("rooms_4.txt","r") as file:
    file = file.read()

file = file + (file[-1])
# it crashes on concave rooms
# Replace all type of walls for same character.
floor_plan = file.replace("-+-", "-=-")
floor_plan = floor_plan.replace("-+ ", "-| ")
floor_plan = floor_plan.replace(" +-", " |-")
floor_plan = floor_plan.replace("/", "|")
floor_plan = floor_plan.replace("\\", "|")
floor_plan = floor_plan.replace(" + ", " | ")
floor_plan = floor_plan.replace("-+", "-|")
floor_plan = floor_plan.replace("+", "|")
floor_plan = (floor_plan[1:-1].split(") (")[0]).split("\n")

print("total:")
print("W: " + str(file.count("W")) + ", P: " + str(file.count("P")) + ", S: " + str(file.count("S")) + ", C: " + str(file.count("C")))

class Characters:
    W = 0
    P = 0
    S = 0
    C = 0
    name_tag = 0
    close_room = 0

room_list = []
result = []
room_list.append({  "W": 0,
                    "P": 0,
                    "S": 0,
                    "C": 0,
                    "name_tag": "",
                    "close_room": 0,
                    "range_start": 0,
                    "range_end": 0,
                    "current_range_start": 0,
                    "current_range_end": 0,
                    "is_close": False})

room_list[0]["range_start"] = floor_plan[1].find("|")
room_list[0]["range_end"] = floor_plan[1].find("|", room_list[0]["range_start"] + 1)
room_list[0]["current_range_start"] = room_list[0]["range_start"]
room_list[0]["current_range_end"] = room_list[0]["range_end"]

i = 0
move_wall = False

for item in floor_plan:
    line_cha = Characters()

    line_cha.W = item.count("W")
    line_cha.P = item.count("P")
    line_cha.S = item.count("S")
    line_cha.C = item.count("C")
    line_cha.name_tag = item.count("(")
    line_cha.close_room = item.count("-|")
    line_cha.move_room = item.count("|-")

    characters_total = line_cha.W + line_cha.P + line_cha.S + line_cha.C + line_cha.name_tag + line_cha.close_room + line_cha.move_room

    if (characters_total > 0 or move_wall) and i != 0:
        walls = item.count("|")

        start = item.find("|")
        end = item.find("|", start + 1)

        index_list = 0
        is_found2 = False
        for index, room in enumerate(room_list):

            if room["range_start"] == start or room["range_end"] == end:
                index_list = index
                if room["range_start"] != start:
                    room_list[index]["range_start"] = start
                if room["range_end"] != end:
                    room_list[index]["range_end"] = end
                is_found2 = True
                move_wall = False
                break

        if is_found2 == False:
            room_list.append({"W": 0,
                              "P": 0,
                              "S": 0,
                              "C": 0,
                              "name_tag": 0,
                              "close_room": 0,
                              "range_start": start,
                              "range_end": end,
                              "current_range_start": start,
                              "current_range_end": end,
                              "is_close": False})

            index_list = len(room_list) - 1

        while walls - 1 > 0 and characters_total > 0:
            range_room = item[start:end + 1]
            if line_cha.W > 0:
                w_result = range_room.count("W")
                line_cha.W -= w_result
                characters_total -= w_result
                room_list[index_list]["W"] += w_result
            if line_cha.P > 0:
                p_result = range_room.count("P")
                line_cha.P -= p_result
                characters_total -= p_result
                room_list[index_list]["P"] += p_result
            if line_cha.S > 0:
                s_result = range_room.count("S")
                line_cha.S -= s_result
                characters_total -= s_result
                room_list[index_list]["S"] += s_result
            if line_cha.C > 0:
                c_result = range_room.count("C")
                line_cha.C -= c_result
                characters_total -= c_result
                room_list[index_list]["C"] += c_result
            if line_cha.name_tag > 0:
                if range_room.count("(") > 0:
                    name_tag_result = range_room[(range_room.index("(")) + 1: range_room.index(")")]
                    line_cha.name_tag -= 1
                    characters_total -= 1
                    room_list[index_list]["name_tag"] = str(name_tag_result)
            if line_cha.move_room > 0:
                move_room_result = range_room.count("|-")
                line_cha.move_room -= move_room_result
                characters_total -= move_room_result
                move_wall = True
                cha_index = item.index("|-")

                if range_room.count("|-") > 0:
                    if range_room.find("=", 1) == -1:
                        index_close = range_room.find("|", 1)
                    elif range_room.find("|", 1) == -1:
                        index_close = range_room.find("=", 1)
                    elif range_room.find("=", 1) > range_room.find("|", 1):
                        index_close = range_room.find("|", 1)
                    else:
                        index_close = range_room.find("=", 1)
                    close_cha_index = start + index_close

                    if i + 1 < 50 and floor_plan[i + 1][cha_index] == " " and floor_plan[i + 1][cha_index + 1] == " " and floor_plan[i + 1][cha_index - 1] == " ":
                        for index, room in enumerate(room_list):
                            if room["range_end"] == start:
                                end = close_cha_index
                                if room["range_end"] != end:
                                    room_list[index]["range_end"] = close_cha_index
                                break
                        end = close_cha_index + 1
                        move_wall = False

            if line_cha.close_room > 0:
                close_room_result = range_room.count("-|")
                line_cha.close_room -= close_room_result
                characters_total -= close_room_result
                if close_room_result > 0:
                    index_close = range_room.index("-|")
                    close_cha_index = start + index_close + 1
                    if floor_plan[i -1][close_cha_index] == "|" or floor_plan[i -1][close_cha_index + 1] == "|" or floor_plan[i -1][close_cha_index - 1] == "|":
                        result.append(room_list[index_list])
                        room_list.pop(index_list)
                    if floor_plan[i - 1][close_cha_index] == " " and floor_plan[i - 1][close_cha_index + 1] == " " and floor_plan[i - 1][close_cha_index - 1] == " ":
                        for index, room in enumerate(room_list):
                            if room["range_start"] == start:
                                start = close_cha_index + 1
                                if room["range_start"] != start:
                                    room_list[index]["range_start"] = close_cha_index + 1
                                    if room_list[index]["range_start"] > room_list[index]["range_end"]:
                                        room_list[index]["range_end"] = int(item.find("|", start + 1))
                                        end = int(room_list[index]["range_end"])
                                break
                        start = close_cha_index + 1
                        move_wall = False
            if walls - 1 > 1:
                start = end
                end = item.find("|", start + 1)
                is_found = False

                for index, room in enumerate(room_list):
                    if room["range_start"] == start or room["range_end"] == end:
                        index_list = index
                        if room["range_start"] != start:
                            room_list[index]["range_start"] = start
                        if room["range_end"] != end:
                            room_list[index]["range_end"] = end
                        is_found = True
                        break

                range_room = item[start:end + 1]

                if is_found == False:
                    room_list.append({"W": 0,
                                      "P": 0,
                                      "S": 0,
                                      "C": 0,
                                      "name_tag": 0,
                                      "close_room": 0,
                                      "range_start": start,
                                      "range_end": end,
                                      "current_range_start": start,
                                      "current_range_end": end,
                                      "is_close": False})

                    index_list = len(room_list) - 1

            walls -= 1
    i += 1

for room in room_list:
    result.append(room)

result.sort(key=lambda x: x["name_tag"], reverse=False)

filtered_list = [item for item in result if item["name_tag"] == 0]

if (len(filtered_list) != 0): 
    for item in filtered_list:
        remove_index = result.index(item)
        result.pop(remove_index)

for item in result:
    print(item["name_tag"] + ":")
    print("W: " + str(item["W"]) + ", P: " + str(item["P"]) + ", S: " + str(item["S"]) + ", C: " + str(item["C"]))