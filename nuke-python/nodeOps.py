# Copyright (c) 2009 LUX Visual Effects Inc.  All Rights Reserved.

import nuke


# Toggles viewer pipes off and on
def toggleViewerPipes():
   for n in nuke.allNodes('Viewer'):
       curValue = n['hide_input'].value()
       n['hide_input'].setValue(not curValue)

# Turns off the Use GPU If Available knobs
def dontUseGPU():
    if nuke.selectedNodes():
        for n in nuke.selectedNodes():
            if 'useGPUIfAvailable' in n.knobs():
                #print n.name()
                n['useGPUIfAvailable'].setValue(False)
    else:
        for n in nuke.allNodes():
            if 'useGPUIfAvailable' in n.knobs():
                #print n.name()
                n['useGPUIfAvailable'].setValue(False)

# Deletes disabled nodes
def deleteDisabled():
    for i in nuke.allNodes():
        try:
            if i['disable'].value()==True:
                nuke.delete(i)
        except:
            pass

# Toggles the disable knob on selected nodes
def disable_invert():
    import nuke
    for i in nuke.selectedNodes():
        i['disable'].setValue(not i['disable'].value())
        
# Toggles the unpremult by alpha knob on selected nodes
def alphaUnpremult():
    for i in nuke.selectedNodes():
        if i.knob('unpremult'):
            if i['unpremult'].value()=='alpha':
                i['unpremult'].setValue('none')
            else:
                i['unpremult'].setValue('alpha')

# Sets the BBox to B on selected nodes
def bbox_B():
    for i in nuke.selectedNodes():
        if i.knob('bbox'):
            i.knob('bbox').setValue('B')

# Animates a merge
def mergeAnim():
    node = nuke.selectedNode()
    inputs = node.inputs()
    param=node['mix']
    param.setAnimated()
    x = 0
    
    for i in range(0, inputs):
    
        if node.input(i).knob('first_frame_1') != None: 
            v =  int(node.input(i)['first_frame_1'].value())
    
        elif node.input(i).knob('first_frame') != None:
            v =  int(node.input(i)['first_frame'].value())
    
        print v
        
        param.setValueAt(x, v)
        x+=1
        
#Changes the filter on selected nodes
def changeFilter():
    p = nuke.Panel('Change Filter')
    p.addEnumerationPulldown('filter', 'Impulse Cubic Keys Simon Rifman Mitchell Parzen Notch Lanczos4 Lanczos6 Sinc4')
    
    ret = p.show()
    def setFilter():
        if p:
            for n in nuke.selectedNodes():
                n['filter'].setValue(p.value('filter'))
    setFilter()

#Imports a jpeg
def import_jpegs_from_selected():

    for i in nuke.selectedNodes('Read'):

        full_res_jpeg = i['file'].value()
        full_res_jpeg = full_res_jpeg.replace('.exr', '.jpeg')
        full_res_jpeg = full_res_jpeg.replace('.EXR', '.JPEG')
        full_res_jpeg = full_res_jpeg.replace('01_EXRS', '02_FULL_RES_JPEGS')

        r = nuke.createNode('Read')
        r['file'].setValue(full_res_jpeg)
        r['first'].setValue(i['first'].value())
        r['last'].setValue(i['last'].value())
        r['label'].setValue(i['label'].value())

#Sets up a gui template from selected read nodes.
def import_jpegs_with_gui():

    for i in nuke.selectedNodes('Read'):

        full_res_jpeg = i['file'].value()
        full_res_jpeg = full_res_jpeg.replace('.exr', '.jpeg')
        full_res_jpeg = full_res_jpeg.replace('.EXR', '.JPEG')
        full_res_jpeg = full_res_jpeg.replace('01_EXRS', '02_FULL_RES_JPEGS')

        r = nuke.createNode('Read',inpanel=False)
        r['file'].setValue(full_res_jpeg)
        r['first'].setValue(i['first'].value())
        r['last'].setValue(i['last'].value())
        r['label'].setValue(i['label'].value())

        reformat = nuke.createNode('Reformat',inpanel=False)
        reformat.setInput(0,r)

        gui = nuke.createNode('gui.gizmo',inpanel=False)
        gui.setInput(0, i)
        gui.setInput(1, reformat)


#Disables Localization knob of node(s)
def disable_node_localization():
    nodes = nuke.selectedNodes('Read')
    if not nodes:
        nodes = nuke.allNodes('Read')
    for n in nodes:
        if 'localizationPolicy' in n.knobs():
            n['localizationPolicy'].setValue('off')
            
#Enables Localization knob of node(s)
def enable_node_localization():
    nodes = nuke.selectedNodes('Read')
    if not nodes:
        nodes = nuke.allNodes('Read')
    for n in nodes:
        if 'localizationPolicy' in n.knobs():
            n['localizationPolicy'].setValue('on')



def get_sources():
    nodes = nuke.selectedNodes()
    if not nodes:
        nodes = nuke.allNodes()

    nodes_with_file_knob = [i for i in nodes if i.knob('file')]
    files = []
    message = ''
    for node in nodes_with_file_knob:
        if node.knob('disable'):
            if node['disable'].value()==False:
                file = node['file'].value()
                files.append(file)
                
    files = list(set(files))
    files.sort()
    for file in files:
        message += file+'\n\n'
    nuke.message(message)

