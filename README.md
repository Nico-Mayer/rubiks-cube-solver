# Rubiks Cube Solver

This is the code for my rubiks cube solving robot. It uses a webcam to scan the cube, and then uses a Kociemba algorithm implementation to solve the cube. The robot will built using a Raspberry Pi 3, and will use stepper motors to rotate the cube.

## Showcase

Images of the robot will be added here once it is built.

## Getting Started

You can run the code on your own computer, but you will need to install the following dependencies:

-   OpenCV `pip install opencv-python`
-   Numpy `pip install numpy`
-   Kociemba `pip install kociemba`

Clone the repository to your computer, and run the main.py file. You will need to have a webcam connected to your computer.

```bash
git clone https://github.com/nico-mayer/rubiks-cube-solver.git

cd rubiks-cube-solver

python main.py
```
