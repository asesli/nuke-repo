# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
# LUX Visual Effects Inc.

import nuke

#LUX LOGGING
import nuke
import nukelogging
#nuke.addOnUserCreate( lambda: nukelogging.log_node( nuke.thisNode().Class() ) )
nuke.addOnCreate( lambda: nukelogging.log_node( nuke.thisNode().Class() ) )
nuke.addOnScriptLoad( lambda: nukelogging.log_script() )
nuke.addOnScriptSave( lambda: nukelogging.log_script() )


if nuke.NUKE_VERSION_MAJOR ==11:
	import global_clipboard_11 as gcb
elif nuke.NUKE_VERSION_MAJOR <11:
	import global_clipboard as gcb
else:
	pass

import lux_write_knobchanged

#import RandomTiles #used?

import AnimationMaker
import DeadlineNukeClient
import animatedSnap3D
import versionUp
import cam_presets
import importAssets
import nodeOps
cam_presets.nodePresetCamera()

import dropData
nukescripts.dropData = dropData.dropData

import cryptomatte_utilities
cryptomatte_utilities.setup_cryptomatte_ui()

import browseDir
import ftrack_nuke_utils

'''
#LUX Asset Manager
from nukescripts import panels
pane = nuke.getPaneFor('Properties.1')
panels.registerWidgetAsPanel('lux_asset_manager.AssetManager', 'LUX Asset Manager', 'uk.co.thefoundry.AssetManager', True).addToPane(pane)
'''


toolbar = nuke.menu('Nodes')

def myViewer_Input():
	setVal = nuke.createNode('VIEWER_INPUT').name()
	[i.knob('input_process_node').setValue(setVal) for i in nuke.allNodes() if i.Class() == 'Viewer']


nuke.menu('Nodes').addCommand("Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )")

#### add menu item to existing Nuke menu
nodeMenu = nuke.menu('Nuke').findItem('Edit/Node')
nodeMenu.addCommand('Toggle Viewer Pipes', 'nodeOps.toggleViewerPipes()', 'alt+t')


# Norman Toolset
n_menu = toolbar.addMenu('Norman Tools', icon='ntools_icon.png')
n_menu.addCommand("N_Distant", "nuke.createNode('N_Distant.nk')")
n_menu.addCommand("N_Sticker", "nuke.createNode('N_Sticker.nk')")
n_menu.addCommand("N_AmbientLight", "nuke.createNode('N_AmbientLight.nk')")
n_menu.addCommand("N_3DMaskRamp", "nuke.createNode('N_3DMaskRamp.nk')")
n_menu.addCommand("N_3DMaskBubble", "nuke.createNode('N_3DMaskBubble.nk')")
n_menu.addCommand("N_3DMaskCube", "nuke.createNode('N_3DMaskCube.nk')")
n_menu.addCommand("N_Noise3D", "nuke.createNode('N_Noise3D.nk')")
n_menu.addCommand("N_PointLight", "nuke.createNode('N_PointLight.nk')")

#SPRUT Fluid Simulation
sprutMenu = toolbar.addMenu('SPRUT', icon='sprut.png')
sprutMenu.addCommand('SprutEmitter', "nuke.createNode('SprutEmitter.gizmo')")
sprutMenu.addCommand('SprutSolver', "nuke.createNode('SprutSolver.gizmo')")
sprutMenu.addCommand('SprutInspect', "nuke.createNode('SprutInspect.gizmo')")

#RED
#LUX Gizmos
gizmoMenu = toolbar.addMenu('LUX Gizmos', icon='X:/apps/Scripts/NUKE/icons/lux_red_32.png')

#Matte/Image Operators
gizmoMenu.addMenu("Mattes", icon='lux_mattes.png')
gizmoMenu.addCommand('Mattes/edge_004', "nuke.createNode('edge004')")
gizmoMenu.addCommand('Mattes/edge_plus001', "nuke.createNode('edgeplus001')")
gizmoMenu.addCommand('Mattes/fractal_blur_tex', "nuke.createNode('lx_fractal_blurtex002')")
gizmoMenu.addCommand('Mattes/Matrix_preloaded', "nuke.createNode('matrix_preloaded001')")
gizmoMenu.addCommand('Mattes/MultiMatteSimple', "nuke.createNode('multimattesimple.gizmo')")
gizmoMenu.addCommand('Mattes/L_Fuze', "nuke.createNode('l_fuze.gizmo')")
gizmoMenu.addCommand('Mattes/ColourDilate', "nuke.createNode('ColourDilate.nk')")

#Filter (Erode/Blur/Sharpen/Glow/Distortion) Operators
gizmoMenu.addMenu("Filter", icon='lux_filter.png')
gizmoMenu.addCommand("Filter/Erode (fine)", "nuke.createNode('erodeFine.gizmo')")
gizmoMenu.addCommand("Filter/ErodeDir", "nuke.createNode('erodeDir.gizmo')")
gizmoMenu.addCommand("Filter/ErodeX", "nuke.createNode('erodeX.gizmo')")
gizmoMenu.addCommand("Filter/ErodeZ", "nuke.createNode('erodeZ.gizmo')")
#gizmoMenu.addCommand("Filter/dirErode", "nuke.createNode('dirErode.gizmo')")
gizmoMenu.addCommand('Filter/L_FillBlur', "nuke.createNode('L_FillBlur.gizmo')")
gizmoMenu.addCommand('Filter/fillBlur', "nuke.createNode('lx_fillBlur.gizmo')")
gizmoMenu.addCommand("Filter/BlurZ", "nuke.createNode('blurZ.gizmo')")
gizmoMenu.addCommand("Filter/dirBlur2", "nuke.createNode('dirBlur2.gizmo')")
gizmoMenu.addCommand('Filter/BokehBlur', "nuke.createNode('lx_BokehBlur')")
gizmoMenu.addCommand("Filter/ConvolveDefocus", "nuke.createNode('convolveDefocus.gizmo')")
gizmoMenu.addCommand('Filter/focusbreathing', "nuke.createNode('focusbreathing001')")
gizmoMenu.addCommand('Filter/heat', "nuke.createNode('heat_002.gizmo')")
gizmoMenu.addCommand('Filter/FengGlow', 'nuke.nodes.FengGlow()')
gizmoMenu.addCommand("Filter/lx_sharpen", "nuke.createNode('lx_sharpen.gizmo')")
gizmoMenu.addCommand('Filter/cab', "nuke.createNode('lx_cab_002')")#Chromatic abberation
gizmoMenu.addCommand('Filter/ExponentialGlow', "nuke.createNode('exponentialGlow.nk')")
gizmoMenu.addCommand('Filter/N_Soften', "nuke.createNode('N_Soften.gizmo')")
gizmoMenu.addCommand('Filter/N_Convolve', "nuke.createNode('N_Convolve.gizmo')")

#Transform Operators
gizmoMenu.addMenu("Transform", icon='lux_transform.png')
gizmoMenu.addCommand('Transform/iDistort_lux', "nuke.createNode('lx_iDistort.gizmo')")
gizmoMenu.addCommand("Transform/Glass", "nuke.createNode('glass.nk')")
gizmoMenu.addCommand("Transform/Glass2", "nuke.createNode('Glass2.gizmo')")
gizmoMenu.addCommand("Transform/iTransform", "nuke.createNode('ITransform.gizmo')")
gizmoMenu.addCommand("Transform/Wave Distortion", "nuke.createNode('WaveDistortion.gizmo')")
gizmoMenu.addCommand("Transform/Ripple Distortion", "nuke.createNode('RippleDistortion.gizmo')")
gizmoMenu.addCommand("Transform/Transform Dissolve", "nuke.createNode('TransformDissolve.gizmo')")

#Overlay Operators
gizmoMenu.addMenu("Overlays", icon='lux_overlays.png')
gizmoMenu.addCommand('Overlays/filmlut', "nuke.createNode('filmlut003')")#Film Lut
gizmoMenu.addCommand('Overlays/flicker', "nuke.createNode('flicker003')")#Flicker
gizmoMenu.addCommand('Overlays/lensFilters', "nuke.createNode('lensFilters_003')")
gizmoMenu.addCommand('Overlays/BadVideo', "nuke.createNode('lx_BadVideo_001.gizmo')")
gizmoMenu.addCommand('Overlays/AdvancedGrain', "nuke.createNode('lx_AdvancedGrain')")
gizmoMenu.addCommand('Overlays/Vignette', "nuke.createNode('vignette.gizmo')")
gizmoMenu.addCommand('Overlays/CustomTimecode', "nuke.createNode('custom_timecode.gizmo')")
gizmoMenu.addCommand('Overlays/TimeCode', "nuke.createNode('TimeCode.nk')")
gizmoMenu.addCommand('Overlays/CS_Label', "nuke.createNode('cs_label.gizmo')")
gizmoMenu.addCommand('Overlays/GrainCheck', "nuke.createNode('graincheck.gizmo')")
gizmoMenu.addCommand('Overlays/TimerClock', "nuke.createNode('TimerClock.gizmo')")

#Image/Asset Generation
gizmoMenu.addMenu("Image", icon='lux_image.png')
gizmoMenu.addCommand('Image/muzzle', "nuke.createNode('muzzle_003.gizmo')")
gizmoMenu.addCommand('Image/fire', "nuke.createNode('lx_fire_001.gizmo')")
gizmoMenu.addCommand('Image/Flaire', 'nuke.nodes.FlareFactory_Plus()')
gizmoMenu.addCommand('Image/NormalMap', "nuke.createNode('normalmap.gizmo')")
gizmoMenu.addCommand('Image/FogBox', "nuke.createNode('FogBox.gizmo')")
gizmoMenu.addCommand('Image/ImagePlane', "nuke.createNode('ImagePlane.gizmo')")
gizmoMenu.addCommand("Image/CurveGenerator", "nuke.createNode('curveGenerator.gizmo')")
gizmoMenu.addCommand("Image/looper", "nuke.createNode('looper.gizmo')")
gizmoMenu.addCommand('Image/Seamless', "nuke.createNode('seamless.gizmo')")
gizmoMenu.addCommand('Image/GltHeatHaze', 'nuke.createNode("GltHeatHaze")')
gizmoMenu.addCommand("Image/UV_Map", "nuke.createNode('uv.nk')")
gizmoMenu.addCommand('Image/X-Tesla', "nuke.createNode('X_Tesla.gizmo')")

#Utility Operators
gizmoMenu.addMenu("Utility", icon='lux_utils.png')
gizmoMenu.addCommand("Utility/MMin", "nuke.createNode('mmin.gizmo')")
gizmoMenu.addCommand("Utility/Breakdown", "nuke.createNode('breakdown.gizmo')")
gizmoMenu.addCommand("Utility/gui", "nuke.createNode('gui.gizmo')")
gizmoMenu.addCommand('Utility/NAN_Handler', "nuke.createNode('lx_NAN_001')")
gizmoMenu.addCommand('Utility/timecode_lux', "import importTimecode; importTimecode.importTimecode()")
gizmoMenu.addCommand("Utility/RenderIDRandomizer", "nuke.createNode('RenderIDRandomizer.gizmo')")
gizmoMenu.addCommand("Utility/idSelector", "nuke.createNode('idSelector.gizmo')")
gizmoMenu.addCommand("Utility/LuxLUT", "nuke.createNode('luxlut3.gizmo')")
gizmoMenu.addCommand('Utility/vray_BB', "nuke.createNode('vray_BB_008')")
gizmoMenu.addCommand('Utility/lifetime', "nuke.createNode('lifetime.gizmo')")
gizmoMenu.addCommand('Utility/QC Creator', "nuke.createNode('QCCreator.nk')")
gizmoMenu.addCommand('Utility/Retime Matcher', "import match_retime; match_retime.create_control_node()")

#Color Operators
gizmoMenu.addMenu("Color", icon='lux_color.png')
gizmoMenu.addCommand("Color/SoftClipExp", "nuke.createNode('SoftClipExp.gizmo')")
gizmoMenu.addCommand('Color/DespillMadness', "nuke.createNode('DespillMadness.nk')")
gizmoMenu.addCommand('Color/HighPass', "nuke.createNode('HighPass.gizmo')")
gizmoMenu.addCommand('Color/SL_Despill', "nuke.createNode('sl_despill.nk')")
gizmoMenu.addCommand("Color/BlackSoftClip", "nuke.createNode('blackSoftClip.nk')")
gizmoMenu.addCommand("Color/SuperWhiteRollOff", "nuke.createNode('superWhiteRollOff.nk')")
gizmoMenu.addCommand("Color/OmensLUT", "nuke.createNode('OmensLUT.nk')")

# The "Lens Tools" specific menu items
gizmoMenu.addMenu('Lens Tools', icon='lux_lens_tools.png')
gizmoMenu.addMenu('Lens Tools/Canon')
gizmoMenu.addCommand('Lens Tools/Canon/Canon1DMK4_10_20_001', "nuke.createNode('Canon1DMK4_10_20_001')")
gizmoMenu.addCommand('Lens Tools/Canon/Canon1DMK4_24_70_001', "nuke.createNode('Canon1DMK4_24_70_001')")
gizmoMenu.addCommand('Lens Tools/Canon/Canon1DMK4_70_200_001', "nuke.createNode('Canon1DMK4_70_200_001')")
gizmoMenu.addCommand('Lens Tools/Canon/Canon1DMK4_50_18_001', "nuke.createNode('Canon1DMK4_50_18_001')")
gizmoMenu.addMenu('Lens Tools/Nikon')
gizmoMenu.addCommand('Lens Tools/Nikon/NikonD700_Nikkor_1424_001', "nuke.createNode('NikonD700_Nikkor_1424_001')")
gizmoMenu.addCommand('Lens Tools/Nikon/NikonD700_Nikkor_2470_001', "nuke.createNode('NikonD700_Nikkor_2470_001')")
gizmoMenu.addCommand('Lens Tools/Nikon/NikonD700_Nikkor_70200_001', "nuke.createNode('NikonD700_Nikkor_70200_001')")
gizmoMenu.addCommand('Lens Tools/Nikon/NikonD7000_Nikkor_18200_001', "nuke.createNode('NikonD7000_Nikkor_18200_001')")
gizmoMenu.addCommand('Lens Tools/Nikon/NikonD700_Nikkor_85_14_001', "nuke.createNode('NikonD700_Nikkor_85_14_001')")
gizmoMenu.addCommand('Lens Tools/Nikon/NikonD700_Sigma_50_14_001', "nuke.createNode('NikonD700_Sigma_50_14_001')")
gizmoMenu.addCommand('Lens Tools/Arri Lens Distortion', "nuke.createNode('ArriLensDistortion.gizmo')")
gizmoMenu.addMenu('Lens Tools/Arri Zeiss')
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_16mm_Coated', "nuke.createNode('ArriMasterPrime_16mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_18mm_Coated', "nuke.createNode('ArriMasterPrime_18mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_21mm_Coated', "nuke.createNode('ArriMasterPrime_21mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_25mm_Coated', "nuke.createNode('ArriMasterPrime_25mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_27mm_Coated', "nuke.createNode('ArriMasterPrime_27mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_32mm_Coated', "nuke.createNode('ArriMasterPrime_32mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_35mm_Coated', "nuke.createNode('ArriMasterPrime_35mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_40mm_Coated', "nuke.createNode('ArriMasterPrime_40mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_50mm_Coated', "nuke.createNode('ArriMasterPrime_50mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_65mm_Coated', "nuke.createNode('ArriMasterPrime_65mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_75mm_Coated', "nuke.createNode('ArriMasterPrime_75mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_100mm_Coated', "nuke.createNode('ArriMasterPrime_100mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_135mm_Coated', "nuke.createNode('ArriMasterPrime_135mm_Coated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Coated/MasterPrime_150mm_Coated', "nuke.createNode('ArriMasterPrime_150mm_Coated.nk')")

gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_12mm_Uncoated', "nuke.createNode('ArriMasterPrime_12mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_14mm_Uncoated', "nuke.createNode('ArriMasterPrime_14mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_16mm_Uncoated', "nuke.createNode('ArriMasterPrime_16mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_18mm_Uncoated', "nuke.createNode('ArriMasterPrime_18mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_21mm_Uncoated', "nuke.createNode('ArriMasterPrime_21mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_25mm_Uncoated', "nuke.createNode('ArriMasterPrime_25mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_27mm_Uncoated', "nuke.createNode('ArriMasterPrime_27mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_32mm_Uncoated', "nuke.createNode('ArriMasterPrime_32mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_35mm_Uncoated', "nuke.createNode('ArriMasterPrime_35mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_40mm_Uncoated', "nuke.createNode('ArriMasterPrime_40mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_50mm_Uncoated', "nuke.createNode('ArriMasterPrime_50mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_65mm_Uncoated', "nuke.createNode('ArriMasterPrime_65mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_75mm_Uncoated', "nuke.createNode('ArriMasterPrime_75mm_Uncoated.nk')")
gizmoMenu.addCommand('Lens Tools/Arri Zeiss Master Prime/Uncoated/MasterPrime_100mm_Uncoated', "nuke.createNode('ArriMasterPrime_100mm_Uncoated.nk')")

gizmoMenu.addMenu('Lens Tools/MASTERPRIME')
gizmoMenu.addCommand('Lens Tools/MASTERPRIME/MASTERPRIME-14MM', "nuke.createNode('MASTERPRIME-14MM.nk')")
gizmoMenu.addCommand('Lens Tools/MASTERPRIME/MASTERPRIME-18MM', "nuke.createNode('MASTERPRIME-18MM.nk')")
gizmoMenu.addCommand('Lens Tools/MASTERPRIME/MASTERPRIME-21MM', "nuke.createNode('MASTERPRIME-21MM.nk')")
gizmoMenu.addCommand('Lens Tools/MASTERPRIME/MASTERPRIME-27MM', "nuke.createNode('MASTERPRIME-27MM.nk')")
gizmoMenu.addCommand('Lens Tools/MASTERPRIME/MASTERPRIME-32MM', "nuke.createNode('MASTERPRIME-32MM.nk')")
gizmoMenu.addCommand('Lens Tools/MASTERPRIME/MASTERPRIME-40MM', "nuke.createNode('MASTERPRIME-40MM.nk')")
gizmoMenu.addCommand('Lens Tools/MASTERPRIME/MASTERPRIME-65MM', "nuke.createNode('MASTERPRIME-65MM.nk')")
gizmoMenu.addCommand('Lens Tools/MASTERPRIME/MASTERPRIME-75MM', "nuke.createNode('MASTERPRIME-75MM.nk')")
gizmoMenu.addCommand('Lens Tools/MASTERPRIME/MASTERPRIME-100MM', "nuke.createNode('MASTERPRIME-100MM.nk')")
gizmoMenu.addCommand('Lens Tools/MASTERPRIME/MASTERPRIME-135MM', "nuke.createNode('MASTERPRIME-135MM.nk')")

gizmoMenu.addMenu('Lens Tools/VISTA-M')
gizmoMenu.addCommand('Lens Tools/VISTA-M/VISTA-M-18MM', "nuke.createNode('VISTA-M-18MM.nk')")
gizmoMenu.addCommand('Lens Tools/VISTA-M/VISTA-M-25MM', "nuke.createNode('VISTA-M-25MM.nk')")
gizmoMenu.addCommand('Lens Tools/VISTA-M/VISTA-M-35MM', "nuke.createNode('VISTA-M-35MM.nk')")
gizmoMenu.addCommand('Lens Tools/VISTA-M/VISTA-M-50MM', "nuke.createNode('VISTA-M-50MM.nk')")
gizmoMenu.addCommand('Lens Tools/VISTA-M/VISTA-M-85MM', "nuke.createNode('VISTA-M-85MM.nk')")

gizmoMenu.addMenu('Lens Tools/FUJINON')
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-ZOOM', "nuke.createNode('FUJINON-ZOOM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-18MM', "nuke.createNode('FUJINON-18MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-20MM', "nuke.createNode('FUJINON-20MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-22MM', "nuke.createNode('FUJINON-22MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-25MM', "nuke.createNode('FUJINON-25MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-30MM', "nuke.createNode('FUJINON-30MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-35MM', "nuke.createNode('FUJINON-35MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-40MM', "nuke.createNode('FUJINON-40MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-45MM', "nuke.createNode('FUJINON-45MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-50MM', "nuke.createNode('FUJINON-50MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-55MM', "nuke.createNode('FUJINON-55MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-60MM', "nuke.createNode('FUJINON-60MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-65MM', "nuke.createNode('FUJINON-65MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-70MM', "nuke.createNode('FUJINON-70MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-75MM', "nuke.createNode('FUJINON-75MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-80MM', "nuke.createNode('FUJINON-80MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-85MM', "nuke.createNode('FUJINON-85MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-100MM', "nuke.createNode('FUJINON-100MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-120MM', "nuke.createNode('FUJINON-120MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-140MM', "nuke.createNode('FUJINON-140MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-160MM', "nuke.createNode('FUJINON-160MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-180MM', "nuke.createNode('FUJINON-180MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-200MM', "nuke.createNode('FUJINON-200MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-225MM', "nuke.createNode('FUJINON-225MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-250MM', "nuke.createNode('FUJINON-250MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-275MM', "nuke.createNode('FUJINON-275MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-300MM', "nuke.createNode('FUJINON-300MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-325MM', "nuke.createNode('FUJINON-325MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-350MM', "nuke.createNode('FUJINON-350MM.nk')")
gizmoMenu.addCommand('Lens Tools/Fujinon18-400/FUJINON-400MM', "nuke.createNode('FUJINON-400MM.nk')")

#LD_3DE4 Plugins
gizmoMenu.addCommand("Lens Tools/3DE4/LD_3DE4_Anamorphic_Standard_Degree_4", "nuke.createNode('LD_3DE4_Anamorphic_Standard_Degree_4')")
gizmoMenu.addCommand("Lens Tools/3DE4/LD_3DE4_Anamorphic_Rescaled_Degree_4", "nuke.createNode('LD_3DE4_Anamorphic_Rescaled_Degree_4')")
gizmoMenu.addCommand("Lens Tools/3DE4/LD_3DE4_Anamorphic_Degree_6", "nuke.createNode('LD_3DE4_Anamorphic_Degree_6')")
gizmoMenu.addCommand("Lens Tools/3DE4/LD_3DE4_Radial_Standard_Degree_4", "nuke.createNode('LD_3DE4_Radial_Standard_Degree_4')")
gizmoMenu.addCommand("Lens Tools/3DE4/LD_3DE4_Radial_Fisheye_Degree_8", "nuke.createNode('LD_3DE4_Radial_Fisheye_Degree_8')")
gizmoMenu.addCommand("Lens Tools/3DE4/LD_3DE_Classic_LD_Model", "nuke.createNode('LD_3DE_Classic_LD_Model')")



# The "CameraToolz" specific menu items
gizmoMenu.addMenu('Camera Tools', icon='lux_camera_tools.png')
gizmoMenu.addCommand('Camera Tools/CamQuake', 'nuke.nodes.CamQuake()')
gizmoMenu.addCommand('Camera Tools/EngineShake', 'nuke.nodes.ALT_engineBase()')
gizmoMenu.addCommand('Camera Tools/CameraShake', 'nuke.nodes.ALT_engineRough()')
gizmoMenu.addCommand('Camera Tools/EXT_Shake', 'nuke.nodes.alt_ext_shake()')
gizmoMenu.addCommand('Camera Tools/EXT_Shake_motion_blur', 'nuke.nodes.alt_ext_shake_MB()')
gizmoMenu.addCommand('Camera Tools/INT_Shake', 'nuke.nodes.alt_int_shake()')


# The "Guides" specific menu items
gizmoMenu.addMenu('Guides', icon='lux_guides.png')
gizmoMenu.addCommand('Guides/AspectGuide', 'nuke.nodes.AspectGuide()')
gizmoMenu.addCommand('Guides/GridOverlay', 'nuke.nodes.GridOverlay()')
gizmoMenu.addCommand('Guides/GoldenRatio', "nuke.createNode('lx_GoldenRatio')")




# The "LUX Write" specific menu items
gizmoMenu.addMenu('Read\Write', icon='lux_writes.png')
gizmoMenu.addCommand('Read\Write/LuxWRITE (Empty)', 'nuke.createNode("lux_write.gizmo")')
gizmoMenu.addCommand('Read\Write/LuxWRITE (JPEG)', 'nuke.createNode("lux_write_jpeg.gizmo")', 'shift+w')


#gizmoMenu.addCommand('Read\Write/LuxOUTPUT', 'nuke.createNode("lux_write_output.gizmo")', 'f11')# this will need to be expanded on.
#gizmoMenu.addCommand('Read\Write/LuxPRECOMP', 'nuke.createNode("lux_write_precomp.gizmo")', 'f10')

gizmoMenu.addCommand('Read\Write/LuxOUTPUT', 'importAssets.ImportAssets().createLuxWrites(wtype="OUTPUT")', 'f11')
gizmoMenu.addCommand('Read\Write/LuxPRECOMP', 'importAssets.ImportAssets().createLuxWrites(wtype="PRECOMP")', 'f10')

#GARBAGE
#gizmoMenu.addCommand('defocus_001', "nuke.createNode('lx_defocus_001')")
#gizmoMenu.addCommand('convolve_001', "nuke.createNode('lx_convolve_001')")
#gizmoMenu.addCommand('zblur_001', "nuke.createNode('lx_zblur_001')")
#gizmoMenu.addCommand('transform_0_1', "nuke.createNode('lx_transform_0_1')")
#gizmoMenu.addCommand('reformat_0_1', "nuke.createNode('lx_reformat_0_1')")
#gizmoMenu.addCommand('lensdistortion_0_1', "nuke.createNode('lx_lensdistortion_0_1')")

#GREEN
#LUX Macros
macroMenu = toolbar.addMenu('LUX Macros', icon='lux_green_32.png')
macroMenu.addCommand('Autocomp EXR Passes (VRay)', 'import autoComp; autoComp.autoComp()', icon='vray_logo.png')
macroMenu.addCommand('Autocomp EXR Passes (Clarisse)', 'nuke.nodePaste("//qumulo/Libraries/HAL/LIVEAPPS/apps/Scripts/NUKE/scripts/Clarisse/clarisse_breakout_v002.nk")', icon='clarisse_logo.png')
macroMenu.addCommand('Contact Sheet Namer', 'import contactSheetNamer; contactSheetNamer.contactSheetNamer()', icon='contactSheet.png')
macroMenu.addCommand('Random Tile', 'RandomTile.randomTile()','',icon='RandomTile.png')
macroMenu.addCommand('Quick 3d', 'import quick3d; quick3d.quick3d()')
macroMenu.addCommand('Pan And Tile', 'import panAndTile; panAndTile.panAndTile()')
macroMenu.addCommand('Auto Backdrop', 'import autoBackdrop; autoBackdrop.autoBackdrop()', 'alt+b')
macroMenu.addCommand('Fix Paths', 'fixPaths.fixPaths()')
macroMenu.addCommand('Delete Disabled Nodes', 'nodeOps.deleteDisabled()')
macroMenu.addCommand('Disable invert', 'nodeOps.disable_invert()', 'shift+d')
macroMenu.addCommand('Extract Roto Shapes', 'import extractRotoShapes; extractRotoShapes.extractRotoShapes()')
macroMenu.addCommand('Unpremult by Alpha', 'nodeOps.alphaUnpremult()', 'ctrl+u')
macroMenu.addCommand('Import Jpeg plates from selected', 'nodeOps.import_jpegs_from_selected()', 'ctrl+j')
macroMenu.addCommand('Import Jpeg with Gui Switch', 'nodeOps.import_jpegs_with_gui()')
macroMenu.addCommand('Disable Node Localization', 'nodeOps.disable_node_localization()')
macroMenu.addCommand('Enable Node Localization', 'nodeOps.enable_node_localization()')
macroMenu.addCommand('Set BBox to B', 'nodeOps.bbox_B()', 'ctrl+b')
#macroMenu.addCommand('Create a Write Node for RotoFrames', 'import aliScript; aliScript.rotoFrameWrite()')
macroMenu.addCommand('Create a Write Node for Roto Frames', 'import rotoframe; reload(rotoframe); rotoframe.RotoFrames().create_roto_write(nuke.selectedNodes())')
macroMenu.addCommand('Create a Write Node for MatchMove Frames', 'import mmframe; reload(mmframe); mmframe.RotoFrames().create_roto_write(nuke.selectedNodes())')
macroMenu.addCommand('Paste Multiple', 'import multiPaste; multiPaste.multiPaste()', 'shift+ctrl+v')
macroMenu.addCommand('Roto Points to Tracker', 'import rotoTrack; rotoTrack.rotoTrack()')
macroMenu.addCommand('reconcile3D to CornerPin', 'import reconcileCornerPin; reconcileCornerPin.reconcileCornerPin()')
macroMenu.addMenu('Misc. Macros')
macroMenu.addCommand('Misc. Macros/Animate Merge', 'nodeOps.mergeAnim()')
macroMenu.addCommand('Misc. Macros/Change Filter', 'nodeOps.changeFilter()')
macroMenu.addCommand('Misc. Macros/Dont Use GPU', 'nodeOps.dontUseGPU()')

macroMenu.addCommand("Create Camera from EXR 3D Render", "import createExrCamVray; createExrCamVray.createExrCamVray(nuke.selectedNode())")
macroMenu.addCommand("Render With LUX Logo", 'import renderWithLogo; renderWithLogo.renderWithLogo()')

macroMenu.addCommand("Invert Transformation Matrix", 'import invert_transform_matrix; invert_transform_matrix.invert_transform_matrix()')


macroMenu.addCommand('Transfer Selected 3D data to 2D Tracker', 'import cgTracker; cgTracker.cgTracker()')
macroMenu.addCommand('Breakout Passes','import breakout; breakout.breakout()', icon='breakout.png')
macroMenu.addCommand('LensDistort Compiler','import lensDistort_Group; lensDistort_Group.lensDistort_Group()')

#nodeMenu = nuke.menu('Nuke').findItem('File')
#nodeMenu.addCommand('Ftrack Shot Launcher', 'import ftrack_shot_launcher; ftrack_shot_launcher.showDialog()', 'ctrl+shift+o', icon='ftrack_32.png')


#BLUE
#Workflow items   - Macors; Mandatory macros that an artist would use regardless of the shot they are working on
workflowMenu = toolbar.addMenu('Workflow Tools', icon='lux_blue_32.png')
#workflowMenu.addCommand('Ftrack Shot Launcher', 'import ftrack_shot_launcher; ftrack_shot_launcher.showDialog()', 'ctrl+shift+o', icon='ftrack_32.png')
workflowMenu.addMenu('Ingest', icon='ingest4.png')
workflowMenu.addCommand('Ingest/Ingest Script','import ingest2; ingest2.ingestScript().ui()', 'f9', icon='ingest4.png')
workflowMenu.addCommand('Ingest/Ingest Script old','import ingest; ingest.ingestScript().ui()', 'shift+f9', icon='ingest4.png')
workflowMenu.addCommand('Ingest/Ingest Element','import ingestElement; ingestElement.ingestElement()', icon='ingest4.png')
workflowMenu.addCommand('Update Selected to Latest','import lux_utils; lux_utils.updateToLatest(20)', icon='ingest4.png')
workflowMenu.addCommand('Get All Read names connected to node','import lux_utils; lux_utils.getConnectedReadPaths()', icon='ingest4.png')
#workflowMenu.addCommand('Get all file paths','import aliScript; aliScript.get_file_paths()')
workflowMenu.addCommand('Open File in DJV_View','import open_in_djvview; open_in_djvview.launch_with_DJVView()','f6')
###MULTI CLIPBOARD
'''
workflowMenu.addMenu('Multi Clipboard')
workflowMenu.addMenu('Multi Clipboard/Copy')

workflowMenu.addCommand('Multi Clipboard/Copy/Copy 1', 'multi_clipboard.multi_clipboard().copy(1)', 'ctrl+1')
workflowMenu.addCommand('Multi Clipboard/Copy/Copy 2', 'multi_clipboard.multi_clipboard().copy(2)', 'ctrl+2')
workflowMenu.addCommand('Multi Clipboard/Copy/Copy 3', 'multi_clipboard.multi_clipboard().copy(3)', 'ctrl+3')
workflowMenu.addCommand('Multi Clipboard/Copy/Copy 4', 'multi_clipboard.multi_clipboard().copy(4)', 'ctrl+4')
workflowMenu.addCommand('Multi Clipboard/Copy/Copy 5', 'multi_clipboard.multi_clipboard().copy(5)', 'ctrl+5')
workflowMenu.addCommand('Multi Clipboard/Copy/Copy 6', 'multi_clipboard.multi_clipboard().copy(6)', 'ctrl+6')
workflowMenu.addCommand('Multi Clipboard/Copy/Copy 7', 'multi_clipboard.multi_clipboard().copy(7)', 'ctrl+7')
workflowMenu.addCommand('Multi Clipboard/Copy/Copy 8', 'multi_clipboard.multi_clipboard().copy(8)', 'ctrl+8')
workflowMenu.addCommand('Multi Clipboard/Copy/Copy 9', 'multi_clipboard.multi_clipboard().copy(9)', 'ctrl+9')
workflowMenu.addCommand('Multi Clipboard/Copy/Copy 0', 'multi_clipboard.multi_clipboard().copy(0)', 'ctrl+0')

workflowMenu.addMenu('Multi Clipboard/Paste')
workflowMenu.addCommand('Multi Clipboard/Paste/Paste 1', 'multi_clipboard.multi_clipboard().paste(1)', 'shift+1')
workflowMenu.addCommand('Multi Clipboard/Paste/Paste 2', 'multi_clipboard.multi_clipboard().paste(2)', 'shift+2')
workflowMenu.addCommand('Multi Clipboard/Paste/Paste 3', 'multi_clipboard.multi_clipboard().paste(3)', 'shift+3')
workflowMenu.addCommand('Multi Clipboard/Paste/Paste 4', 'multi_clipboard.multi_clipboard().paste(4)', 'shift+4')
workflowMenu.addCommand('Multi Clipboard/Paste/Paste 5', 'multi_clipboard.multi_clipboard().paste(5)', 'shift+5')
workflowMenu.addCommand('Multi Clipboard/Paste/Paste 6', 'multi_clipboard.multi_clipboard().paste(6)', 'shift+6')
workflowMenu.addCommand('Multi Clipboard/Paste/Paste 7', 'multi_clipboard.multi_clipboard().paste(7)', 'shift+7')
workflowMenu.addCommand('Multi Clipboard/Paste/Paste 8', 'multi_clipboard.multi_clipboard().paste(8)', 'shift+8')
workflowMenu.addCommand('Multi Clipboard/Paste/Paste 9', 'multi_clipboard.multi_clipboard().paste(9)', 'shift+9')
workflowMenu.addCommand('Multi Clipboard/Paste/Paste 0', 'multi_clipboard.multi_clipboard().paste(0)', 'shift+0')
'''

###GLOBAL CLIPBOARD
workflowMenu.addMenu('Global Clipboard')
workflowMenu.addCommand('Global Clipboard/Copy', 'gcb.GlobalClipboard().copy()', 'ctrl+alt+c')
workflowMenu.addCommand('Global Clipboard/Paste from...', 'gcb.GlobalClipboard().showDialog()', 'ctrl+alt+shift+v')
workflowMenu.addCommand('How many nodes?','import numberNodes; numberNodes.howmany()')
workflowMenu.addCommand('Get File Paths','nodeOps.get_sources()')
workflowMenu.addCommand('Check Efficiency','import checkEfficiency; checkEfficiency.checkEfficiency()')
workflowMenu.addCommand('Version Up','versionUp.versionUp()', 'f12', icon='floppySave.png')
#workflowMenu.addCommand('Create Write Node','import writeNodePath; writeNodePath.writeNodePath()', icon='writeNodePath.png')
workflowMenu.addCommand('Re-Link','import relink; relink.relink()', icon='link.png')
workflowMenu.addCommand('Download Video','import nukeYoutube; nukeYoutube.start()', icon="nukeYoutube.png")
#workflowMenu.addCommand('Content Generator','import contentGen; contentGen.gen()', icon='contentGen.png')
workflowMenu.addCommand('Open path in browser', 'browseDir.browseDir()', 'f1', icon='browseDir.png')
workflowMenu.addCommand('Browse COMP Directory', 'browseDir.browseDiscipline("05_COMP")', 'f2', icon='browseDir.png')
workflowMenu.addCommand('Browse RENDERS Directory', 'browseDir.browseDiscipline("06_RENDERS")', 'f3', icon='browseDir.png')
workflowMenu.addCommand('Browse PLATES Directory', 'browseDir.browseDiscipline("01_PLATES")', 'f4', icon='browseDir.png')
workflowMenu.addCommand('Import from Write', 'import aliScript; aliScript.importPath()', 'shift+r', icon='compare.png')


#\\qumulo\Libraries\HAL\LIVEAPPS\


#YELLOW
#Show specific tools. 
shotMenu = toolbar.addMenu('Shot Specific Tools', icon='lux_yellow_32.png')
shotMenu.addCommand('Match Cutref', 'import matchCutref; matchCutref.matchCutref()', icon='cdl_32.png')
shotMenu.addCommand('Get Shot CDLs', 'import get_CDL; get_CDL.get_cdl()', icon='cdl_32.png')

#Import functions
shotMenu.addMenu('Import Assets')
shotMenu.addCommand('Import Assets/Import All Assets', 'importAssets.ImportAssets().importAll()')
shotMenu.addCommand('Import Assets/Import Plates', 'importAssets.ImportAssets().importPlates()')
shotMenu.addCommand('Import Assets/Import Cutrefs', 'importAssets.ImportAssets().importCutrefs()')
shotMenu.addCommand('Import Assets/Import Geos', 'importAssets.ImportAssets().importGeos()')
shotMenu.addCommand('Import Assets/Import Cameras', 'importAssets.ImportAssets().importCameras()')
shotMenu.addCommand('Import Assets/Import 3D Renders', 'importAssets.ImportAssets().importRenders()')
shotMenu.addCommand('Import Assets/Import LensDistorts', 'importAssets.ImportAssets().importUndistorts()')
shotMenu.addCommand('Import Assets/Import Latest Comps', 'importAssets.ImportAssets().importLatestComps()')
shotMenu.addCommand('Import Assets/Import Writes', 'importAssets.ImportAssets().createLuxWrites()')
shotMenu.addCommand('Import Assets/Create Plate Writes', 'importAssets.ImportAssets().createPlateWritesUI()')


shotMenu.addMenu('TRAINING', icon='learn_32.png')
shotMenu.addCommand('TRAINING/Keying_Template_001', 'nuke.nodePaste("//qumulo/Libraries/HAL/LIVEAPPS/apps/Scripts/NUKE/scripts/Tutorial_Templates/Keying_Template_001.nk")')
shotMenu.addCommand('TRAINING/Keying_Cleanscreen_Template_001', 'nuke.nodePaste("//qumulo/Libraries/HAL/LIVEAPPS/apps/Scripts/NUKE/scripts/Tutorial_Templates/Keying_Cleanscreen_Template_001")')
shotMenu.addCommand('TRAINING/Breakdown_template_001', 'nuke.nodePaste("//qumulo/Libraries/HAL/LIVEAPPS/apps/Scripts/NUKE/scripts/Tutorial_Templates/Breakdown_template_001.nk")')

'''
#YELLOW
#Show specific tools. 
shotMenu = toolbar.addMenu('Shot Specific Tools', icon='lux_yellow_32.png')
shotMenu.addCommand('Get Shot CDLs', 'import get_CDL; get_CDL.get_cdl()', icon='cdl_32.png')
shotMenu.addCommand('Set Shot Status', 'import setStatus; setStatus.SetStatus().showDialog()', 'alt+s', icon='lux_logo_32.png')

shotMenu.addMenu('BEY', icon='bey_32.png')
shotMenu.addCommand('BEY/Templates/Batman Effect 1', 'nuke.nodePaste("L:/HAL/LIVEAPPS/apps/Scripts/NUKE/scripts/BEY_Batman_Effect_Template_v001.nk")')
shotMenu.addCommand('BEY/Templates/Batman Effect 2', 'nuke.nodePaste("L:/HAL/LIVEAPPS/apps/Scripts/NUKE/scripts/BEY_Batman_Effect_Template_v002.nk")')
shotMenu.addCommand('BEY/Get JPG LUT', 'nuke.nodePaste("L:/HAL/LIVEAPPS/apps/Scripts/NUKE/scripts/BEY_lut.nk")')
shotMenu.addCommand('BEY/Set Selected Writes to Lowercase', 'import convert_writes_to_lowercase; convert_writes_to_lowercase.convert_writes_to_lowercase()')

shotMenu.addMenu('WIL', icon='william_32.png')
shotMenu.addCommand('WIL/Get JPG LUT', 'nuke.nodePaste("L:/HAL/LIVEAPPS/apps/Scripts/NUKE/scripts/WIL_lut.nk")')
shotMenu.addCommand('WIL/LensDistortion/16mm', 'nuke.nodePaste("X:/apps/Scripts/NUKE/scripts/WIL_LensDistortion/LensDistortion_16mm.nk")')
shotMenu.addCommand('WIL/LensDistortion/24mm', 'nuke.nodePaste("X:/apps/Scripts/NUKE/scripts/WIL_LensDistortion/LensDistortion_24mm.nk")')
shotMenu.addCommand('WIL/LensDistortion/50mm', 'nuke.nodePaste("X:/apps/Scripts/NUKE/scripts/WIL_LensDistortion/LensDistortion_50mm.nk")')
shotMenu.addCommand('WIL/LensDistortion/85mm', 'nuke.nodePaste("X:/apps/Scripts/NUKE/scripts/WIL_LensDistortion/LensDistortion_85mm.nk")')
shotMenu.addCommand('WIL/LensDistortion/135mm', 'nuke.nodePaste("X:/apps/Scripts/NUKE/scripts/WIL_LensDistortion/LensDistortion_135mm.nk")')

shotMenu.addMenu('TRAINING', icon='learn_32.png')
shotMenu.addCommand('TRAINING/Keying_Template_001', 'nuke.nodePaste("X:/apps/Scripts/NUKE\scripts/Tutorial_Templates/Keying_Template_001.nk")')
shotMenu.addCommand('TRAINING/Keying_Cleanscreen_Template_001', 'nuke.nodePaste("X:/apps/Scripts/NUKE\scripts/Tutorial_Templates/Keying_Cleanscreen_Template_001")')
shotMenu.addCommand('TRAINING/Breakdown_template_001', 'nuke.nodePaste("X:/apps/Scripts/NUKE\scripts/Tutorial_Templates/Breakdown_template_001.nk")')
'''




ftrackMenu = toolbar.addMenu('ftrack', icon='lux_ftrack_32.png')
ftrackMenu.addCommand('Ftrack Info', 'ftrack_nuke_utils.go_to_ftrack_tab()', 'ctrl+f', icon='lux_ftrack_32.png')
#ftrackMenu.addCommand('Get Shot Info from Ftrack', 'import get_shot_info; get_shot_info.get_shot_info()', icon='lux_ftrack_32.png')
ftrackMenu.addCommand('Set Shot Status', 'import setStatus; setStatus.SetStatus().showDialog()', 'alt+s', icon='lux_ftrack_32.png')
ftrackMenu.addCommand('Open Ftrack Link', 'ftrack_nuke_utils.open_in_dashboard( nuke.Root()["ftrack_id"].value() )', 'alt+f', icon='lux_ftrack_32.png')
ftrackMenu.addCommand('Open Ftrack Project Link', 'ftrack_nuke_utils.open_in_projects( nuke.Root()["ftrack_parent_id"].value() )', 'ctrl+alt+f', icon='lux_ftrack_32.png')


#Submit to Deadline --from Deadline10
deadlineMenu= toolbar.addMenu('LUX', icon='lux_render_32.png')
#deadlineMenu.addCommand("Submit To Deadline", "import SubmitToDeadline; SubmitToDeadline.main()", "F8", icon='tool_menu.png')
deadlineMenu.addCommand("Submit To Deadline", DeadlineNukeClient.main, "F8", icon='tool_menu.png')
try:
    if nuke.env[ 'studio' ] or nuke.env[ 'NukeVersionMajor' ] >= 11:
        import DeadlineNukeFrameServerClient
        deadlineMenu.addCommand("Reserve Frame Server Slaves", DeadlineNukeFrameServerClient.main, "")
except:
    pass
try:
    import DeadlineNukeVrayStandaloneClient
    deadlineMenu.addCommand("Submit V-Ray Standalone to Deadline", DeadlineNukeVrayStandaloneClient.main, "")
except:
    pass



# Video Copilot
toolbar.addMenu("VideoCopilot", icon="VideoCopilot.png")
toolbar.addCommand( "VideoCopilot/OpticalFlares", "nuke.createNode('OpticalFlares')", icon="OpticalFlares.png")



try:
	# The "Merge" menu
	ms = nuke.menu("Nodes").menu("Merge").menu("Merges")
	ms.addCommand("Average", "nuke.createNode('Merge2', 'operation average name Average', False)")
	ms.addCommand("Copy", "nuke.createNode('Merge2', 'operation copy name Copy', False)")
	ms.addCommand("Difference", "nuke.createNode('Merge2', 'operation difference name Difference', False)")
	ms.addCommand("Divide", "nuke.createNode('Merge2', 'operation divide name Divide', False)")
	ms.addCommand("From", "nuke.createNode('Merge2', 'operation from name From', False)")
	ms.addCommand("Mask", "nuke.createNode('Merge2', 'operation mask name Mask', False)")
	ms.addCommand("Minus", "nuke.createNode('Merge2', 'operation minus name Minus', False)")
	ms.addCommand("Multiply", "nuke.createNode('Merge2', 'operation multiply name Multiply', False)")
	ms.addCommand("Plus", "nuke.createNode('Merge2', 'operation plus name Plus', False)")
	ms.addCommand("Screen", "nuke.createNode('Merge2', 'operation screen name Screen', False)")
	ms.addCommand("Stencil", "nuke.createNode('Merge2', 'operation stencil name Stencil', False)")
	ms.addCommand("Under", "nuke.createNode('Merge2', 'operation under name Under', False)")
except:
	pass

'''
### AutoCARD ###
def AutoCard():
	nuke.nodes.Card()
	nuke.nodes.TransformGeo()
nuke.menu("Nodes").addCommand("3D/Geometry/Auto Card","AutoCard()",icon="Card.png")
'''

#Run scripts on Nuke startup
def killViewers():
	for v in nuke.allNodes("Viewer"):
		nuke.delete(v)
nuke.addOnScriptLoad(killViewers)

# Presses the getShotPath button upon creation.
def lux_write_onCreate():
    if nuke.thisNode().knob("luxwrite"):
    	if len(nuke.thisNode()['root_path'].value()) < 2:
        	nuke.thisNode()['getShotPath'].execute()
nuke.addOnCreate(lux_write_onCreate, nodeClass='Group')
# Connects the lux write nodes if V000/V001 (script generated from hiero) of the script is opened.
# Always connects it to "ModifyMetaData2", so make sure V000/V001 of the script is ingested through Hiero!
def lux_write_node_connect():
	try:
		if (nuke.Root().name().upper().split('_V')[-1].split('.')[0]) in ['000', '001']:
			lxw_nodes = [i for i in nuke.allNodes('Group') if (i.knob('luxwrite') and ((i.input(0) == None) or ("lux_" in i.input(0).name().lower())) )]
			connect_to = "ModifyMetaData2"
			if not nuke.toNode(connect_to):
				connect_to = "ModifyMetaData1"
			for lxw in lxw_nodes:
				lxw.setInput(0, nuke.toNode(connect_to))
				lxw.autoplace()
	except:
	    print 'exception happened while trying to connect inputs of the lux_write nodes.'
	    pass

#nuke.addOnScriptLoad(lux_write_node_connect)
# Presses the getShotPath button if the parameters are empty upon opening a script.
def lux_write_onScriptLoad():
	lxw_nodes = [i.name() for i in nuke.allNodes('Group') if i.knob('luxwrite') ]
	for i in lxw_nodes:
		n = nuke.toNode("root.%s" % i)
		if len( n['root_path'].value() ) < 2:
			n['getShotPath'].execute()
			existing_assets = n['existing_asset'].values()
			for a in existing_assets:
				if a.lower() in nuke.Root().name().lower():
					n['tag'].setValue(a)

nuke.addOnScriptLoad(lux_write_onScriptLoad)

def setCodeForWrites():
	for w in nuke.allNodes("Write"):
		if w['label'].value()!='SLATE': #SLATE TEMPLATES EXCLUDED
			w['beforeRender'].setValue('def createPath():\n    file = nuke.filename(nuke.thisNode())\n    dir = os.path.dirname(file)\n    osdir = nuke.callbacks.filenameFilter(dir)\n    try:\n        os.makedirs (osdir)\n    except OSError:\n        pass\ncreatePath()\ndef saveRenderScript():\n    try:\n        assetFileName = nuke.filename(nuke.thisNode()).split(".")[0]+".nk"\n        print "Saving a copy of the render script >> ", assetFileName\n        nuke.scriptSave(assetFileName)\n    except:\n        pass\nsaveRenderScript()')
			w['afterRender'].setValue('')
			w['renderProgress'].setValue('')
		
#nuke.addOnScriptLoad(setCodeForWrites)#is this even necesarry? this seems like outdated. all the write nodes already have this by default.

nuke.addKnobChanged(lux_write_knobchanged.lux_write_knobchanged, nodeClass="Group")



#import lux_callbacks
#nuke.addOnCreate(lambda: lux_callbacks.record_node(nuke.thisNode().Class(), nuke.thisNode().name()))