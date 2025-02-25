# Rubik's Cube Solver

This repository contains the code for my Rubik's Cube solving robot. The robot uses a webcam to scan the cube and implements the Kociemba algorithm to solve it. The robot is built using an Arduino and stepper motors to rotate the cube.

## Showcase

Images of the robot will be added here once it is built.

## Getting Started

Clone the repository and ensure all dependencies are installed.

### System Dependencies

- Python-tk (optional): On some systems, you might need to install `python-tk` to run this application. Install it using your system's package manager.

### Running the Project

Make sure [`uv`](https://docs.astral.sh/uv/getting-started/installation/) is installed on your system. This is optional, but the project was set up using [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for easier management, so I recommend using it.

1. Install dependencies and set up a virtual environment:
    ```sh
    uv sync
    source .venv/bin/activate
    ```

2. Run the project:
    ```sh
    uv run src/main.py
    ```
