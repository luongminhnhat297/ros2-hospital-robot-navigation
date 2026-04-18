![ROS2](https://img.shields.io/badge/ROS2-Jazzy-blue)
![Navigation](https://img.shields.io/badge/Nav2-MPPI-green)
![Status](https://img.shields.io/badge/status-active-success)

# Hospital Omni-directional Robot Navigation (ROS2)

> An autonomous multi-goal navigation system for hospital environments using ROS2, Nav2, and a Genetic Algorithm.

---

## Overview

This project implements an autonomous omnidirectional robot capable of navigating hospital-like environments and visiting multiple target locations in an optimized order.

Unlike standard navigation problems that focus on a single goal, this system solves a **multi-goal navigation problem**, similar to the Traveling Salesman Problem (TSP), where the objective is to minimize the total travel distance.

The system is designed in a modular way and integrates key components of a real robotic system, including SLAM, localization, navigation, task planning, and a user interface.

---

## Features

- Multi-goal navigation with optimized visiting order
- Route optimization using a Genetic Algorithm (GA)
- Uses actual path cost from Nav2 instead of Euclidean distance
- Re-planning when a goal becomes unreachable
- Simulation of complex hospital environments (rooms, corridors)
- Simple GUI for goal selection and monitoring

---

## System Architecture

Main components:

- **Gazebo** – simulation environment
- **Cartographer** – SLAM (map building)
- **robot_localization (EKF)** – sensor fusion
- **Nav2** – path planning and control
- **Genetic Algorithm** – goal ordering optimization
- **Navigation Controller** – execution and re-planning logic
- **GUI (PyQt5)** – user interaction

### Workflow

1. User selects target locations
2. Genetic Algorithm computes optimal order
3. Nav2 generates detailed paths
4. Robot executes navigation
5. If failure occurs → system re-plans

---

## Project Structure

```bash
robot_omni/
├── launch/
├── config/
├── urdf/
├── worlds/
├── map/
├── rviz/
├── models/
├── scripts/
├── gui/
└── CMakeLists.txt
```

---

## Installation

### Requirements

- ROS2 (Jazzy recommended)
- Nav2
- Cartographer
- robot_localization
- Gazebo (ros_gz)
- Python3 + PyQt5

### Install dependencies

```bash
sudo apt update
sudo apt install ros-jazzy-navigation2 \
                 ros-jazzy-nav2-bringup \
                 ros-jazzy-cartographer \
                 ros-jazzy-robot-localization \
                 python3-pyqt5
```

---

## Usage

### Launch the system

```bash
ros2 launch robot_omni navigation2_old.launch.py
```

### Run GUI

```bash
python3 gui/gui.py
```

### Modes

- `ga`: optimized route using Genetic Algorithm
- `sequential`: follow input order

---

## Algorithms

| Component        | Method              |
|------------------|---------------------|
| SLAM             | Cartographer        |
| Localization     | EKF                 |
| Navigation       | Nav2                |
| Controller       | MPPI                |
| Task Planning    | Genetic Algorithm   |

---

## Future Work

- Multi-robot support
- Task management system integration
- Deployment on real hardware
- Improved dynamic obstacle handling

---

## Contributing

If you find a bug or have suggestions, feel free to open an issue.

Pull requests are welcome.

---

## Authors

- Tran Huy Hau
- Luong Minh Nhat
- Tran Minh Quan

---

## Credits

- ROS2 Navigation (Nav2)
- Cartographer
- robot_localization

