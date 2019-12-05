#! Python3
#Pipline test 

import os

os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline' )
pipelinePath = r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline' 

#Mappen met mappen er in. 
#In folder zit: _Pre, _ref, _source, _element, _workfiles, _renders & _pipeline. 
#De variables daar onder zijn de mappen in de variable er boven. 
folders = ['01_pre', '02_ref', '03_source', '04_elements', '05_workfiles', '06_renders', '_pipeline']
_pre = ['01_script', '02_breakdown', '03_concept', '04_visie', '05_previs', '06_techvis', '07_planning']
_script = ['latest', 'archive']

_ref = ['01_setdata', '02_schematics', '03_images', '04_video', '05_anim', '06_picturelock']
_setdata = ['photogrammetry', 'reports', 'setimages', 'hdri', 'lens']

_source = ['source']

_elements = ['01_assets', '02_caches', '03_hdri', '04_mattepainting', '05_stock']
_caches = ['anim', 'sim']
_stock = ['images', 'sequences', 'models']

_workfiles = ['assets', 'shot']

_renders = ['prerender', 'cg', 'delivery']

_pipeline = ['templates']
templates = ['Nuke', 'Houdini', 'Maya']

print(os.chdir(pipelinePath + '01_pre\\'))

# 1e Mappen worden aangemaakt. 
try:
	for map in folders:
		if map not in os.listdir():
			os.makedirs(map)
	print(os.listdir())
except:
	pass

# 2e Mappen worden aangemaakt in 01_pre. 	
if '01_pre' in os.listdir():
	print('True 01_pre')
	os.chdir(pipelinePath + '01_pre\\')
	
	try: 
		for i in _pre:
			while i not in os.listdir():
				os.makedirs(i)
				print(i)
	except:
		pass
	try: # 3e mappen worden gecontrolleerd en aangemaakt in 01_script gezet. 
		if '01_script' in os.listdir():
			print('True 01_script')
			os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline\01_pre\01_script')
			while i not in os.listdir():
				for i in _script: # 3e mappen in 01_script. 
					os.makedirs(i)
			os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline')
			print(os.chdir())
	except:
		os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline')
		pass

#1e map 02_ref controlleren. Zit die er in dan wordt os.chdir veranderd naar 02_ref map. We gaan dus een map dieper.
if '02_ref' in os.listdir():
	print('True 02_ref')
	os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline\02_ref')
	try:
		while i not in os.listdir():	
			for i in _ref:
				os.makedirs(i)
				print(i)
	except:
		pass
	try:	#3e mappen worden gecontrolleerd en gemaakt in 01_setdata. 
		if '01_setdata' in os.listdir():
			print('True 01_setdata')
			os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline\02_ref\01_setdata')
			try: 
				for i in _setdata: # Er wordt niet gecontrolleerd of alle mappen er in zitten. Dus als er 1 onbreekt dan loopt die er niet doorheen. :
					while i not in os.listdir():
						print(i)
						os.makedirs(i)
				os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline')
				
			except:
				pass		
	except:
		os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline')
		pass

# 2e Mappen worden aangemaakt in 04_elements. 	
try:	
	if '04_elements' in os.listdir():
		print('True 04_elements')
		os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline\04_elements')
		for i in _elements:
			while i not in os.listdir():
				os.makedirs(i)
				os.listdir()
except:
	pass

# 2e Mappen worden aangemaakt in 02_caches. 	
try:	
	if '02_caches' in os.listdir():
		print('True 02_caches')
		os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline\04_elements\02_caches')
		for i in _caches:
			while i not in os.listdir():
				print(i + ' _caches')
				os.makedirs(i)
				print(os.getcwd())
		os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline\04_elements\05_stock')
		for i in _stock:
			while i not in os.listdir():
				os.makedirs(i)
				print(i + '_stock')
		os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline')
except:
	os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline')
	pass

# 2e Mappen worden aangemaakt in 05_workfiles. 	
try:	
	if '05_workfiles' in os.listdir():
		print('True 05_workfiles')
		os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline\05_workfiles')
		for i in _workfiles:
			while i not in os.listdir():
				os.makedirs(i)
		os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline')
except:
	pass

# 2e Mappen worden aangemaakt in 06_renders. 	
try:	
	if '06_renders' in os.listdir():
		print('True 06_renders')
		os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline\06_renders')
		for i in _renders:
			while i not in os.listdir():
				os.makedirs(i)
		os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline')
except:
	pass

# 2e Mappen worden aangemaakt in _pipeline.  	
try:	
	if '_pipeline' in os.listdir(): #Als dit bestaat dan change directory.
		print('True _pipeline')
		os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline\_pipeline')
		for i in _pipeline: 
			while i not in os.listdir(): #van de i Mappen in Pipeline wordt gecontrolleerd of het bestaat en zo niet dan worden ze aangemaakt.  
				os.makedirs(i)
				print(i)
except:
	pass
# 3e mappen worden gecontrolleerd en in templates gezet. 
try:		
	if 'templates' in os.listdir():
		print('True template')
		os.chdir(r'C:\Users\Golan.vanderBend\Documents\Golan\Python\Pipeline\_pipeline\templates')
		for i in templates:
			while i not in os.listdir():
				os.makedirs(i)
except:
	pass
