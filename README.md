# ParentZero

An addon, that allows to reset parent space offset or parent object A to B that way, when zero point of parent space is on the A object's origin. It is handy to know exactly where is 000.  Thanks to [ideasman42 on StackExchange](https://blender.stackexchange.com/a/28897/83714) for initial code that makes this possible.

Made for Blender 2.80 and above.

## Installation
To install, simply clone or copy this repository into your blender `addons` folder and enable it in the preferences like any other plugin.

## Usage
Addon adds menu options to Object->Parent and context->Parent.
Apply inverse for already existing shifted parent spaces and use new parent method as default.

This is the same as clearing the parent inverse and then moving/rotating/scaling the object to how it was before. Keep in mind that this does not work for any objects with shear!
Work with many objects
