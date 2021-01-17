# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.



## init.py
## loaded by nuke before menu.py
if nuke.NUKE_VERSION_MAJOR ==10:
	nuke.pluginAddPath('./OpticalFlares_10')
if nuke.NUKE_VERSION_MAJOR ==11:
	if nuke.NUKE_VERSION_MINOR ==2:
		nuke.pluginAddPath('./OpticalFlares_11.2')
	if nuke.NUKE_VERSION_MINOR ==3:
		nuke.pluginAddPath('./OpticalFlares_11.3')
if nuke.NUKE_VERSION_MAJOR ==12:
	nuke.pluginAddPath('./OpticalFlares_12')

'''
if nuke.NUKE_VERSION_MAJOR ==11:
	import global_clipboard_11 as gcb
elif nuke.NUKE_VERSION_MAJOR <11:
	import global_clipboard as gcb
else:
	pass
'''

nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./gizmos/Luma Gizmos')

nuke.pluginAddPath('./gizmos/LensDistortions/ArriZeissMasterPrime/Coated')
nuke.pluginAddPath('./gizmos/LensDistortions/ArriZeissMasterPrime/Uncoated')
nuke.pluginAddPath('./gizmos/LensDistortions/Fujinon18-400')
nuke.pluginAddPath('./gizmos/LensDistortions/MasterPrime')
nuke.pluginAddPath('./gizmos/LensDistortions/Vista-M')

nuke.pluginAddPath('X:/apps/Scripts/NUKE/icons/')

nuke.pluginAddPath('./python')
nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./python/pixelfudger')
nuke.pluginAddPath('./python/ftrack')
nuke.pluginAddPath('./python/lux_utils')
#nuke.pluginAddPath('./python/ftrack_api')
#nuke.pluginAddPath('./plugins/geometry')
#nuke.pluginAddPath('./plugins/bokeh')
#nuke.pluginAddPath('./plugins/J_Ops')

v = str(nuke.NUKE_VERSION_MAJOR) + '.' + str(nuke.NUKE_VERSION_MINOR)
nuke.pluginAddPath('./plugins/LD_3DE/Nuke{}'.format(v))


#def filenameFix(filename):

# if platform.system() in ("Windows", "Microsoft"):

#	 return filename.replace( "/mnt/Projects/", "Q:\\" )

# else:

# 	return filename.replace( "Q:\\", "/mnt/Projects/" )

# return filename

#auto create folders on write nodes (python: before render) &&& duplicate the nk script in the render directories. (python render progress)
#nuke.knobDefault('Write.beforeRender', 'def createPath():\n    file = nuke.filename(nuke.thisNode())\n    dir = os.path.dirname(file)\n    osdir = nuke.callbacks.filenameFilter(dir)\n    try:\n        os.makedirs (osdir)\n    except OSError:\n        pass\ncreatePath()')
#nuke.knobDefault('Write.afterRender', 'def saveRenderScript():\n    assetFileName = nuke.filename(nuke.thisNode()).split(".")[0]+".nk"\n    print "Saving a copy of the render script >> ", assetFileName\n    nuke.scriptSave(assetFileName)\nsaveRenderScript()')
#nuke.knobDefault('WriteGeo.beforeRender', 'def createPath():\n    file = nuke.filename(nuke.thisNode())\n    dir = os.path.dirname(file)\n    osdir = nuke.callbacks.filenameFilter(dir)\n    try:\n        os.makedirs (osdir)\n    except OSError:\n        pass\ncreatePath()')
#nuke.knobDefault('WriteGeo.afterRender', 'def saveRenderScript():\n    assetFileName = nuke.filename(nuke.thisNode()).split(".")[0]+".nk"\n    print "Saving a copy of the render script >> ", assetFileName\n    nuke.scriptSave(assetFileName)\nsaveRenderScript()')

nuke.knobDefault('Write.beforeRender', 'def createPath():\n    file = nuke.filename(nuke.thisNode())\n    dir = os.path.dirname(file)\n    osdir = nuke.callbacks.filenameFilter(dir)\n    try:\n        os.makedirs (osdir)\n    except OSError:\n        pass\ncreatePath()\ndef saveRenderScript():\n    try:\n        assetFileName = nuke.filename(nuke.thisNode()).split(".")[0]+".nk"\n        print "Saving a copy of the render script >> ", assetFileName\n        nuke.scriptSave(assetFileName)\n    except:\n        pass\nsaveRenderScript()')
nuke.knobDefault('WriteGeo.beforeRender', 'def createPath():\n    file = nuke.filename(nuke.thisNode())\n    dir = os.path.dirname(file)\n    osdir = nuke.callbacks.filenameFilter(dir)\n    try:\n        os.makedirs (osdir)\n    except OSError:\n        pass\ncreatePath()\ndef saveRenderScript():\n    try:\n        assetFileName = nuke.filename(nuke.thisNode()).split(".")[0]+".nk"\n        print "Saving a copy of the render script >> ", assetFileName\n        nuke.scriptSave(assetFileName)\n    except:\n        pass\nsaveRenderScript()')
nuke.knobDefault('SmartVector.beforeRender', 'def createPath():\n    file = nuke.filename(nuke.thisNode())\n    dir = os.path.dirname(file)\n    osdir = nuke.callbacks.filenameFilter(dir)\n    try:\n        os.makedirs (osdir)\n    except OSError:\n        pass\ncreatePath()\ndef saveRenderScript():\n    try:\n        assetFileName = nuke.filename(nuke.thisNode()).split(".")[0]+".nk"\n        print "Saving a copy of the render script >> ", assetFileName\n        nuke.scriptSave(assetFileName)\n    except:\n        pass\nsaveRenderScript()')

nuke.knobDefault('ReagGeo.read_on_each_frame', 'True')
nuke.knobDefault('Tracker4.keyframe_display', '3')
nuke.knobDefault('Tracker4.max_iter', '1000')
nuke.knobDefault('Tracker4.adjust_for_luminance_changes', '3')
nuke.knobDefault('Invert.channels', 'alpha')
nuke.knobDefault('Mirror2.flop', 'True')
nuke.knobDefault('AddChannels.channels', 'alpha')
nuke.knobDefault('STMap.uv', 'rgba')

# ASSIGNING KNOB DEFAULTS
nuke.knobDefault("Bezier.output","alpha")
nuke.knobDefault("Blur.label","[value size]")
nuke.knobDefault("Bezier.linear","on")
nuke.knobDefault("Root.format","HD")
nuke.knobDefault("Project3D.crop", "0")
nuke.knobDefault("ScanlineRender.motion_vectors_type", "off")
nuke.knobDefault("ScanlineRender.MB_channel", "none")
nuke.knobDefault("TimeOffset.label", "[value time_offset]")
nuke.knobDefault("LensDistortion.gridType", "Thin Line")

# LUX KNOB DEFAULTS
nuke.knobDefault("ZBlur.shape","1")
nuke.knobDefault("TimeBlur.shutteroffset","centred")
nuke.knobDefault("MotionBlur2D.shutteroffset","centred")
nuke.knobDefault("MotionBlur3D.shutteroffset","centred")
nuke.knobDefault("Grade.black_clamp","0")
nuke.knobDefault("Write.jpeg._jpeg_quality", "1")
nuke.knobDefault("Write.jpeg._jpeg_sub_sampling", "4:2:2")
nuke.knobDefault('Clamp.maximum_enable', 'False')

# NO CLIPS
nuke.knobDefault("Roto.cliptype","no clip")
nuke.knobDefault("RotoPaint.cliptype","no clip")
nuke.knobDefault("Grid.cliptype","no clip")
nuke.knobDefault("Noise.cliptype","no clip")
nuke.knobDefault("Radial.cliptype","no clip")
nuke.knobDefault("Rectangle.cliptype","no clip")
nuke.knobDefault("Ramp.cliptype","no clip")
nuke.knobDefault("Text2.cliptype","no clip")


# LUX FORMATS
nuke.addFormat("4096 4096 square_4K")
nuke.addFormat("8192 8192 square_8K")
nuke.addFormat("960 540 HALF_HD")
nuke.addFormat("720 480 0 0 720 480 0.9 FCP")
nuke.addFormat("2048 1165 BBC")
nuke.addFormat("1024 582 BBC_HALF")
nuke.addFormat("2048 1080 DCI_2K")
nuke.addFormat("2048 1152 DCI_2K 16:9")
nuke.addFormat("2288 858 ANA_2K")
nuke.addFormat("3200 1800 QHD+ 16:9")
nuke.addFormat("4096 3416 2 4K_ANA")
nuke.addFormat("4096 3416 1 4K_ANA_S")
nuke.addFormat("2880 1620 1 3K")

def filenameFix(filename):

	win = 'Q:/'
	nix = '/mnt/Projects/'
	if nuke.env['LINUX']:
		if filename.startswith(win):
			filename =filename.replace(win,nix)
	return filename

	if nuke.env['WIN32']: 
		if filename.startswith(nix): 
			filename = filename.replace(nix, win) 
	return filename 


import cryptomatte_utilities
cryptomatte_utilities.setup_cryptomatte()