# Copyright (c) 2019 Andrew Cassidy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

import bpy

bl_info = {
    "name": "Apply Parent Inverse",
    "author": "Andrew Cassidy",
    "blender": (2, 80, 0),
    "description": "Apply parent inverse without moving objects around",
    "category": "Object"
}


class OBJECT_OT_apply_parent_inverse(bpy.types.Operator):
    """Apply Parent Inverse"""
    bl_idname = "object.parent_apply"
    bl_label = "Apply Parent Inverse"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):  # execute() is called when running the operator
        obj = context.active_object

        # code from https://blender.stackexchange.com/a/28897

        # store a copy of the objects final transformation
        # so we can read from it later.
        ob_matrix_orig = obj.matrix_world.copy()

        # reset parent inverse matrix
        # (relationship created when parenting)
        obj.matrix_parent_inverse.identity()

        # re-apply the difference between parent/child
        # (this writes directly into the loc/scale/rot) via a matrix.
        obj.matrix_basis = obj.parent.matrix_world.inverted() @ ob_matrix_orig

        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_apply_parent_inverse.bl_idname)


# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(OBJECT_OT_apply_parent_inverse)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    # Note that in background mode (no GUI available), keyconfigs are not available either,
    # so we have to check this to avoid nasty errors in background case.
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(OBJECT_OT_apply_parent_inverse.bl_idname, 'P', 'PRESS', ctrl=False, shift=True, alt=True)
        addon_keymaps.append((km, kmi))


def unregister():
    # Note: when unregistering, it's usually good practice to do it in reverse order you registered.
    # Can avoid strange issues like keymap still referring to operators already unregistered...
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(OBJECT_OT_apply_parent_inverse)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
