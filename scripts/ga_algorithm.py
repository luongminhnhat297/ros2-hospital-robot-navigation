#!/usr/bin/env python3

import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
import random
import time
import json
import math
import sys

ROOMS = {
    'Phong_1': (-7.1, 4.6),
    'Phong_2': (-3.65, 7.75),
    'Phong_3': (0.05, 10.14),
    'Phong_4': (5.38, 10.0),
    'Phong_5': (14.44, 8.52),
    'Phong_6': (10.45, 7.14),
    'Phong_7': (28.09, 8.32),
    'Phong_8': (24.35, 7.14),
    'Phong_9': (38.73, 3.35),
    'Phong_10': (28.9, 2.22),
    'Phong_11': (28.26, -2.57),
    'Phong_12': (21.9, 1.81),
    'Phong_13': (22.17, -1.71),
    'Phong_14': (14.03, 1.22),
    'Phong_15': (14.01, -1.45),
    'Phong_16': (-7.01, -4.52),
    'Phong_17': (-3.72, -8.13),
    'Phong_18': (0.8, -10.33),
    'Phong_19': (4.98, -10.31),
    'Phong_20': (14.42, -8.21),
    'Phong_21': (10.6, -7.12),
    'Phong_22': (28.42, -8.11),
    'Phong_23': (24.45, -7.17),
    'Phong_24': (38.8, -8.19),
}

try:
    with open('distance_matrix.json', 'r') as f:
        DISTANCE_MATRIX = json.load(f)
except:
    print("[ERROR] Missing distance_matrix.json")
    sys.exit()

START_TO_ROOM_DISTANCES = {}

# ==========================================
# 🔥 FIX QUAN TRỌNG: dùng Nav2 path thật
# ==========================================
def get_path_length(nav, sx, sy, gx, gy):

    # filter nhanh bằng khoảng cách Euclidean
    if math.hypot(sx - gx, sy - gy) > 30:
        return float('inf')

    start = PoseStamped()
    start.header.frame_id = 'map'
    start.pose.position.x = sx
    start.pose.position.y = sy

    goal = PoseStamped()
    goal.header.frame_id = 'map'
    goal.pose.position.x = gx
    goal.pose.position.y = gy

    path = nav.getPath(start, goal)

    if not path or len(path.poses) < 2:
        return float('inf')

    dist = 0.0
    for i in range(len(path.poses)-1):
        p1 = path.poses[i].pose.position
        p2 = path.poses[i+1].pose.position
        dist += math.hypot(p1.x - p2.x, p1.y - p2.y)

    return dist

# ==========================================
# DISTANCE
# ==========================================
def route_distance(route):
    dist = START_TO_ROOM_DISTANCES.get(route[0], float('inf'))

    for i in range(len(route)-1):
        d = DISTANCE_MATRIX[route[i]][route[i+1]]
        if d == float('inf'):
            return float('inf')
        dist += d

    return dist

# ==========================================
# GA (giữ nguyên)
# ==========================================
def create_route(rooms):
    r = rooms[:]
    random.shuffle(r)
    return r

def tournament_selection(pop, k=5):
    return min(random.sample(pop, k), key=route_distance)

def crossover(p1, p2):
    size = len(p1)
    if size < 2:
        return p1[:]

    a, b = sorted(random.sample(range(size), 2))
    child = [None]*size
    child[a:b] = p1[a:b]

    fill = [x for x in p2 if x not in child]
    idx = 0
    for i in range(size):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    return child

def mutate(route):
    r = random.random()
    size = len(route)

    if size < 2:
        return

    if r < 0.33:
        i, j = random.sample(range(size), 2)
        route[i], route[j] = route[j], route[i]

    elif r < 0.66:
        i, j = sorted(random.sample(range(size), 2))
        route[i:j] = reversed(route[i:j])

    else:
        i, j = sorted(random.sample(range(size), 2))
        sub = route[i:j]
        random.shuffle(sub)
        route[i:j] = sub

def two_opt(route):
    best = route
    improved = True

    while improved:
        improved = False
        for i in range(1, len(route)-2):
            for j in range(i+1, len(route)):
                new_route = route[:]
                new_route[i:j] = reversed(route[i:j])

                if route_distance(new_route) < route_distance(best):
                    best = new_route
                    improved = True
        route = best
    return best

def run_ga(rooms, pop_size=80, generations=200):

    population = [create_route(rooms) for _ in range(pop_size)]

    best = float('inf')
    stagnation = 0

    for gen in range(generations):

        population = sorted(population, key=route_distance)
        current = route_distance(population[0])

        print(f"[GEN {gen}] Best = {current:.2f}")

        if abs(current - best) < 1e-3:
            stagnation += 1
        else:
            best = current
            stagnation = 0

        if stagnation > 30:
            print("[GA] Early stop")
            break

        mutation_rate = max(0.05, 0.2 * (1 - gen/generations))

        next_gen = population[:10]

        while len(next_gen) < pop_size:
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)

            child = crossover(p1, p2)

            if random.random() < mutation_rate:
                mutate(child)

            child = two_opt(child)

            next_gen.append(child)

        population = next_gen

    return min(population, key=route_distance)

def get_user_selection():
    names = list(ROOMS.keys())
    for i, n in enumerate(names):
        print(f"[{i+1}] {n}")

    while True:
        try:
            sel = list(map(int, input("Chọn phòng: ").split()))
            rooms = list(dict.fromkeys([names[i-1] for i in sel]))
            return rooms
        except:
            print("Sai input")

# ==========================================
# MAIN
# ==========================================
def main():
    rclpy.init()
    nav = BasicNavigator()
    nav.waitUntilNav2Active()

    while True:
        selected = get_user_selection()

        # 👉 lấy vị trí robot MỖI LẦN
        tf_buffer = Buffer()
        tf_listener = TransformListener(tf_buffer, nav)
        time.sleep(1)

        try:
            trans = tf_buffer.lookup_transform('map', 'base_footprint', rclpy.time.Time())
        except:
            trans = tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())

        cx = trans.transform.translation.x
        cy = trans.transform.translation.y

        START_TO_ROOM_DISTANCES.clear()

        # 👉 tính lại distance từ vị trí hiện tại
        for r in selected:
            rx, ry = ROOMS[r]
            dist = get_path_length(nav, cx, cy, rx, ry)

            if dist == float('inf'):
                continue

            START_TO_ROOM_DISTANCES[r] = dist
        
        valid_rooms = list(START_TO_ROOM_DISTANCES.keys())

        if not valid_rooms:
            print("❌ Không có phòng nào reachable!")
            continue

        # chạy GA
        best_route = run_ga(valid_rooms)

        print("Best route:", best_route)

        # execute
        poses = []
        for r in best_route:
            x, y = ROOMS[r]
            p = PoseStamped()
            p.header.frame_id = 'map'
            p.pose.position.x = x
            p.pose.position.y = y
            p.pose.orientation.w = 1.0
            poses.append(p)

        nav.goThroughPoses(poses)

        while not nav.isTaskComplete():
            time.sleep(0.5)

        print("DONE")

        # 👉 hỏi có chạy tiếp không
        cont = input("Chạy tiếp? (y/n): ")
        if cont.lower() != 'y':
            break

    rclpy.shutdown()

if __name__ == "__main__":
    main()