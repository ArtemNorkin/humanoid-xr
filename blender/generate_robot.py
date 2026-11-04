# Blender 5.1: run from Scripting workspace. Generates editable robot and exports GLB.
import bpy, math
from pathlib import Path
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
def mat(name,color,metal=0.0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bs=m.node_tree.nodes.get("Principled BSDF");bs.inputs["Base Color"].default_value=(*color,1);bs.inputs["Metallic"].default_value=metal;bs.inputs["Roughness"].default_value=.42
 return m
steel=mat("Steel",(.36,.45,.56),.7);dark=mat("Dark",(.12,.17,.25),.4);glow=mat("Cyan",(.04,.75,.9),.1)
def cube(name,loc,scale,material):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);return o
def orb(name,loc,r,material,segments=48,rings=24):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,radius=r,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(material);return o
def tube(name,loc,r,h,material):
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=h,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(material);return o
cube("Torso",(0,0,2.12),(1.25,.66,1.55),steel);cube("Chest panel",(0,-.37,2.27),(.87,.07,.62),dark)
for s in (-1,1):
 orb("Shoulder",(s*.82,0,2.63),.36,steel);tube("Upper arm",(s*.88,0,2.06),.22,.83,steel);orb("Elbow",(s*.88,0,1.62),.24,dark);tube("Forearm",(s*.88,0,1.19),.24,.72,steel);cube("Hand",(s*.88,0,.69),(.37,.4,.31),dark);cube("Leg",(s*.33,0,.7),(.42,.53,1.02),steel);cube("Foot",(s*.33,-.14,.12),(.55,.85,.23),dark);orb("Eye",(s*.27,-.36,3.31),.14,glow);cube("Knee",(s*.33,-.04,.55),(.44,.58,.18),dark)
cube("Neck",(0,0,3.03),(.32,.32,.24),dark);cube("Head",(0,0,3.43),(.99,.72,.79),steel);cube("Face",(0,-.39,3.37),(.76,.06,.34),dark);orb("Core",(0,-.43,2.24),.21,glow)
for i in range(4):cube("Vent",(-.28+i*.18,-.44,1.96),(.12,.08,.05),dark)
tube("Antenna",(.28,0,4),.055,.32,dark);orb("Antenna tip",(.28,0,4.18),.10,glow)
for o in bpy.context.scene.objects:
 if o.type=='MESH':
  bpy.context.view_layer.objects.active=o
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True)
  bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(island_margin=.02);bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')
path=Path(bpy.path.abspath('//'))/'robot_from_blender.glb'
bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=False)
print('Saved:',path)
