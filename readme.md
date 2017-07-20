# Mars Rover Guidance System 

(Problem statement is not repeated here so Google doesn't find it.)

The Mars Rover Guidance System takes the command file, validates that the trip is safe, that all systems work, and then sends the commands to the rover. 

We supply a handy map so that we can see what the rover will cover.

## Guidance System Description

The position, `P`, and direction, `D`, of the rover completely determines the state of the rover. So we can represent the rover with the pair `[P, D]`. 

An instruction given to the rover is then a transformation on its current state. 

When the rover is given the instruction `L` or `R`, this is a transformation on its direction. We can represent this as 

> `L[P, D] = [P, L(D)]`  
> `R[P, D] = [P, R(D)]`

The direction of the rover is one of the four positions `N`, `S`, `E`, or `W`. The rover can only have one direction at a time. The commands `L` and `R` make the following transformations on direction:

> `L(N) = W`, `L(S) = E`, `L(E) = N`, `L(W) = S`  
> `R(W) = N`, `R(E) = S`, `R(N) = E`, `R(S) = W`
  
So if the rover has the state `[P, E]`, then `R[P, E] = [P, R(E)] = [P, S]`

The position of the rover is a set of coordinates. When the rover moves, it takes a unit step in the direction it is pointing. So it would seem natural to then represent the direction of the rover as appropriate unit vectors. So we can then have that 
 
 > `N = [0, 1]`, `S = [0, -1]`, `E = [1, 0]`, and `W = [-1, 0]`.
 
 Knowing that the commands `R` and `L` are rotations, and we have represented each direction as a vector, so make a transformation on the rover's direction, we simply rotate our direction vectors using a [rotation matrix](https://en.wikipedia.org/wiki/Rotation_matrix). 
 
 When a rover moves, with its position given by a vector (same as coordinate), and the direction it will move also a vector, the command `M` is simply the point-wise addition of the rovers current position and direction.
 
That is, 
> `M[P, D] = [P + D, D]`

Say the rover has current state `[[1, 2], E]`, moving the rover produces the state `[[1, 2] + E, E] = [[1, 2] + [1, 0], E] = [[2, 2], E]`. 

Since we produced an almost formal system in which the rover operates, to verify the correctness of our code, we need simply check that we can add two vectors, and rotate a vector. 

We don't even have to rotate an arbitrary vector by an arbitrary amount, we have 4 unit direction vectors, that can only be rotated left or right.

## Usage Instructions 

Missions must be given in a text formatted file with the extension `.rover`. The mission file needs to be in the same directory as the `rover.py` file. 

A mission file is the three lines:
> 8 8  
1 2 E  
MMLMRMMRRMML  

Note that there are no line spaces.

To run a mission, simply type `python rover.py`. Any mission file that ends with `.rover` will be automatically loaded. 
