import bpy

def rename_object_in_scene(old_name, new_name):
    old_object = bpy.data.objects.get(old_name)
    old_object.name = new_name