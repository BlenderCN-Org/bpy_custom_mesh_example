bl_info = {
    "name": "Custom Mesh",
    "author": "jnphgs",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > Custom Mesh",
    "description": "Adds a new Custom Mesh",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "category": "Add Mesh",
}


import bpy
import math
from bpy.types import Operator
from bpy.props import IntProperty, FloatProperty, FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector


def add_object(self, context):
    verts = []
    edges = []
    faces = []
    res = self.Resolution
    height = 0.5*self.Height
    radius = self.Radius

    for i in range(res):
        theta = 2.0*math.pi*i/res       
        verts.append(Vector((radius*math.cos(theta), radius*math.sin(theta), height)))
        
    for i in range(res):
        theta = 2.0*math.pi*i/res
        verts.append(Vector((radius*math.cos(theta), radius*math.sin(theta), -height)))
    
    for i in range(res):
        faces.append([i, (i+1)%res, res+(i+1)%res, res+i ])
    
    
    mesh = bpy.data.meshes.new(name="New Object Mesh")
    mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    object_data_add(context, mesh, operator=self)


class OBJECT_OT_Add_Custom_Mesh(Operator, AddObjectHelper):
    bl_idname = "mesh.add_custom_mesh"
    bl_label = "Add Custom Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    Resolution: IntProperty(
        name="Resolution",
        description="division count.",
        default=6,
        min=3,
        max=256
    )

    Height: FloatProperty(
        name="Height",
        description="height of poll.",
        default=1.0,
        min=0.0001
    )
    Radius: FloatProperty(
        name="Height",
        description="height of poll.",
        default=1.0,
        min=0.0001
    )

    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}

def menu_fn(self, context):
    self.layout.operator(
        OBJECT_OT_Add_Custom_Mesh.bl_idname,
        text="Add Custom Mesh",
        icon='PLUGIN')

def register():
    bpy.utils.register_class(OBJECT_OT_Add_Custom_Mesh)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_fn)
    print("register: custom mesh addon")


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_Add_Custom_Mesh)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_fn)
    print("unregister: custom mesh addon")


if __name__ == "__main__":
    register()
