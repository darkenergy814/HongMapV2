from django.db import models

NonExistentNode = '[NonExistentNode]: There is no such node'
NonExistentRoute = '[NonExistentRoute]: There is no such route'


# Create your models here.
class Node(models.Model):
    node = models.CharField(max_length=30, primary_key=True)

    class Meta:
        db_table = 'node'
        indexes = [
            models.Index(fields=['node'], name='node_idx')
        ]


class ResultWithElevator(models.Model):
    class Meta:
        db_table = 'result_with_elevator'
        constraints = [
            models.UniqueConstraint(
                fields=["departure", "destination"],
                name="UniqueConstraintWithElevator",
            )
        ]
        indexes = [
            models.Index(fields=['departure', 'destination'], name='result_with_elevator_idx'),
        ]

    departure = models.ForeignKey("Node", unique=False, db_column='departure',
                                  on_delete=models.CASCADE, related_name='departure_with_elevator')
    destination = models.ForeignKey("Node", unique=False, db_column='destination',
                                    on_delete=models.CASCADE, related_name='destination_with_elevator')
    distance = models.IntegerField()
    route = models.CharField(max_length=1000)


class ResultWithoutElevator(models.Model):
    class Meta:
        db_table = 'result_without_elevator'
        constraints = [
            models.UniqueConstraint(
                fields=["departure", "destination"],
                name="UniqueConstraintWithoutElevator",
            )
        ]
        indexes = [
            models.Index(fields=['departure', 'destination'], name='result_without_elevator_idx'),
        ]

    departure = models.ForeignKey("Node", unique=False, db_column='departure',
                                  on_delete=models.CASCADE, related_name='departure_without_elevator')
    destination = models.ForeignKey("Node", unique=False, db_column='destination',
                                    on_delete=models.CASCADE, related_name='destination_without_elevator')
    distance = models.IntegerField()
    route = models.CharField(max_length=1000)


class Coordinate(models.Model):
    class Meta:
        db_table = 'coordinate'

    node = models.OneToOneField("Node", db_column='node', primary_key=True, on_delete=models.CASCADE,
                                related_name='coordinate_node')
    x = models.IntegerField()
    y = models.IntegerField()


class Recommendation(models.Model):
    class Meta:
        db_table = 'recommendation'
        indexes = [
            models.Index(fields=['recommendation'], name='recommendation_idx')
        ]

    node = models.OneToOneField("Node", db_column='node', primary_key=True, on_delete=models.CASCADE,
                                related_name='recommendation_node')
    recommendation = models.CharField(max_length=50)


def initialize_database():
    pass


def initialize_table():
    pass


def clean():
    pass


def save(result: dict, elevator: bool):
    # print(f'Save New Data with{"" if elevator else "out"} elevator')
    create_results_with_elevator = []
    create_results_without_elevator = []
    update_results_with_elevator = []
    update_results_without_elevator = []

    for (start, end), value in result.items():
        if not exist_node(start):
            Node(node=start).save()
        if not exist_node(end):
            Node(node=end).save()
        departure = Node.objects.get(node=start)
        destination = Node.objects.get(node=end)
        distance = value['distance']
        route = ','.join(value['route'])

        if exist_route(start, end, elevator):
            print(f'update data | {start} {end} elevator={elevator}')
            update_result = None
            if elevator:
                update_result = ResultWithElevator.objects.get(departure=departure, destination=destination)
                update_result.distance = distance
                update_result.route = route
                update_results_with_elevator.append(update_result)
            if not elevator:
                update_result = ResultWithoutElevator.objects.get(departure=departure, destination=destination)
                update_result.distance = distance
                update_result.route = route
                update_results_without_elevator.append(update_result)
            # update_result.save()
        if not exist_route(start, end, elevator):
            print(f'create data | {start} {end} elevator={elevator}')
            if elevator:
                result_with_elevator = ResultWithElevator(departure=departure, destination=destination,
                                                          distance=distance, route=route)
                # result_with_elevator.save()
                create_results_with_elevator.append(result_with_elevator)
            if not elevator:
                result_without_elevator = ResultWithoutElevator(departure=departure, destination=destination,
                                                                distance=distance, route=route)
                # result_without_elevator.save()
                create_results_without_elevator.append(result_without_elevator)

    ResultWithElevator.objects.bulk_create(create_results_with_elevator)
    ResultWithoutElevator.objects.bulk_create(create_results_without_elevator)

    ResultWithElevator.objects.bulk_update(update_results_with_elevator, ['distance', 'route'])
    ResultWithoutElevator.objects.bulk_update(update_results_without_elevator, ['distance', 'route'])


def save_recommendation(rooms: list):
    create_recommendations = []
    update_recommendations = []

    for room in rooms:
        if not exist_node(room):
            Node(node=room).save()
        node = Node.objects.get(node=room)

        building, floor, entity = room.split('-')
        if floor.startswith('B'):
            floor = f'0{floor[1:]}'
            recommendation = f'{building}{floor}{entity}'
        else:
            if "_" in entity:
                prefix_entity, postfix_entity = entity.split("_")
                recommendation = f'{building}{floor}{prefix_entity:0>2}_{postfix_entity}'
            else:
                recommendation = f'{building}{floor}{entity:0>2}'
            # recommendation = f'{building}{floor}{entity if "_" in entity else entity:0>2}'
        # recommendation = f'{building}{floor}{entity:0>2}'
        if not Recommendation.objects.filter(node=node).exists():
            create_recommendation = Recommendation(node=node, recommendation=recommendation)
            create_recommendations.append(create_recommendation)
            # Recommendation(node=node, recommendation=recommendation).save()
        else:
            update_recommendation = Recommendation.objects.get(node=node)
            update_recommendation.recommendation = recommendation
            update_recommendations.append(update_recommendation)
    Recommendation.objects.bulk_create(create_recommendations)
    Recommendation.objects.bulk_update(update_recommendations, ['recommendation'])


def get_route(start: str, end: str, elevator: bool) -> dict:
    if not exist_node(start) or not exist_node(end):
        return {}
    departure = Node.objects.get(node=start)
    destination = Node.objects.get(node=end)

    if elevator:
        if not exist_route(start, end, elevator):
            print(f'NonExistentRoute: There is no such route | ({start}, {end})')
            return {}
        retrieved_route = ResultWithElevator.objects.filter(departure=departure,
                                                            destination=destination).values('distance', 'route').first()
        distance = retrieved_route['distance']
        route = retrieved_route['route'].split(',')
        return {
            'distance': distance,
            'route': route
        }

    if not elevator:
        if not exist_route(start, end, elevator):
            print(f'NonExistentRoute: There is no such route | ({start}, {end})')
            return {}
        retrieved_route = ResultWithoutElevator. \
            objects.filter(departure=departure, destination=destination).values('distance', 'route').first()
        distance = retrieved_route['distance']
        route = retrieved_route['route'].split(',')
        return {
            'distance': distance,
            'route': route
        }


def get_coordinate(node: str) -> (int, int):
    node = Node(node=node)
    if not Node.objects.filter(node=node.node).exists():
        node.save()
    if not Coordinate.objects.filter(node=node).exists():
        print('NonExistentCoordinate: There is no such coordinate')
        return ()

    return Coordinate.objects.filter(node=node).values()[0]


def get_routes_of_start_building(start: str, elevator: bool) -> list:
    if not exist_node(start):
        return []

    departure = Node.objects.get(node=start)
    if elevator:
        if not ResultWithElevator.objects.filter(departure=departure).exists():
            print(NonExistentRoute)
            return []
        building = start.split('-')[0]
        routes = [{'distance': result['distance'], 'route': result['route'].split(',')} for result in
                  ResultWithElevator.objects.filter(departure=departure, destination__node__startswith=building,
                                                    destination__node__contains='X').values('distance', 'route')]
        return routes

    if not elevator:
        if not ResultWithoutElevator.objects.filter(departure=departure).exists():
            print(NonExistentRoute)
            return []
        building = start.split('-')[0]
        routes = [{'distance': result['distance'], 'route': result['route'].split(',')} for result in
                  ResultWithoutElevator.objects.filter(departure=departure, destination__node__startswith=building,
                                                       destination__node__contains='X').values('distance', 'route')]
        return routes


def get_routes_of_end_building(end: str, elevator: bool) -> list:
    if not exist_node(end):
        return []
    destination = Node.objects.get(node=end)
    if elevator:
        if not ResultWithElevator.objects.filter(destination=destination).exists():
            print(NonExistentRoute)
            return []
        building = end.split('-')[0]
        routes = [{'distance': result['distance'], 'route': result['route'].split(',')} for result in
                  ResultWithElevator.objects.filter(departure__node__startswith=building, departure__node__contains='X',
                                                    destination=destination).values('distance', 'route')]
        return routes

    if not elevator:
        if not ResultWithoutElevator.objects.filter(destination=destination).exists():
            print(NonExistentRoute)
            return []
        building = end.split('-')[0]
        routes = [{'distance': result['distance'], 'route': result['route'].split(',')} for result in
                  ResultWithoutElevator.objects.filter(departure__node__startswith=building,
                                                       departure__node__contains='X',
                                                       destination=destination).values('distance', 'route')]
        return routes


def get_same_building_XtoX(elevator: bool) -> list:
    result = []
    if elevator:
        XtoX = ResultWithElevator.objects.filter(departure__node__contains='X',
                                                 destination__node__contains='X').values()
    else:
        XtoX = ResultWithoutElevator.objects.filter(departure__node__contains='X',
                                                    destination__node__contains='X').values()

    for route in XtoX:
        if is_same_building(route):
            result.append(route)
    return result


def is_same_building(route: dict) -> bool:
    return route['departure_id'][0] == route['destination_id'][0]


def is_out_building(node: str) -> bool:
    return node.startswith('OUT')


def get_recommendation(keyword: str) -> list:
    result = []
    for node in Recommendation.objects.filter(recommendation__contains=keyword).values('node'):
        if is_out_building(node['node']):
            continue
        result.append(node['node'])
    return result


def exist_node(node: str) -> bool:
    if Node.objects.filter(node=node).exists():
        return True
    print(NonExistentNode, node)
    return False


def exist_route(start: str, end: str, elevator: bool) -> bool:
    if not exist_node(start):
        return False

    if not exist_node(end):
        return False
    departure = Node.objects.get(node=start)
    destination = Node.objects.get(node=end)
    if elevator:
        return ResultWithElevator.objects.filter(departure=departure, destination=destination).exists()
    if not elevator:
        return ResultWithoutElevator.objects.filter(departure=departure, destination=destination).exists()


def exist_recommendations(node: str) -> bool:
    if not exist_node(node):
        return False
    retrieved_node = Node.objects.get(node=node)
    if Recommendation.objects.filter(node=retrieved_node).exists():
        return True
    else:
        return False
