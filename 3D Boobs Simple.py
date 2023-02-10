import bpy
import bmesh
import math
import mathutils

verts = []
edges = []
faces = []

try:
    object_to_delete = bpy.data.objects['boobs']
    bpy.data.objects.remove(object_to_delete, do_unlink=True)
except:
    pass

def add_vertex(vertex):
    verts.append(vertex)
    return len(verts) - 1

# breast parameters
breast_x_length = 2
breast_x_radius = breast_x_length/2
breast_upper_z_length = 1.5
breast_lower_z_length = 1
chest_angle = 30
breast_spread = 1.2

# starter vertices
breast_lower = add_vertex((0,0,-breast_lower_z_length))
breast_lower_tension = add_vertex((breast_x_radius,0,-breast_lower_z_length))
breast_side = add_vertex((breast_x_radius,0,0))
breast_upper_tension = add_vertex((breast_x_radius,0,breast_upper_z_length))
breast_upper = add_vertex((0,0,breast_upper_z_length))

edges = [(0,1),(1,2),(2,3),(3,4)]

# create mesh and object
mesh = bpy.data.meshes.new("boobs")
object = bpy.data.objects.new("boobs",mesh)

bpy.context.collection.objects.link(object)

# create mesh from python data
mesh.from_pydata(verts,edges,faces)

bm = bmesh.new()
bm.from_mesh(mesh)
bm.verts.ensure_lookup_table()

# bevel to form curves of breast
bmesh.ops.bevel(bm, geom=[bm.verts[breast_upper_tension], bm.verts[breast_lower_tension]], offset=breast_upper_z_length, segments=36, profile=0.5, affect='VERTICES')

# spin to wrap around curviture of chest
bmesh.ops.spin(bm, geom=bm.verts[:] + bm.edges[:], angle=math.radians(-180 - chest_angle), steps=84, axis=(0, 0, 1), cent=(0, 0, 0))

# move to right side of chest
bmesh.ops.translate(bm, verts=bm.verts[:], vec=(-breast_spread,0,0))

# duplicate bmesh for right breast
ret = bmesh.ops.duplicate(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:])
geom_dupe = ret["geom"]
verts_dupe = [ele for ele in geom_dupe if isinstance(ele, bmesh.types.BMVert)]

# move to left side of chest
bmesh.ops.translate(bm, verts=verts_dupe, vec=(breast_spread*2,0,0))

# rotate to match left chest curve
bmesh.ops.rotate(bm, verts=verts_dupe, cent=(breast_spread, 0.0, 0.0), matrix=mathutils.Matrix.Rotation(math.radians(chest_angle), 3, 'Z'))

bm.to_mesh(mesh)
bm.free()