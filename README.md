# Flying Saucer Animation Project in Blender with Interpolations

This project involves creating and animating a flying saucer using Blender and Python. The script automates object creation, material assignment, camera setup, and animation through trajectory interpolations.

## Features

### Orphan Data Purge
The `purge_orphans()` function clears orphaned data in the scene to free memory, supporting both Blender versions before 3.0 and 3.0+.

### Scene Cleanup
`clean_scene()` removes existing objects, collections, and unused materials, preparing the scene for new additions.

### Camera Setup
The `setup_camera()` function adds a camera, positions it, and orients it based on given coordinates and rotations. It also assigns a property to track a control object.

### Material Creation
Functions like `create_metal_ring_material()` and `create_floor_material()` generate materials with properties such as random colors and settings for reflection or light emission. The metallic material is applied to the saucer's body, and the floor material is used for the landing plane.

### Saucer Animation
The `animate_object()` function assigns a trajectory to the saucer using interpolations between key points. It utilizes 'CUBIC' and 'BEZIER' interpolations for smoother motion.

### Flying Saucer Creation
`create_flying_saucer()` is the primary function for building the 3D saucer model. It includes the body, dome, legs, and lights. It also applies materials like the metallic material for the body and emissive materials for the lights.

### Saucer Path Creation
The `create_path()` function creates a 3D curve representing the saucer's path. This function accepts a set of keyframes to define the saucer's positions and timing.

## Project Structure

### Key Functions:
- `purge_orphans()`: Removes orphaned data from the scene.
- `clean_scene()`: Cleans the scene by deleting unwanted objects and collections.
- `add_ctrl_empty()`: Creates an empty control object in the scene.
- `track_empty()`: Sets up a control for an object to "look at" a target.
- `animate_object()`: Adds keyframes to animate an object along a defined trajectory.
- `create_flying_saucer()`: Builds and assembles the flying saucer with its geometry and materials.
- `create_path()`: Generates a path for the saucer's animation.

### Saucer Components:
1. **Body**: A flattened UV sphere representing the saucer's main body.
2. **Dome**: An additional sphere placed atop the body.
3. **Legs**: Four cylindrical legs added to the bottom of the saucer.
4. **Lights**: Eight emissive lights positioned on the saucer's body.

### Interpolations
The saucer's movement is managed through 'CUBIC' and 'BEZIER' interpolations to ensure smooth transitions between keyframes.

## Requirements
- Blender 3.x or later.
- Basic knowledge of Python scripting for Blender.

## How to Run the Script
1. Open Blender.
2. Navigate to the scripting workspace.
3. Create a new script and paste the code.
4. Run the script to create and animate the flying saucer.

## Notes
- This project uses materials with nodes and specific configurations to achieve realistic visual effects, such as light emission from the saucer.
- The saucer's animation can be customized by adding or modifying keyframes in the `animate_object()` function.

## Demo Video
[https://youtu.be/ylmtM0hIKp8](https://youtu.be/ylmtM0hIKp8)
