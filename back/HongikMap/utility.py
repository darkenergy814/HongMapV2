from collections import OrderedDict
from .models import Recommendation

BUILDING_EXTERNAL = "건물 외부"
EXTERNAL = "외부"
HALLWAY = "H"
ELEVATOR = "E"
STAIR = "S"
EXIT = "X"
BASEMENT = "B"

data_path = "HongikMap/static/data/data.txt"
keywords_path = "HongikMap/static/data/keywords.txt"
recommends_by_parsing_path = "HongikMap/static/data/recommends_by_parsing.txt"
result_with_elevator_path = "HongikMap/static/data/result_with_elevator.txt"
result_without_elevator_path = "HongikMap/static/data/result_without_elevator.txt"
coordinate_path = "HongikMap/static/data/coordinate.txt"


def recommend2node(input_recommend: str) -> str:
    """
    Convert input recommend into node
    by searching keywords.txt and recommends_by_paring.txt
    :param input_recommend
    :return: node
    """
    with open(keywords_path, "r", encoding="UTF8") as f:
        for line in f.readlines():
            node, recommend = line.split(":")
            if input_recommend == recommend.split(",")[0].rstrip("\n"):
                return node

    # with open(recommends_by_parsing_path, "r", encoding="UTF8") as f:
    #     for line in f.readlines():
    #         node, recommend = line.split(":")
    #         if input_recommend == recommend.split(",")[0]:
    #             return node

    if Recommendation.objects.filter(recommendation=input_recommend).exists():
        return Recommendation.objects.get(recommendation=input_recommend).node.node
    return ""


def nodes2recommends(input_nodes: list) -> list:
    """
    Convert list of node into list of recommended
    :param input_nodes: list
    :return: list
    """
    result = OrderedDict()

    for node in input_nodes:
        result[node] = ""

    with open(keywords_path, "r", encoding="UTF8") as f:
        for line in f.readlines():
            node, value = line.split(":")
            if node in input_nodes:
                result[node] = value.split(",")[0].rstrip("\n")
                input_nodes.remove(node)
                if not input_nodes:
                    break

    # with open("HongikMap/static/data/recommends_by_parsing.txt", "r", encoding="UTF8") as f:
    #     for line in f.readlines():
    #         node, value = line.split(":")
    #         if node in input_nodes:
    #             result[node] = value.split(",")[0]
    #             input_nodes.remove(node)
    #             if not input_nodes:
    #                 break

    for node in result.keys():
        if result[node] == "":
            result[node] = node2keyword(node)

    return list(result.values())


# Not using
def get_recommends(recommend_path: str, search_nodes: list) -> (dict, list):
    result = dict()
    with open(recommend_path, "r", encoding='UTF8') as f:
        for line in f.readlines():
            node, value = line.split(":")
            if node in search_nodes:
                result[node] = value.split(",")[0]
                search_nodes.remove(node)
                if not search_nodes:
                    break

    return result, search_nodes


def node2keyword(node: str) -> str:
    """
    Convert node into keyword including Entity name

    ---Example---
    A-1-1 -> A101
    T-5-X1 -> T동 5층 출입문

    :param node: str
    :return: keyword string
    """
    building, floor, entity = node.split("-")

    if is_external(node):
        return BUILDING_EXTERNAL

    if is_hallway(node):
        return "{}동 {}층 {}".format(building, floor, "복도")

    if is_elevator(node):
        return "{}동 {}층 {}".format(building, floor, "엘리베이터")

    if is_stair(node):
        return "{}동 {}층 {}".format(building, floor, "계단")

    if is_exit(node):
        return "{}동 {}층 {}".format(building, floor, "출입문")

    if is_room(node):
        if is_basement(node):
            floor = f'0{floor[1:]}'
            return "{}{}{}".format(building, floor, entity)
        # return "{}{}{:0>2}".format(building, floor, entity)
        if '_' in entity:
            prefix, postfix = entity.split("_")
            return "{}{}{:0>2}_{}".format(building, floor, prefix, postfix)
        else:
            return "{}{}{:0>2}".format(building, floor, entity)
    return node


# Return True if floor of the node is basement
def is_basement(node: str) -> bool:
    return node.split("-")[1].startswith(BASEMENT)


# Return True if the node is at EXTERNAL
def is_external(node: str) -> bool:
    return node.startswith(EXTERNAL)


# Return True if entity of the node is hallway
def is_hallway(node: str) -> bool:
    return node.split("-")[2][0] == HALLWAY


# Return Ture if entity of the node is elevator
def is_elevator(node: str) -> bool:
    return node.split("-")[2][0] == ELEVATOR


# Return True if entity of the node is stair
def is_stair(node: str) -> bool:
    return node.split("-")[2][0] == STAIR


# Return True if entity of the node is exit
def is_exit(node: str) -> bool:
    return node.split("-")[2][0] == EXIT


# Return True if entity of the node is room
def is_room(node: str) -> bool:
    if not is_external(node) and node.split("-")[2][0].isdecimal():
        return True
    return False


# Return what is entity of the node
def get_kind(node: str) -> str:
    if is_external(node):
        return EXTERNAL

    if is_hallway(node):
        return HALLWAY

    if is_elevator(node):
        return ELEVATOR

    if is_stair(node):
        return STAIR

    if is_exit(node):
        return EXIT

    return "WRONG_NODE"


def get_external_node_number(node: str) -> str:
    return node.split("-")[2]


def same_kind(prev_node: str, cur_node: str) -> bool:
    if is_external(prev_node) and is_external(cur_node):
        return True
    if prev_node.split("-")[2][0] == cur_node.split("-")[2][0]:
        return True

    return False
