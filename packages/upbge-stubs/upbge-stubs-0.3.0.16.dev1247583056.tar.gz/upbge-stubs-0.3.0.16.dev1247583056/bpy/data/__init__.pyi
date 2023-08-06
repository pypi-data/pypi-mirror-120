"""


Data Access (bpy.data)
**********************

This module is used for all Blender/Python access.

:data:`data`

.. code::

  import bpy


  # print all objects
  for obj in bpy.data.objects:
      print(obj.name)


  # print all scene names in a list
  print(bpy.data.scenes.keys())


  # remove mesh Cube
  if "Cube" in bpy.data.meshes:
      mesh = bpy.data.meshes["Cube"]
      print("removing mesh", mesh)
      bpy.data.meshes.remove(mesh)


  # write images into a file next to the blend
  import os
  with open(os.path.splitext(bpy.data.filepath)[0] + ".txt", 'w') as fs:
      for image in bpy.data.images:
          fs.write("%s %d x %d\n" % (image.filepath, image.size[0], image.size[1]))

"""

import bpy

import typing

data: bpy.types.BlendData = ...

"""

Access to Blender's internal data

"""
