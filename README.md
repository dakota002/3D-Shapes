# 3D-Shapes
3D shape maker

This program takes an input and creates a .stl file named "object.stl".
The stl file is in a format that can be imported into Blender and from there exported into another file type.

--2/23/16--
Creates random shapes for all inputs other than 4.
When input is 4, creates a triangular pyramid.


--2/25/16--
Creates cones based on input.
Added various vector functions.

--3/1/16--
Cones now have closed bases
  
--3/3/16--
Added reflection

--3/6/16--
Updated reflection.
Added cubes centered at origin.
Made some subtle changes to how and when input variables are retrieved.
Added option to update or overwrite existing file (this leads to a little issue with the reflection if cones are added and reflected to a file that already contains anything).

