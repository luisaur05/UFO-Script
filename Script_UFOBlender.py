import random
import time
import math
import bpy
import numpy as np
from math import radians, cos, sin
from mathutils import Vector

def purge_orphans():
    if bpy.app.version >= (3, 0, 0):
        # run this only for Blender versions 3.0 and higher
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    else:
        # run this only for Blender versions lower than 3.0
        # call purge_orphans() recursively until there are no more orphan data blocks to purge
        result = bpy.ops.outliner.orphans_purge()
        if result.pop() != "CANCELLED":
            purge_orphans()


def clean_scene():
    # make sure the active object is not in Edit Mode
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()

    # make sure non of the objects are hidden from the viewport, selection, or disabled
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False

    # select all the object and delete them (just like pressing A + X + D in the viewport)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # find all the collections and remove them
    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])

    # in the case when you modify the world shader
    # delete and recreate the world object
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


def active_object():
    return bpy.context.active_object


def time_seed():
    seed = time.time()
    print(f"seed: {seed}")
    random.seed(seed)

    # add the seed value to your clipboard
    bpy.context.window_manager.clipboard = str(seed)

    return seed


def add_ctrl_empty(name=None):

    bpy.ops.object.empty_add(type="PLAIN_AXES", align="WORLD")
    empty_ctrl = active_object()

    if name:
        empty_ctrl.name = name
    else:
        empty_ctrl.name = "empty.cntrl"

    return empty_ctrl


def apply_material(material):
    obj = active_object()
    obj.data.materials.append(material)


def make_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def track_empty(obj):
    empty = add_ctrl_empty(name=f"empty.tracker-target.{obj.name}")

    make_active(obj)
    bpy.ops.object.constraint_add(type="TRACK_TO")
    bpy.context.object.constraints["Track To"].target = empty

    return empty


def setup_camera(loc, rot):
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    camera = active_object()

    # set the camera as the "active camera" in the scene
    bpy.context.scene.camera = camera

    # set the Focal Length of the camera
    camera.data.lens = 70

    camera.data.passepartout_alpha = 0.9

    empty = track_empty(camera)

    return empty


def set_1080px_square_render_res():
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080



def get_random_color():
    return random.choice(
        [
            [0.984375, 0.4609375, 0.4140625, 1.0],
            [0.35546875, 0.515625, 0.69140625, 1.0],
            [0.37109375, 0.29296875, 0.54296875, 1.0],
            [0.8984375, 0.6015625, 0.55078125, 1.0],
            [0.2578125, 0.9140625, 0.86328125, 1.0],
            [0.80078125, 0.70703125, 0.59765625, 1.0],
            [0.0, 0.640625, 0.796875, 1.0],
            [0.97265625, 0.33984375, 0.0, 1.0],
            [0.0, 0.125, 0.24609375, 1.0],
            [0.67578125, 0.93359375, 0.81640625, 1.0],
            [0.375, 0.375, 0.375, 1.0],
            [0.8359375, 0.92578125, 0.08984375, 1.0],
            [0.92578125, 0.16796875, 0.19921875, 1.0],
            [0.84375, 0.3515625, 0.49609375, 1.0],
            [0.58984375, 0.734375, 0.3828125, 1.0],
            [0.0, 0.32421875, 0.609375, 1.0],
            [0.9296875, 0.640625, 0.49609375, 1.0],
            [0.0, 0.38671875, 0.6953125, 1.0],
            [0.609375, 0.76171875, 0.83203125, 1.0],
            [0.0625, 0.09375, 0.125, 1.0],
        ]
    )


def render_loop():
    bpy.ops.render.render(animation=True)


def create_background():
    create_floor()


def create_metal_ring_material():
    color = get_random_color()
    material = bpy.data.materials.new(name="metal_ring_material")
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    material.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
    return material


def create_floor_material():
    color = get_random_color()
    material = bpy.data.materials.new(name="floor_material")
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    if bpy.app.version < (4, 0, 0):
        material.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 0
    else:
        material.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0
    return material


def create_floor():
    # add a plain into the scene
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -6.0))
    floor_obj = active_object()
    floor_obj.name = "plane.floor"

    # create and assign an emissive material
    floor_material = create_floor_material()
    floor_obj.data.materials.append(floor_material)


def add_light():
    # add area light
    bpy.ops.object.light_add(type="AREA")
    area_light = active_object()

    # update scale and location
    area_light.location.z = 6
    area_light.scale *= 10

    # set the light's energy
    area_light.data.energy = 1000


def clear_keyframes(obj):
    obj.animation_data_clear()

def animate_object(obj):
    # Define locations and times for the keyframes
    keyframes = [
        (0, Vector((0, 0, 0))),
        (20, Vector((3, 3, 1))),
        (40, Vector((10, 0, 2))),
        (60, Vector((7, -3, 1))),
        (80, Vector((-10, 3, 0))),
        (100, Vector((-4, 2, 2))),
        (120, Vector((8, 2, 1))),
        (140, Vector((0 , 0, 0))),
    ]
    
    # Insert keyframes
    for frame, location in keyframes:
        obj.location = location
        obj.keyframe_insert(data_path="location", frame=frame)

    # Apply interpolation to the keyframes
    for fcurve in obj.animation_data.action.fcurves:
        for i, keyframe in enumerate(fcurve.keyframe_points):
            if i < 4:  # First 4 keyframes (Hermite interpolation)
                keyframe.interpolation = 'CUBIC'  # Hermite is a type of cubic
            else:  # Next 4 keyframes (Bezier interpolation)
                keyframe.interpolation = 'BEZIER'

  
    
def create_flying_saucer():
    # Clear existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create the body of the flying saucer
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.5, location=(0, 0, 0))
    body = bpy.context.object
    body.name = "Body"
    
    # Flatten the body
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.resize(value=(1, 1, 0.25))  # Flatten more
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create the dome
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.8, location=(0, 0, 0.4))
    dome = bpy.context.object
    dome.name = "Dome"
   
    # Join body and dome
    bpy.ops.object.select_all(action='DESELECT')
    body.select_set(True)
    dome.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    
    # Apply metal material to the body
    metal_material = create_metal_ring_material()
    apply_material(metal_material)

    # Create legs with more details
    legs = []
    leg_height = 0.5
    for i in range(4):
        angle = i * 90
        x = 1.1 * cos(radians(angle))
        y = 1.1 * sin(radians(angle))

        # Create the top part of the leg
        bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.3, location=(x, y, -leg_height + 0.1))
        top_leg = bpy.context.object
        top_leg.name = f"Top_Leg_{i + 1}"
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.resize(value=(1, 1, 2))  # Make the legs longer
        bpy.ops.object.mode_set(mode='OBJECT')

        # Create the bottom part of the leg
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.2, location=(x, y, -leg_height))
        bottom_leg = bpy.context.object
        bottom_leg.name = f"Bottom_Leg_{i + 1}"

        # Create joints for the legs
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.1, location=(x, y, -leg_height + 0.1))
        joint = bpy.context.object
        joint.name = f"Joint_{i + 1}"

        # Group the leg parts
        bpy.ops.object.select_all(action='DESELECT')
        top_leg.select_set(True)
        bottom_leg.select_set(True)
        joint.select_set(True)
        bpy.context.view_layer.objects.active = top_leg
        bpy.ops.object.join()

        # Add details to the legs
        bpy.ops.mesh.primitive_cube_add(size=0.1, location=(x, y, -leg_height - 0.15))
        foot = bpy.context.object
        foot.name = f"Foot_{i + 1}"
        bpy.ops.transform.resize(value=(0.5, 0.5, 0.1))  # Make the leg base wider

        # Add the top leg object to the list of legs
        legs.append(top_leg)  # Append the final top leg to the list

    # Create lights on the body
    lights = []
    for i in range(8):
        angle = i * 45
        x = 1.2 * cos(radians(angle))
        y = 1.2 * sin(radians(angle))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(x, y, 0.2))
        light = bpy.context.object
        light.name = f"Light_{i + 1}"

        # Apply emissive material to the lights
        emissive_material = create_emissive_material()
        apply_material(emissive_material)
        lights.append(light)

    # Group all parts of the flying saucer
    bpy.ops.object.select_all(action='DESELECT')
    body.select_set(True)
    for leg in legs:
        leg.select_set(True)
    for light in lights:
        light.select_set(True)
    
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()  # Join everything into one single object

    # Rename the object to "FlyingSaucer"
    flying_saucer = bpy.context.object
    flying_saucer.name = "FlyingSaucer"
    
    
    return flying_saucer


def create_emissive_material():
    material = bpy.data.materials.new(name="Emissive Material")
    material.use_nodes = True
    principled_bsdf = material.node_tree.nodes.get("Principled BSDF")
    
    # Establecer propiedades de emisión
    if bpy.app.version < (4, 0, 0):
        principled_bsdf.inputs["Emission"].default_value = (1.0, 1.0, 0.0, 1)  # Color amarillo
    else:
        principled_bsdf.inputs["Emission Color"].default_value = (1.0, 1.0, 0.0, 1)  # Color amarillo
    
    principled_bsdf.inputs["Emission Strength"].default_value = 20.0  # Ajusta la fuerza de emisión como desees
    return material



 

# Function to create the path
def create_path(keyframes):
    # Create a new curve
    curve_data = bpy.data.curves.new(name="CubePath", type='CURVE')
    curve_data.dimensions = '3D'
    
    # Create a new polyline spline
    polyline = curve_data.splines.new(type='BEZIER')  # Change to BEZIER for smooth curves

    # Prepare the polyline with the required number of points
    polyline.bezier_points.add(len(keyframes) - 1)  # Add enough points to match keyframes

    # Add points for the path
    for i, (_, location) in enumerate(keyframes):
        point = polyline.bezier_points[i]  # Access the correct point
        point.co = (location.x, location.y, location.z)  # Set point coordinates
        point.handle_left_type = 'AUTO'  # Set handle type to AUTO for smooth curves
        point.handle_right_type = 'AUTO'

    # Create the object from the curve
    path_obj = bpy.data.objects.new("CubePath", curve_data)
    bpy.context.collection.objects.link(path_obj)
    
    return path_obj

# Function to calculate the length of a Bezier spline curve
def calculate_arc_lengths(path):
    # Get the curve points
    spline = path.data.splines[0]
    bezier_points = spline.bezier_points
    
    # Calculate distances between consecutive points
    arc_lengths = [0.0]  # Start with 0
    total_length = 0.0
    
    for i in range(1, len(bezier_points)):
        # Calculate the distance between consecutive points
        prev_point = bezier_points[i - 1].co
        curr_point = bezier_points[i].co
        segment_length = (curr_point - prev_point).length
        total_length += segment_length
        arc_lengths.append(total_length)
    
    return np.array(arc_lengths), total_length

# Function to calculate arc length and create a driver for constant speed
def setup_arc_length_driver(cube, path, arc_lengths, total_length):
    # Add a custom property to control speed
    cube["speed"] = 1.0  # Speed factor

    # Create a driver for the cube's location along the curve
    driver_x = cube.driver_add("location", 0).driver
    driver_y = cube.driver_add("location", 1).driver
    driver_z = cube.driver_add("location", 2).driver

    # Driver expression for each axis
    driver_x.expression = "speed_based_position(frame, 0)"
    driver_y.expression = "speed_based_position(frame, 1)"
    driver_z.expression = "speed_based_position(frame, 2)"

    # Use a Python expression for the driver function
    bpy.app.driver_namespace["speed_based_position"] = lambda frame, axis: interpolate_position(frame, axis, arc_lengths, total_length, path)

# Function to interpolate the position of the cube based on arc length
def interpolate_position(frame, axis, arc_lengths, total_length, path):
    # Normalize the time (frame) to a value between 0 and 1
    normalized_time = frame / bpy.context.scene.frame_end

    # Find the corresponding length along the curve
    target_length = normalized_time * total_length
    
    # Find the segment of the curve where the target length falls
    for i in range(1, len(arc_lengths)):
        if target_length <= arc_lengths[i]:
            t = (target_length - arc_lengths[i-1]) / (arc_lengths[i] - arc_lengths[i-1])
            point_prev = path.data.splines[0].bezier_points[i-1].co
            point_next = path.data.splines[0].bezier_points[i].co
            # Linear interpolation between the two points based on t
            return point_prev[axis] + t * (point_next[axis] - point_prev[axis])
    
    return 0.0  # Fallback in case something goes wrong


def main():

    obj = create_flying_saucer()
    create_background()
    add_light()
    animate_object(obj)

    # Create the path based on the keyframes
    keyframes = [
        (0, Vector((0, 0, 0))),
        (20, Vector((3, 3, 1))),
        (40, Vector((10, 0, 2))),
        (60, Vector((7, -3, 1))),
        (80, Vector((-10, 3, 0))),
        (100, Vector((-4, 2, 2))),
        (120, Vector((8, 2, 1))),
        (140, Vector((0  , 0, 0))),
    ]
    path_obj = create_path(keyframes)

    # Calculate the arc lengths for the path
    arc_lengths, total_length = calculate_arc_lengths(path_obj)

    # Set up the arc length driver for constant speed
    setup_arc_length_driver(obj, path_obj, arc_lengths, total_length)

    # Optionally, set the end frame of the animation
    bpy.context.scene.frame_end = 140


if __name__ == "__main__":
    main()