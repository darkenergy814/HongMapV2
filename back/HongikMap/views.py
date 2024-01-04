from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie


from . import features
from . import suggest
from . import utility
from . import navigate
from . import models

import os

import json
# Create your views here.

def welcome(request):
    return render(request, 'HongikMap/welcome.html', {})


def responsiveWebMain(request):
    departure = request.GET.get('departure', None)
    destination = request.GET.get('destination', None)
    return render(request, 'HongikMap/responsiveWebMain.html', {'departure': departure, 'destination': destination})


def admin(request):
    return render(request, 'HongikMap/admin_main.html', {})


def update(request):
    return render(request, 'HongikMap/update.html', {})


def QandA(request):
    return render(request, 'HongikMap/QandA.html', {})


def txtCorrection(request):
    return render(request, 'HongikMap/txtCorrection.html', {})


def coordinateCorrection(request):
    return render(request, 'HongikMap/coordinateCorrection.html', {})


def date(request):
    return render(request, 'HongikMap/date.html', {})


@csrf_exempt
# @ensure_csrf_cookie
def recommend(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        response_name = data.get('input_val')

        if response_name is not None:
            # Your logic with response_name
            response_list = suggest.recommend(response_name)
            return JsonResponse({"recommendations": response_list})
        else:
            return JsonResponse({"error": "Missing input_val parameter"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    # response_name = request.POST.get('input_val')
    # print(response_name)
    # response_list = suggest.recommend(response_name)
    # # response_list.sort(key=lambda x: (int(x[1:]) if str(x[1:]).isdecimal() else str(x[1:]), x[0]))
    # return JsonResponse({"recommendations": response_list})

@csrf_exempt
def submit(request):
    request = json.loads(request.body.decode('utf-8'))
    departure = request.get('departure')
    destination = request.get('destination')
    print(departure, destination)

    departure_node = utility.recommend2node(departure)
    destination_node = utility.recommend2node(destination)
    # 여기서 출발지, 도착지를 DB에 보낸다. 그럼 DB에서 출발지->x ,도착지->x에 대한 정보를 준다. 그럼 이중 for문을 통해 모든 경우에 대한 경로를 요구하고, 이를 받아서 최소를 출력한다.
    # print(f'submitted_node: {departure_node} {destination_node}')
    elevatorUse = navigate.search(departure_node, destination_node, elevator=True)
    elevatorNoUse = navigate.search(departure_node, destination_node, elevator=False)

    return JsonResponse({'elevatorUse': elevatorUse,
                         'elevatorNoUse': elevatorNoUse})


def compute(f: object, filename: str = ''):
    # 엘리베이터 사용여부에 대한 모든 노드정보에 대한 객체를 변수에 준다.
    graph_with_elevator = features.Graph(f, elevator=True)
    graph_without_elevator = features.Graph(f, elevator=False)
    # 구한 모든 노드에 대해 다익스트라를 돌리기 위해 객체를 생성한다.
    path_with_elevator = features.Path(graph_with_elevator)
    path_without_elevator = features.Path(graph_without_elevator)

    # XtoX에 저장할 건물내에서 출입구 출입구사이 가중치를 저장할 파일을 열어준다.
    result_with_elevator_XtoX = open("HongikMap/static/data/external_node/result_with_elevator_XtoX.txt", 'a',
                                     encoding="UTF8")
    result_without_elevator_XtoX = open("HongikMap/static/data/external_node/result_without_elevator_XtoX.txt", 'a',
                                        encoding="UTF8")

    print(graph_with_elevator.rooms + graph_with_elevator.exits)
    # 모든 위치를 기준으로 하여 모든 장소에 대한 최단 거리를 구한다. 그리고 이 경로를 저장한다.
    for start in graph_with_elevator.rooms + graph_with_elevator.exits:
        if start.split('-')[0] == '외부':
            continue
        path_with_elevator.dijkstra(start)
    # XtoX를 엘리베이터 사용 유무에 따라 분리해서 저장한다.
    # 외부노드가 아닌경우에는 XtoX에 출입구에서 출입구를 넣어주고 아닌 경우에는 경로에 X->X가 있을경우 중간경로를 넣어준다,
    if filename != 'external_node.txt':
        # XtoX일경우에만 XtoX 파일에 넣어준다.
        for key, value in path_with_elevator.result.items():
            if key[0].split('-')[2][0] == 'X' and key[1].split('-')[2][0] == 'X':
                result_with_elevator_XtoX.write(f'{key[0]} {key[1]}:{value["distance"]} {" ".join(value["route"])}\n')
        # 강의실 이름 붙여준다.
        models.save_recommendation(path_with_elevator.rooms)
    # 건물 안 경로 만들어주는함수
    else:
        copy_result = path_with_elevator.result
        for key, value in copy_result.items():
            for value_index in range(len(value['route']) - 1):
                intermediate_place1 = value['route'][value_index]
                intermediate_place2 = value['route'][value_index + 1]
                if intermediate_place1.split('-')[2][0] == 'X' and intermediate_place2.split('-')[2][0] == 'X':
                    XtoX_route = models.get_route(intermediate_place1, intermediate_place2, True)
                    if XtoX_route != {}:
                        XtoX_route = XtoX_route['route'][1:-1]
                        path_with_elevator.result[key]['route'][value_index + 1:value_index + 1] = XtoX_route

    models.save(path_with_elevator.result, True)

    for start in graph_without_elevator.rooms + graph_without_elevator.exits:
        # 외부노드가 시작점이면 다익스트라를 돌리지않는다.
        if start.split('-')[0] == '외부':
            continue
        path_without_elevator.dijkstra(start)
    if filename != 'external_node.txt':
        for key, value in path_without_elevator.result.items():
            if key[0].split('-')[2][0] == 'X' and key[1].split('-')[2][0] == 'X':
                result_without_elevator_XtoX.write(
                    f'{key[0]} {key[1]}:{value["distance"]} {" ".join(value["route"])}\n')
    # 건물 안 경로 만들어주는함수
    else:
        copy_result = path_without_elevator.result
        for key, value in copy_result.items():
            for value_index in range(len(value['route']) - 1):
                intermediate_place1 = value['route'][value_index]
                intermediate_place2 = value['route'][value_index + 1]
                if intermediate_place1.split('-')[2][0] == 'X' and intermediate_place2.split('-')[2][0] == 'X':
                    XtoX_route = models.get_route(intermediate_place1, intermediate_place2, False)
                    if XtoX_route != {}:
                        XtoX_route = XtoX_route['route'][1:-1]
                        path_without_elevator.result[key]['route'][value_index + 1:value_index + 1] = XtoX_route

    models.save(path_without_elevator.result, False)
    # 이름을 파싱 해준다. 다만 with elevator와 without elevator의 rooms는 동일하니 하나만.


def compute_XtoX():
    with open('HongikMap/static/data/external_node/merged_external_node_with_elevator.txt', 'r', encoding='UTF8') as f:
        graph_with_elevator = features.Graph(f, elevator=True)
        path_with_elevator = features.Path(graph_with_elevator)
        for start in graph_with_elevator.rooms + graph_with_elevator.exits:
            if start.split('-')[0] == '외부':
                continue
            path_with_elevator.dijkstra(start)

        copy_result = path_with_elevator.result
        for key, value in copy_result.items():
            for value_index in range(len(value['route']) - 1):
                intermediate_place1 = value['route'][value_index]
                intermediate_place2 = value['route'][value_index + 1]
                if intermediate_place1.split('-')[2][0] == 'X' and intermediate_place2.split('-')[2][0] == 'X':
                    XtoX_route = models.get_route(intermediate_place1, intermediate_place2, True)
                    if XtoX_route != {}:
                        XtoX_route = XtoX_route['route'][1:-1]
                        path_with_elevator.result[key]['route'][value_index + 1:value_index + 1] = XtoX_route
        print('save_path_with_elevator.result')
        models.save(path_with_elevator.result, True)

    with open('HongikMap/static/data/external_node/merged_external_node_without_elevator.txt', 'r',
              encoding='UTF8') as f:
        graph_without_elevator = features.Graph(f, elevator=False)
        path_without_elevator = features.Path(graph_without_elevator)
        for start in graph_without_elevator.rooms + graph_without_elevator.exits:
            if start.split('-')[0] == '외부':
                continue
            path_without_elevator.dijkstra(start)

        copy_result = path_without_elevator.result
        for key, value in copy_result.items():
            for value_index in range(len(value['route']) - 1):
                intermediate_place1 = value['route'][value_index]
                intermediate_place2 = value['route'][value_index + 1]
                if intermediate_place1.split('-')[2][0] == 'X' and intermediate_place2.split('-')[2][0] == 'X':
                    XtoX_route = models.get_route(intermediate_place1, intermediate_place2, False)
                    if XtoX_route != {}:
                        XtoX_route = XtoX_route['route'][1:-1]
                        path_without_elevator.result[key]['route'][value_index + 1:value_index + 1] = XtoX_route
        models.save(path_without_elevator.result, False)


# 각 건물 별로 XToX가 있을 경우 저장
def XToXDataization():
    # externalNode = open("HongikMap/static/data/external_node/external_node.txt", 'r', encoding="UTF8")
    # result_without_elevator_XtoX = open("HongikMap/static/data/external_node/result_without_elevator_XtoX.txt", 'r',
    #                                     encoding="UTF8")
    #
    # # 외부노드와 XtoX를 합쳐서 merged_externalNode로 만들어준다.
    # merged_external_node_path = "HongikMap/static/data/external_node/merged_external_node.txt"
    # with open(merged_external_node_path, 'w', encoding="UTF8") as merged_externalNode:
    #     for line in result_without_elevator_XtoX.readlines():
    #         destination = line.split()[1]
    #         edge = destination.split(':')[1]
    #         destination = destination.split(':')[0]
    #         merged_externalNode.write(f'{line.split()[0]} {destination} {edge}\n')
    #     data = externalNode.read()
    #     merged_externalNode.write(data)
    #
    # externalNode.close()
    # result_without_elevator_XtoX.close()
    # merged_externalNode.close()

    external_nodes = open('HongikMap/static/data/external_node/external_node.txt', 'r', encoding='UTF8')
    with open('HongikMap/static/data/external_node/merged_external_node_with_elevator.txt', 'w', encoding='UTF8') as f:
        external_node_lines = [line for line in external_nodes.readlines()]
        f.writelines(external_node_lines)

        for line in models.get_same_building_XtoX(elevator=True):
            departure = line['departure_id']
            destination = line['destination_id']
            distance = line['distance']

            sentence = f'{departure} {destination} {distance} t\n'
            f.write(sentence)
    external_nodes.close()

    external_nodes = open('HongikMap/static/data/external_node/external_node.txt', 'r', encoding='UTF8')
    with open('HongikMap/static/data/external_node/merged_external_node_without_elevator.txt', 'w',
              encoding='UTF8') as f:
        external_node_lines = [line for line in external_nodes.readlines()]
        f.writelines(external_node_lines)

        for line in models.get_same_building_XtoX(elevator=False):
            departure = line['departure_id']
            destination = line['destination_id']
            distance = line['distance']

            sentence = f'{departure} {destination} {distance} t\n'
            f.write(sentence)
    external_nodes.close()


def building_preprocessing(request):
    building = request.POST.get('building')
    if building == 'ALL':
        print('all building')
        preprocessing(request)
    else:
        specific_preprocessing(building)
    return JsonResponse({})


def preprocessing(request):
    # 동적으로 생긴 XtoX에 똑같은 자료가 다시 들어가는 것을 방지하기위해 초기화
    open("HongikMap/static/data/external_node/result_with_elevator_XtoX.txt", 'w', encoding="UTF8").close()
    open("HongikMap/static/data/external_node/result_without_elevator_XtoX.txt", 'w', encoding="UTF8").close()
    # 각 파일별로 읽어낸다. listdir은 디렉토리의 파일명을 리스트로 저장, join은 두 경로를 합쳐준다.
    for filename in os.listdir("HongikMap/static/data/all_buildings_data"):
        with open(os.path.join("HongikMap/static/data/all_buildings_data", filename), 'r', encoding="UTF8") as f:
            # print(filename)
            compute(f, filename)

    XToXDataization()
    compute_XtoX()
    # 외부노드에 대한 다익스트라를 돌린다.
    # with open('HongikMap/static/data/external_node/merged_external_node.txt', 'r', encoding="UTF8") as f:
    #     compute(f, 'external_node.txt')


def XtoX_preprocessing(request):
    XToXDataization()
    compute_XtoX()
    # 외부노드에 대한 다익스트라를 돌린다.
    # with open('HongikMap/static/data/external_node/merged_external_node.txt', 'r', encoding="UTF8") as f:
    #     compute(f, 'external_node.txt')

    return JsonResponse({})


def specific_preprocessing(building: str):
    # print(f'specific_preprocessing : {building}')
    file_path = f'HongikMap/static/data/all_buildings_data/{building}.txt'
    with open(file_path, "r", encoding="UTF8") as f:
        compute(f, f'{building}.txt')

    XToXDataization()
    compute_XtoX()
