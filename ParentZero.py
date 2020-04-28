# Copyright (c) 2019 Andrew Cassidy, Kobozev Vyacheslav

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

import bpy
from bpy.types import Operator

bl_info = {
	"name": "ParentZero",
	"version": (1,5),
	"author": "Andrew Cassidy, Kobozev Vyacheslav",
	"blender": (2, 80, 0),
	"description": "Parent with applied parent inverse and without moving objects",
	"category": "Object",
#	"location": "Object > Parent",
}
#poll function, returns true with appropriate conditions
def proper (c):
	A = c.area.type == 'VIEW_3D'
	M = c.mode == 'OBJECT'
	S = True if c.selected_objects else False
	return A and M and S

# key function --------------------------------------------------
def inverse_apply(sobjs):
	for ob in sobjs:
		# code from https://blender.stackexchange.com/a/28897
		# stores objects final transformation
		ob_matrix_orig = ob.matrix_world.copy()

		# reset parent inverse matrix (relationship created when parenting)
		ob.matrix_parent_inverse.identity()

		# re-apply the difference between parent/child
		# (this writes directly into the loc/scale/rot) via a matrix.
		ob.matrix_basis = ob.parent.matrix_world.inverted() @ ob_matrix_orig

#Operators -------------------------------------------------------
class OBJECT_OT_apply_parent_inverse(Operator):
	"""Apply Parent Inverse"""
	bl_idname = "object.parent_apply_inverse"
	bl_label = "Apply Parent Inverse"
	bl_context = "objectmode"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):  
		sobjs = bpy.context.selected_objects

		#calling key function
		inverse_apply(sobjs)

		return {'FINISHED'}

	@classmethod 
	def poll(cls,context):
		return proper(context)


class OBJECT_OT_parent_applied_inverse(Operator):
	"""Parent with inverse applied"""
	bl_idname = "object.parent_applied_inverse"
	bl_label = "Parent with applied inverse"
	bl_context = "objectmode"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		c=bpy.context
		bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
		sobjs = c.selected_objects
		sobjs.remove(c.active_object)

		#calling key function
		inverse_apply(sobjs)

		return {'FINISHED'}
	@classmethod 
	def poll(cls,context):
		SS = True if len(bpy.context.selected_objects)>1 else False
		return proper(context) and SS

		#function, that draws menu options
def menu_func(self, context):
	la = self.layout
	la.operator_context = "INVOKE_DEFAULT"
	la.operator(OBJECT_OT_apply_parent_inverse.bl_idname)
	la.operator(OBJECT_OT_parent_applied_inverse.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []

#list with operators for register cycle
classes = [
	OBJECT_OT_apply_parent_inverse,
	OBJECT_OT_parent_applied_inverse,
]


def register():
	for c in classes:
		bpy.utils.register_class(c)

	bpy.types.VIEW3D_MT_object_parent.append(menu_func)
	

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
	for c in classes:
		bpy.utils.unregister_class(c)

	bpy.types.VIEW3D_MT_object_parent.remove(menu_func)

	# Note: when unregistering, it's usually good practice to do it in reverse order you registered.
	# Can avoid strange issues like keymap still referring to operators already unregistered...
	# handle the keymap
	for km, kmi in addon_keymaps:
		km.keymap_items.remove(kmi)
	addon_keymaps.clear()

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
	register()
