# Rubiks Cube Solver

This is the code for my rubiks cube solving robot. It uses a webcam to scan the cube, and then uses a Kociemba algorithm implementation to solve the cube. The robot will be built using a Arduino, and use stepper motors to rotate the cube.

## Showcase

Images of the robot will be added here once it is built.

## Getting Started
Clone the repository to your computer, and run the main.py file. You will need to have a webcam connected to your computer.

cd into repo and install the following dependencies using uv.

-   OpenCV `uv add opencv-python`
-   Numpy `uv add numpy`
-   Kociemba `uv add kociemba`

### Run Project

```sh
uv run src/main.py
```
