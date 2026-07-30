At the core of this project is a 3d graphics engine I built from scratch using CMU CS Academy.
It includes:
- Custom linear algebra perspective projection (uses homogenous normalization)  
- Back-face culling & lighting
- Automatic mesh triangulation

I then layered a Rubik's Cube simulation above the graphics engine.
It includes:
- Custom animation infrastructure for Rubik's cube rotations
- User keypad control & constrained orbiting

Here is the finished demo: https://academy.cs.cmu.edu/sharing/antiqueWhiteCamel100435
- use wasd and arrow keys to move around and rotate view

For this project, I saved my code as the project underwent development, so here are some earlier versions:
(i think they are cool because you can see some of the backend functionality that is not visible in the final version)

v1 - the core rendering math: https://academy.cs.cmu.edu/sharing/yellowGreenBird3460

v2 - lighting and mesh triangulation: https://academy.cs.cmu.edu/sharing/tanBear5471

v3 - re-triangulating meshes when faces become partially occluded: https://academy.cs.cmu.edu/sharing/turquoiseScorpion6536

v4 - start of Rubiks cube: https://academy.cs.cmu.edu/sharing/greenEagle3202

v5 - Finished!
