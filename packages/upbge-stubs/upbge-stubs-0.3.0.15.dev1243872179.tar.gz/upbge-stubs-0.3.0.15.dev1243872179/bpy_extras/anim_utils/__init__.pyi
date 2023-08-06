"""


bpy_extras submodule (bpy_extras.anim_utils)
********************************************

:func:`bake_action`

:func:`bake_action_objects`

:func:`bake_action_iter`

:func:`bake_action_objects_iter`

"""

import typing

import bpy

def bake_action(obj: bpy.types.Object) -> bpy.types.Action:

  ...

def bake_action_objects(object_action_pairs: typing.Any) -> typing.Sequence[bpy.types.Action]:

  """

  A version of :func:`bake_action_objects_iter` that takes frames and returns the output.

  """

  ...

def bake_action_iter(obj: bpy.types.Object) -> bpy.types.Action:

  """

  An coroutine that bakes action for a single object.

  """

  ...

def bake_action_objects_iter(object_action_pairs: typing.Sequence[typing.Any]) -> None:

  """

  An coroutine that bakes actions for multiple objects.

  """

  ...
