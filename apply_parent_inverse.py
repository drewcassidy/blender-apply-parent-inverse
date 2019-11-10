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
    "blender": (2, 7, 0),
    "description": "Apply parent inverse without moving objects around",
    "category": "Object"
}


class ApplyParentInverse(bpy.types.Operator):
    """Apply Parent Inverse"""
    bl_idname = "object.parent_apply"
    bl_label = "Apply Parent Inverse"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):  # execute() is called when running the operator
        scene = context.scene
        for obj in scene.objects:
            # store a copy of the objects final transformation
            # so we can read from it later.
            ob_matrix_orig = obj.matrix_world.copy()

            # reset parent inverse matrix
            # (relationship created when parenting)
            obj.matrix_parent_inverse.identity()

            # re-apply the difference between parent/child
            # (this writes directly into the loc/scale/rot) via a matrix.
            obj.matrix_basis = obj.parent.matrix_world.inverted() * ob_matrix_orig

        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


def register():
    bpy.utils.register_class(ApplyParentInverse)


def unregister():
    bpy.utils.unregister_class(ApplyParentInverse)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
