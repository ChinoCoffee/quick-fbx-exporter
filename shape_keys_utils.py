# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>


import bpy


HIDDEN_WORKING_SCENE = 'FBX_shape_keys_temp'


def get_clean_hidden_working_scene(hidden_scene_name=HIDDEN_WORKING_SCENE):
    if hidden_scene_name in bpy.data.scenes:
        scene = bpy.data.scenes[hidden_scene_name]
        bpy.data.scenes.remove(scene)

    new_hidden_scene = bpy.data.scenes.new(name=hidden_scene_name)
    return new_hidden_scene


def remove_hidden_working_scene(hidden_scene_name=HIDDEN_WORKING_SCENE):
    if hidden_scene_name in bpy.data.scenes:
        scene = bpy.data.scenes[hidden_scene_name]
        bpy.data.scenes.remove(scene)


def generate_obj_with_mixed_shape_keys(obj, scene):
    if obj.type not in {'EMPTY', 'CAMERA', 'LAMP', 'ARMATURE', 'MESH'}:
        return

    dupe = obj.copy()
    dupe.data = obj.data.copy()

    scene.objects.link(dupe)

    if not dupe.data:
        return dupe   # Object("[0]Render.002") etc.

    if not dupe.type == 'MESH':
        return dupe

    old_key_blocks = list(dupe.data.shape_keys.key_blocks)
    num_old_key_blocks = len(old_key_blocks)
    mixed_key = dupe.shape_key_add(from_mix=True)

    for i in range(num_old_key_blocks):
        dupe.shape_key_remove(old_key_blocks[i])

    return dupe


def generate_scene_with_mixed_shape_keys(scene):
    bpy.ops.object.select_all(action='DESELECT')

    temp_scene = get_clean_hidden_working_scene()

    for ob_base in scene.objects:
        if not ob_base.data:
            continue
        dupe = generate_obj_with_mixed_shape_keys(ob_base, temp_scene)

    temp_scene.update()
    return temp_scene
