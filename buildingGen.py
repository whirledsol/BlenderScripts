import bpy
from bpy import *
'''
Building Generator
	Builds parts of buildings to be stitched together in Blender
	Written by: Will Rhodes
	5/25/2014
'''
#global ############################################
mainLayer = 0 #<------- can edit
mainLayerArray = [False]*20
mainLayerArray[mainLayer] = True

constructionLayer = 1   #<------- can edit
constructionLayerArray = [False]*20 
constructionLayerArray[constructionLayer] = True #work on a specific layer of the scene

wallThickness = 0.1

####################################################
def main():
	clearAll()
	bpy.ops.object.camera_add() #must add a camera
	create_Corridor([5,20,5],closed=True, windows=[0,1,0,0,0,0])
####################################################
def create_Corridor(dim=[1,1,10], windows=None, closed = False):
	''' 
	creates a straight corridor or room
	as usual, the dim are in x,y,z and correspond to interior dimensions
	closed determines if the corridor should be closed off on both openings
	windows should be a sized 4 or 6 array displaying the number of windows on each panel (l,r,u,d,f,b)
	'''
	depth = dim[0]
	length = dim[1]
	height = dim[2]
	if len(windows) == 4:
		windows = windows + [0,0]
	#create base
	add_cube([depth,length,wallThickness],[0,0,-wallThickness*0.5])
	add_window(windows[3])
	#create ceiling
	add_cube([depth,length,wallThickness],[0,0,height+wallThickness*0.5])
	add_window(windows[2])
	#create left side
	add_cube([wallThickness,length,height+2*wallThickness],[-(depth+wallThickness)*0.5,0,height*0.5])
	add_window(windows[0])
	#create right side
	add_cube([wallThickness,length,height+2*wallThickness],[(depth+wallThickness)*0.5,0,height*0.5])
	add_window(windows[1])
	if closed:
		#add front
		add_cube([depth+2*wallThickness,wallThickness,height+2*wallThickness],[0,length*0.5+wallThickness*0.5,height*0.5])
		add_window(windows[4])
		#add back
		add_cube([depth+2*wallThickness,wallThickness,height+2*wallThickness],[0,-(length*0.5+wallThickness*0.5),height*0.5])
		add_window(windows[5])
	finalize()

####################################################
def clearAll():
	'''
	clears all items in the scene
	'''
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.object.delete(use_global=False)
####################################################	
def add_cube(scale=[1,1,1],location=[0,0,0]):
	'''
	creates a rectangular mesh with scale at location
	'''
	bpy.ops.mesh.primitive_cube_add(location=tuple([i*2 for i in location]),layers=constructionLayerArray)
	bpy.ops.transform.resize(value=scale,proportional='ENABLED')
####################################################	
def finalize():
	'''
	move objects, temporarily constructed in construction layer, to main layer
	'''
	bpy.ops.object.select_by_layer(False,layers=constructionLayer)
	bpy.ops.object.join()
	bpy.ops.object.select_by_layer(False,layers=constructionLayer)
	bpy.ops.object.move_to_layer(mainLayer)
####################################################	
def moveToObject(obj):
	'''
	moves camera to object but centered at the origin
	'''	
	for area in bpy.context.screen.areas:
		if area.type == 'VIEW_3D':
			override = {'area': area, 'region': area.regions[-1]}
			bpy.ops.view3d.viewnumpad(override, type='FRONT', align_active=True)
			wait = raw_input()
	
####################################################  
def add_window(numberOfWindows):
	'''
	subtracts a window from the selected object
	'''
	
	for each in range(numberOfWindows):	
		obj_A = bpy.context.scene.objects.active
		moveToObject(obj_A)
		"""
		windowScale = None #TODO: fix
		obj_B = add_cube(scale=windowScale,location=windowItem.location) 

		boo = obj_A.modifiers.new('Booh', 'BOOLEAN')
		boo.object = obj_B
		boo.operation = 'DIFFERENCE'
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Booh")
		bpy.context.scene.objects.unlink(obj_B) #remove temp item
		#go back to active item
		bpy.context.scene.objects.active = objA
		"""
	return
####################################################    
class window():
	'''
	a struct for encapsulating a window or gutter hole in a wall
	location is the center point where the hole is created
	it is measured from the origin and for the dimensions, has to be where a wall is
	'''
	def __init__(self, location=[0,0], dim=[1,1], parent = "l"):
		self.location = location
		self.dim = dim
		self.parent = parent


if __name__ == "__main__": main()


