import sys
import os
import bpy
import colorsys
import math
from math import pi
from mathutils import Euler
tau = 2*pi

# Check if script is opened in Blender program


def createSphere(origin=(0, 0, 0)):
    # Create icosphere
    bpy.ops.mesh.primitive_ico_sphere_add(location=origin)
    obj = bpy.context.object
    return obj


def removeAll(type=None):
    # Possible type: ‘MESH’, ‘CURVE’, ‘SURFACE’, ‘META’, ‘FONT’, ‘ARMATURE’, ‘LATTICE’, ‘EMPTY’, ‘CAMERA’, ‘LAMP’
    if type:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type=type)
        bpy.ops.object.delete()
    else:
        # Remove all elements in scene
        bpy.ops.object.select_by_layer()
        bpy.ops.object.delete(use_global=False)


def rainbowLights(r=5, n=100, freq=2, energy=0.1):
    for i in range(n):
        t = float(i)/float(n)
        pos = (r*math.sin(tau*t), r*math.cos(tau*t), r*math.sin(freq*tau*t))

        # Create lamp
        bpy.ops.object.add(type='LAMP', location=pos)
        obj = bpy.context.object
        obj.data.type = 'POINT'

        # Apply gamma correction for Blender
        color = tuple(pow(c, 2.2) for c in colorsys.hsv_to_rgb(t, 0.6, 1))

        # Set HSV color and lamp energy
        obj.data.color = color
        obj.data.energy = energy


def setSmooth(obj, level=None, smooth=True):
    if level:
        # Add subsurf modifier
        modifier = obj.modifiers.new('Subsurf', 'SUBSURF')
        modifier.levels = level
        modifier.render_levels = level

    # Smooth surface
    mesh = obj.data
    for p in mesh.polygons:
        p.use_smooth = smooth


if __name__ == '__main__':
    # Remove all elements
    removeAll()

    # Create camera
    bpy.ops.object.add(type='CAMERA', location=(0, -3.5, 0))
    cam = bpy.context.object
    cam.rotation_euler = Euler((pi/2, 0, 0), 'XYZ')
    # Make this the current camera
    bpy.context.scene.camera = cam

    # Create lamps
    rainbowLights()

    # Create object and its material
    sphere = createSphere()
    setSmooth(sphere, 3)

    # Render image
    rnd = bpy.data.scenes['Scene'].render
    rnd.resolution_x = 500
    rnd.resolution_y = 500
    rnd.resolution_percentage = 100
    rnd.filepath = os.path.join(os.getcwd(), 'simple_sphere.png')
    bpy.ops.render.render(write_still=True)
