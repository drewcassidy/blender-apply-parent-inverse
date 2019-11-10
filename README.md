# blender-apply-parent-inverse

A plugin to reset blender's parent inverse antifeature without breaking everything. Thanks to [ideasman42 on StackExchange](https://blender.stackexchange.com/a/28897/83714) for the code that makes this possible.

Currently 2.79 only, 2.80 version will come when I start using 2.80, or if enough people want it.

## Installation
To install, simply clone or copy this repository into your blender `addons` folder and enable it in the preferences like any other plugin.

## Usage
This plugin adds a single item called "Apply Parent Inverse" to the Object menu. By default, this action is bound to shift-option-P (shift-alt-p on windows and linux). 

Using this action will apply the current parent inverse to the active (most recently selected) object. This is the same as clearing the parent inverse and then moving/rotating/scaling the object to how it was before. Keep in mind that this does not work for any objects with shear!