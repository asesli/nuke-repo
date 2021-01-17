## Autocomp V1.04
## July 30 2019
## Written by Alican Sesli 
## LUX Visual Effects
## VRay breakout that accounts for all layers.
##
## rawLight breakout prefix = raw_
## specular breakout prefix = spec_
 
import nuke

def mirrorNodes( nodes, direction = 'x' ):
    #Mirror nodes either horizontally or vertically.
    if len( nodes ) < 2:
        return
    if direction.lower() not in ('x', 'y'):
        raise ValueError, 'direction argument must be x or y'
    if direction.lower() == 'x':
        positions = [ float( n.xpos()+n.screenWidth()/2 ) for n in nodes ]
    else:
        positions = [ float( n.ypos()+n.screenHeight()/2 ) for n in nodes ]
    axis = sum( positions ) / len( positions )
    for n in nodes:
        if direction.lower() == 'x':
            n.setXpos( int( n.xpos() - 2*(n.xpos()+n.screenWidth()/2-axis) ) )
        else:
            n.setYpos( int( n.ypos() - 2*(n.ypos()+n.screenHeight()/2-axis) ) )
    return axis

def autoComp():
    node = nuke.selectedNode()
    
    
    nodesToSelect = []
    readNodes = []
    nodesToSelect.append(node)

    def climb(node):
        for n in node.dependencies():
            nodesToSelect.append(n)
            climb(n)
    climb(node)

    for i in nodesToSelect:
        if 'read' in i.name().lower():
            readNodes.append(i)
    if len(readNodes)>0:
        readNode = readNodes[0]
        elemID = (readNode['file'].value().split('/')[-1]).split('.')[0]
    else:
        elemID = ''
    print elemID

    

    tileWidth = nuke.toNode("preferences")['TileWidth'].value() 
    dotScale = nuke.toNode("preferences")['dot_node_scale'].value()
    dot_offset = (tileWidth/2)-((dotScale*10)/2)

    nodeXOffset = 150
    nodeYOffset = 150

    firstDot = nuke.createNode('Dot', inpanel=False)
    firstDot.setInput(0, node)
    firstDot['xpos'].setValue(node['xpos'].value())
    firstDot['ypos'].setValue(node['ypos'].value()+nodeYOffset)
    firstDot['label'].setValue(elemID)
    firstDot['note_font_size'].setValue(100)


    c='''
dinput=nuke.thisNode().input(0)
elem = (dinput['file'].value().split('/')[-1]).split('.')[0]
nuke.thisNode()['label'].setValue(elem)
'''
    pyk = nuke.PyScript_Knob('update_name','Update Name',c)
    firstDot.addKnob(pyk)
    
    lastDot = nuke.createNode('Dot', inpanel=False)
    lastDot.setInput(0, node)
    lastDot['xpos'].setValue(node['xpos'].value())
    lastDot['ypos'].setValue(node['ypos'].value()+nodeYOffset)

    
    nuke.selectAll()
    nuke.invertSelection()
    node = firstDot   
    #it craetes a temp lastDot node, to preserve the connected nodes, it then conencts itself to the output node and deletes itself... :)
    #node = lastDot 

    channels = node.channels()
    layers = list( set([c.split('.')[0] for c in channels]) )
    layers.sort()
    #print layers 
    
    createGrades = True # grades for Basic Layers
    processAO = True # process ambient occlusion
    processFA = True # fake atmosphere setup and connection
    showInputs = True # Hide lines of shuffles and remove dots above them


    basicLayers = [] #rawLight, diff, rawGI, spec, refl, selfIllum, sss
    rawLight_Layers = [] #rawLight broken out
    rawSpec_Layers = [] #spec broken out
    selectionLayers = [] #mattes
    xtex_Layers = [] #extra textures
    extraLayers = [] #all others

    splitRawLight = False
    splitRawSpec = False

    cryptomattes = False
    
    basicLayerTemplate = ['diffuse', 'rawGI', 'rawLight', 'reflect', 'specular']

    for layer in layers:
        ### Basic breakout
        if layer.lower() == 'diffuse':
            basicLayers.append(layer)
        if layer.lower() == 'rawgi':
            basicLayers.append(layer)
        if layer.lower() == 'rawlight':
            basicLayers.append(layer)
        if layer.lower() == 'reflect':
            basicLayers.append(layer)
        if layer.lower() == 'specular':
            basicLayers.append(layer)
        if layer.lower() == 'selfillum':
            basicLayers.append(layer)
        if layer.lower() == 'refract':
            basicLayers.append(layer)
        if layer.lower() == 'sss':
            basicLayers.append(layer)
            
        ### Selection breakout   
        if layer.lower() == 'matteshadow':
            selectionLayers.append(layer)
        if layer.lower() == 'ambocc':
            selectionLayers.append(layer)
        if layer.lower() == 'n':
            selectionLayers.append(layer)
        if 'normal' in layer.lower():
            selectionLayers.append(layer)
        if 'matte' in layer.lower():
            selectionLayers.append(layer)
        if 'materialid' in layer.lower():
            selectionLayers.append(layer)
        if layer.lower() == 'depth':
            selectionLayers.append(layer)
        if layer.lower() == 'zdepth':
            selectionLayers.append(layer)
        if layer.lower() == 'displacement':
            selectionLayers.append(layer)     
        if 'atmos' in layer.lower():
            selectionLayers.append(layer)
            
        ### RawLight breakout
        if 'raw_' in layer.lower() and '_spec' not in layer.lower():
            rawLight_Layers.append(layer)
            splitRawLight = True
        if 'rawlight_' in layer.lower():
            rawLight_Layers.append(layer)
            splitRawLight = True
        if 'light_raw' in layer.lower():
            rawLight_Layers.append(layer)
            splitRawLight = True
        if 'lightsel' in layer.lower():
            rawLight_Layers.append(layer)
            splitRawLight = True
        if 'lsel_' in layer.lower():
            rawLight_Layers.append(layer)
            splitRawLight = True
        if 'ls_' in layer.lower() and '_spec' not in layer.lower():
            rawLight_Layers.append(layer)
            splitRawLight = True
            

        ### Specular breakout  
        if '_specular' in layer.lower():
            rawSpec_Layers.append(layer)
            splitRawSpec = True    
        if 'specular_' in layer.lower():
            rawSpec_Layers.append(layer)
            splitRawSpec = True         
        if 'spec_' in layer.lower():
            rawSpec_Layers.append(layer)
            splitRawSpec = True  
        if '_spec' in layer.lower():
            rawSpec_Layers.append(layer)
            splitRawSpec = True  
            
        ### Extra Textures breakout
        if '_xtex' in layer.lower():
            xtex_Layers.append(layer)        
        if 'xtex_' in layer.lower():
            xtex_Layers.append(layer)
    
    basicLayers = list(set(basicLayers))
    rawLight_Layers = list(set(rawLight_Layers))
    rawSpec_Layers = list(set(rawSpec_Layers))
    selectionLayers = list(set(selectionLayers))
    
    #last item will be added first

    if 'matteShadow' in selectionLayers:
        selectionLayers.remove('matteShadow')
        selectionLayers.insert(0, 'matteShadow')
        
    if 'depth' in selectionLayers:
        selectionLayers.remove('depth')
        selectionLayers.insert(0, 'depth')
        
    if 'AmbOcc' in selectionLayers:
        selectionLayers.remove('AmbOcc')
        selectionLayers.insert(0, 'AmbOcc')
        
    if 'atmosphere' in selectionLayers:
        selectionLayers.remove('atmosphere')
        selectionLayers.insert(0, 'atmosphere')
        
        
        
    #selectionLayers.append('AmbOcc')

    xtex_Layers = list(set(xtex_Layers))
    extraLayers = list(set(layers) - set(basicLayers + rawLight_Layers+ rawSpec_Layers + selectionLayers +xtex_Layers))
    extraLayers = list(set(extraLayers))
    extraLayers.remove('rgba')
    
    basicLayersOrder= {'rawLight': 0, 'diffuse':1, 'rawGI': 2, 'SSS': 3, 'selfIllum':4, 'reflect':5, 'specular':6, 'refract':7}
    basicLayers = sorted(basicLayers, key=basicLayersOrder.__getitem__)
    
    ##Print out layer information
    def pr(a, b):
        if len(b)>0:
            print ""
            print str(a)+str(b)

    pr('All Layers: ', layers)
    pr('Basic Layers: ', basicLayers)
    pr('RawLight Layers: ', rawLight_Layers)
    pr('Specular Layers: ', rawSpec_Layers)
    pr('Selection Layers: ', selectionLayers)
    pr('Extra Textrue Layers: ', xtex_Layers)
    pr('Unexpected Layers: ', extraLayers)
    
    merges = []
    dotCount=0
    rsn = 0
    for i in rawSpec_Layers:
        rsn+=1

    ##basic nodes
    basicLayerNodes = []
    bln = 0
    blnLength = len(basicLayers)
    bnLastNode = None
    dots=[]
    shuffles=[]
    tempNode=node

    for layer in basicLayers:
        layerDot = nuke.createNode("Dot", inpanel=False)
        layerDot['ypos'].setValue(node['ypos'].value() + nodeYOffset * 0.5)
        layerDot['xpos'].setValue(node['xpos'].value() + (nodeXOffset*bln)+dot_offset)
        layerDot.setInput(0, tempNode)
        tempNode = layerDot
        dots.append(layerDot)
        
        shuf = nuke.createNode('Shuffle', inpanel=False)
        shuf['in'].setValue(layer)
        shuf['in2'].setValue('alpha')
        shuf['alpha'].setValue('red2')
        shuf['label'].setValue(layer)
        shuf['postage_stamp'].setValue(True)
        shuf['tile_color'].setValue(4234105727)
        shuf['ypos'].setValue(node['ypos'].value() + nodeYOffset)
        shuf['xpos'].setValue(node['xpos'].value() + (nodeXOffset*bln))
        basicLayerNodes.append(shuf)
        shuffles.append(shuf)
        shuf.setInput(0, layerDot)
        

        if shuf['label'].value()=='rawLight':
            '''
            rawLight_m = nuke.createNode("MergeExpression", inpanel=False)
            rawLight_m['expr0'].setValue('(((!isnan(Br/Ba))?Br/Ba:0)*((!isnan(Ar/Aa))?Ar/Aa:0))*Ba')
            rawLight_m['expr1'].setValue('(((!isnan(Bg/Ba))?Bg/Ba:0)*((!isnan(Ag/Aa))?Ag/Aa:0))*Ba')
            rawLight_m['expr2'].setValue('(((!isnan(Bb/Ba))?Bb/Ba:0)*((!isnan(Ab/Aa))?Ab/Aa:0))*Ba')
            rawLight_m['expr3'].setValue('Ba')
            '''
            rawLight_m = nuke.createNode("Merge2", "operation multiply", False)
            rawLight_m['output'].setValue('rgb')
            
            rawLight_m['xpos'].setValue(shuf['xpos'].value())
            rawLight_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*4)
            
            rawLight_s = shuf
            rawLight_m.setInput(1, shuf)
            #merges.append(rawLight_m)

        if shuf['label'].value()=='diffuse':
            diffuse_s=shuf
            diff_dot = nuke.createNode("Dot", inpanel=False)
            diff_dot.setInput(0, shuf)
            diff_dot['xpos'].setValue(shuf['xpos'].value()+ 35)
            diff_dot['ypos'].setValue(shuf['ypos'].value() + nodeYOffset*3.4)
            
            diffuse_m = nuke.createNode("Merge2", "operation plus", False)
            diffuse_m['xpos'].setValue(diffuse_s['xpos'].value())
            diffuse_m['ypos'].setValue(diffuse_s['ypos'].value()+nodeYOffset*4)

            merges.append(diffuse_m)
         
            diff_dot2 = nuke.createNode("Dot", inpanel=False)
            diff_dot2['xpos'].setValue(diffuse_m['xpos'].value()+35)
            diff_dot2['ypos'].setValue(diffuse_m['ypos'].value()+nodeYOffset)
            bnLastNode = diff_dot2


        if shuf['label'].value()=='rawGI':
            rawGI_s = shuf
            '''
            rawGI_m = nuke.createNode("MergeExpression", inpanel=False)
            rawGI_m['expr0'].setValue('(((!isnan(Br/Ba))?Br/Ba:0)*((!isnan(Ar/Aa))?Ar/Aa:0))*Ba')
            rawGI_m['expr1'].setValue('(((!isnan(Bg/Ba))?Bg/Ba:0)*((!isnan(Ag/Aa))?Ag/Aa:0))*Ba')
            rawGI_m['expr2'].setValue('(((!isnan(Bb/Ba))?Bb/Ba:0)*((!isnan(Ab/Aa))?Ab/Aa:0))*Ba')
            rawGI_m['expr3'].setValue('Ba')
            '''
            rawGI_m = nuke.createNode("Merge2", "operation multiply", False)
            rawGI_m['output'].setValue('rgb')
            
            rawGI_m['xpos'].setValue(shuf['xpos'].value())
            rawGI_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*4)
            rawGI_m.setInput(1, shuf)
            #merges.append(rawGI_m)

        if shuf['label'].value()=='SSS':
            sss_s = shuf
            sss_m = nuke.createNode("Merge2", "operation plus", False)
            sss_m['xpos'].setValue(shuf['xpos'].value())
            sss_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*5)
            sss_m.setInput(0, bnLastNode)
            sss_m.setInput(1, shuf)
            bnLastNode = sss_m
            merges.append(sss_m)
            
            
        if shuf['label'].value()=='refract':
            refract_s = shuf
            refract_m = nuke.createNode("Merge2", "operation plus", False)
            refract_m['xpos'].setValue(shuf['xpos'].value())
            refract_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*5)
            refract_m['disable'].setValue(True)
            refract_m.setInput(0, bnLastNode)
            refract_m.setInput(1, shuf)
            bnLastNode = refract_m
            merges.append(refract_m)

        if shuf['label'].value()=='reflect':
            reflect_s = shuf
            reflect_m = nuke.createNode("Merge2", "operation plus", False)
            reflect_m['xpos'].setValue(shuf['xpos'].value())
            reflect_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*5)
            reflect_m.setInput(0, bnLastNode)
            reflect_m.setInput(1, shuf)
            bnLastNode = reflect_m
            merges.append(reflect_m)
            
        if shuf['label'].value()=='specular':
            specular_s = shuf
            specular_m = nuke.createNode("Merge2", "operation plus", False)
            specular_m['xpos'].setValue(shuf['xpos'].value())
            specular_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*5)
            specular_m.setInput(0, bnLastNode)
            specular_m.setInput(1, shuf)
            bnLastNode = specular_m
            merges.append(specular_m)
            
        if shuf['label'].value()=='selfIllum':
            selfIllum_m = nuke.createNode("Merge2", "operation plus", False)
            selfIllum_m['xpos'].setValue(shuf['xpos'].value())
            selfIllum_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*5)
            selfIllum_m.setInput(0, bnLastNode)
            selfIllum_m.setInput(1, shuf)
            bnLastNode = selfIllum_m
            merges.append(selfIllum_m)
            selfIllum_s = shuf 

        bln+=1
        
    try:    
        rawLight_m.setInput(0, diff_dot)
    except:
        pass    
    try:    
        rawGI_m.setInput(0, diff_dot)
    except:
        pass    
    try:    
        diffuse_m.setInput(0, rawGI_m)
    except:
        pass    
    try:    
        diffuse_m.setInput(1, rawLight_m)
    except:
        pass    
        
    ##end of basic nodes
    
    
    
    ##SPECULAR LAYERS BREAKOUT
    ##
    rsnReverse = []
    if splitRawSpec == True:
        rsLastNode = None
        rsnLength=len(rawSpec_Layers)
        rsn = 0
        rsnXOffset = -900
        rsnYOffset = 0
        rs_merges=[]
        #rsDot = nuke.createNode("Dot", inpanel=False)
        #rsDot.setInput(0, node)
        #rsDot['ypos'].setValue(node['ypos'].value()+30)
        #rsDot['xpos'].setValue(node['xpos'].value() + (nodeXOffset)*blnLength)
        last_rsm = None
        for layer in rawSpec_Layers:

            
            #print layer
            shuf = nuke.createNode("Shuffle", inpanel=False)
            shuf['in'].setValue(layer)
            shuf['in2'].setValue('alpha')
            shuf['alpha'].setValue('red2')
            shuf['label'].setValue(layer)
            shuf['postage_stamp'].setValue(True)
            shuf['tile_color'].setValue(4292105727)
            shuf['ypos'].setValue(node['ypos'].value() + nodeYOffset)
            shuf['xpos'].setValue(node['xpos'].value() + nodeXOffset*(rsn+bln))
            shuffles.append(shuf)
            #shuf.setInput(0, rsDot)

            rsnReverse.append(shuf)
            
            layerDot = nuke.createNode("Dot", inpanel=False)
            layerDot['ypos'].setValue(shuf['ypos'].value() - nodeYOffset * 0.5)
            layerDot['xpos'].setValue(shuf['xpos'].value() + dot_offset)
            layerDot.setInput(0, tempNode)
            tempNode = layerDot
            rsnReverse.append(layerDot)
            dots.append(layerDot)
            
            #shuf.setInput(0, layerDot)
            
            rs_m=nuke.createNode("Merge2", "operation plus", False)
            rs_m.setInput(1, shuf)
            rs_m.setInput(0, last_rsm)
            #rs_m.setInput(0, None)
            merges.append(rs_m)
            rs_merges.append(rs_m)
            
            if last_rsm != None:
                #print last_rsm.name()
                #print rs_m.name()
                last_rsm.setInput(0, rs_m)
            last_rsm=rs_m
        
            
            rs_m['xpos'].setValue(shuf['xpos'].value())
            rs_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*1.5)
            rsnReverse.append(rs_m)
            
            rsLastNode = rs_m
            rsn+=1
            shuf.setInput(0, layerDot)
            
        #rsDot['xpos'].setValue(node['xpos'].value() + (nodeXOffset)*blnLength)
        
        #Reorder the merges

        
        #last_rsm_dot = nuke.createNode('Dot', inpanel=False)
        #last_rsm_dot.setInput(0, rsLastNode)
        #last_rsm_dot['ypos'].setValue(rsLastNode['ypos'].value()+nodeYOffset*0.25)
        #last_rsm_dot['xpos'].setValue(rsLastNode['xpos'].value()+dot_offset)
        
        if 'specular_s' in locals():
        
            rawSpec_switch = nuke.createNode("Merge2", "operation copy", False)
            rawSpec_switch['xpos'].setValue(specular_s['xpos'].value())
            rawSpec_switch['ypos'].setValue(rsLastNode['ypos'].value()+nodeYOffset*0.25)
            rawSpec_switch['output'].setValue('rgb')
            
            rawSpec_switch.setInput(1, rs_merges[0])
            rawSpec_switch.setInput(0, specular_s)
            
            rawSpec_switch['label'].setValue(rawSpec_switch.input(0)['label'].value())
            
            #specular_m.setInput(1, rawSpec_switch)
            
        last_rs_m = None
        rs_merges = reversed(rs_merges)

        for rs_merge in rs_merges:
            rs_merge.setInput(0, last_rs_m)
            #rs_merge.setInput(1,None)
            last_rs_m = rs_merge


        
        

        '''
        rawSpec_switch = nuke.createNode("Merge2", "operation copy", False)
        rawSpec_switch['xpos'].setValue(specular_s['xpos'].value())
        rawSpec_switch['ypos'].setValue(rsLastNode['ypos'].value()+nodeYOffset*0.25)
        rawSpec_switch['output'].setValue('rgb')
        
        rawSpec_switch.setInput(1, last_rsm_dot)
        rawSpec_switch.setInput(0, specular_s)
        rawSpec_switch['label'].setValue(rawSpec_switch.input(0)['label'].value())
        '''

        
        #mirrorNodes(rsnReverse, direction="x")
        

            
            
    ##end of rawSpec nodes

    ##SELECTION LAYERS BREAKOUT
    ##

    for layer in selectionLayers:

        if 'crypto' in layer.lower():

            cryptomattes = True

        else:
            layerDot = nuke.createNode("Dot", inpanel=False)
            layerDot['ypos'].setValue(node['ypos'].value() + nodeYOffset * 0.5)
            layerDot['xpos'].setValue(node['xpos'].value() + (nodeXOffset*(bln+rsn))+dot_offset)
            layerDot.setInput(0, tempNode)
            dots.append(layerDot)
            tempNode = layerDot

            shuf = nuke.createNode("Shuffle", inpanel=False)
            shuf['in'].setValue(layer)
            shuf['in2'].setValue('alpha')
            shuf['alpha'].setValue('red2')
            shuf['label'].setValue(layer)
            shuf['postage_stamp'].setValue(True)
            shuf['tile_color'].setValue(2475294719L)
            shuf['ypos'].setValue(node['ypos'].value() + nodeYOffset)
            shuf['xpos'].setValue(node['xpos'].value() + nodeXOffset*(bln+rsn))   
            shuf.setInput(0, layerDot) 
            shuffles.append(shuf)
            bln+=1
            

            if shuf['label'].value().lower()=='ambocc':
                ambOcc_s = shuf
                #shuf['alpha'].setValue('white')
                ambOcc_m = nuke.createNode("Merge2", "operation multiply", False)
                ambOcc_m['xpos'].setValue(shuf['xpos'].value())
                ambOcc_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*5)
                ambOcc_m.setInput(0, bnLastNode)
                ambOcc_m.setInput(1, shuf)
                ambOcc_m['disable'].setValue(True)
                
                #merges.append(ambOcc_m)

                white=nuke.createNode("Constant", inpanel=False)
                white['channels'].setValue('rgba')
                white['color'].setValue(1)
                white['xpos'].setValue(shuf['xpos'].value()+nodeXOffset*0.4)
                white['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*1.5)

                white_m = nuke.createNode("Merge2", inpanel=False)
                white_m['xpos'].setValue(shuf['xpos'].value())
                white_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*2.3)
                white_m['operation'].setValue('under')
                white_m.setInput(0, shuf)
                white_m.setInput(1, white)
                #print white_m.name()
                   
                bnLastNode = ambOcc_m   
                

            if shuf['label'].value().lower()=='depth':
                depth_s = shuf
                depth_m = nuke.createNode("Merge2", "operation plus", False)
                depth_m['xpos'].setValue(shuf['xpos'].value())
                depth_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*5)
                depth_m.setInput(0, bnLastNode)
                depth_m['disable'].setValue(True)
                depth_m.setInput(1, shuf)
                bnLastNode = depth_m
                merges.append(depth_m)
                
                depth_constant=nuke.createNode("Constant", inpanel=False)
                depth_constant['channels'].setValue('rgba')
                depth_constant['color'].setValue(1)
                depth_constant['xpos'].setValue(shuf['xpos'].value()+nodeXOffset*0.4)
                depth_constant['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*1.5)

                depthconst_m = nuke.createNode("Merge2", inpanel=False)
                depthconst_m['xpos'].setValue(shuf['xpos'].value())
                depthconst_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*2.3)
                depthconst_m['operation'].setValue('multiply')
                depthconst_m.setInput(0, shuf)
                depthconst_m.setInput(1, depth_constant)
                
            if shuf['label'].value().lower()=='atmosphere':
                atmos_s = shuf
                atmos_m = nuke.createNode("Merge2", "operation plus", False)
                atmos_m['xpos'].setValue(shuf['xpos'].value())
                atmos_m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*5)
                atmos_m.setInput(0, bnLastNode)
                atmos_m.setInput(1, shuf)
                bnLastNode = atmos_m
                merges.append(atmos_m)
                
              
    if cryptomattes:
        try:
            layerDot = nuke.createNode("Dot", inpanel=False)
            layerDot['ypos'].setValue(node['ypos'].value() + nodeYOffset * 0.5)
            layerDot['xpos'].setValue(node['xpos'].value() + (nodeXOffset*(bln+rsn))+dot_offset)
            layerDot.setInput(0, tempNode)
            dots.append(layerDot)
            tempNode = layerDot

            shuf = nuke.createNode("Cryptomatte", inpanel=False)
            shuf['ypos'].setValue(node['ypos'].value() + nodeYOffset)
            shuf['xpos'].setValue(node['xpos'].value() + nodeXOffset*(bln+rsn))   
            shuf.setInput(0, layerDot) 
            shuffles.append(shuf)
            bln+=1

        except RuntimeError:
            print 'Could not create Cryptomatte node.'
            pass


    ##end of selection nodes
    

    ##RAWLIGHT LAYERS BREAKOUT
    ##
    
    if splitRawLight == True:
        rlLastNode = None
        rlnLength=len(rawLight_Layers)
        rln = 0
        rlnXOffset = -300

        rlnYOffset = 0
        rl_dots = []

        for layer in rawLight_Layers:
            
            #print layer
            shuf = nuke.createNode('Shuffle', inpanel=False)
            shuf['in'].setValue(layer)
            shuf['in2'].setValue('alpha')
            shuf['alpha'].setValue('red2')
            shuf['label'].setValue(layer)
            shuf['postage_stamp'].setValue(True)
            shuf['tile_color'].setValue(4292105727)
            shuf['ypos'].setValue(node['ypos'].value() + nodeYOffset)
            shuf['xpos'].setValue(node['xpos'].value() - (nodeXOffset*rlnLength) + (nodeXOffset*rln))
            #shuf.setInput(0, rlDot)
            shuffles.append(shuf)

            unpremult = nuke.createNode('Unpremult', inpanel=False)
            unpremult['ypos'].setValue(node['ypos'].value() + nodeYOffset + (nodeYOffset/1.5))
            unpremult['xpos'].setValue(node['xpos'].value() - (nodeXOffset*rlnLength) + (nodeXOffset*rln))


            layerDot = nuke.createNode("Dot", inpanel=False)
            layerDot['ypos'].setValue(shuf['ypos'].value() - nodeYOffset * 0.5)
            layerDot['xpos'].setValue(shuf['xpos'].value() + dot_offset)
            try:
                layerDot.setInput(0, dots[0])
            except:
                layerDot.setInput(0, node)
            #tempNode = layerDot
            dots.append(layerDot)
            rl_dots.append(layerDot)



            m=nuke.createNode("Merge2", "operation plus", False)
            m.setInput(1, unpremult)
            m.setInput(0, rlLastNode)
            merges.append(m)
            #['xpos'].setValue(shuf['xpos'].value())
            m['xpos'].setValue(shuf['xpos'].value())
            m['ypos'].setValue(shuf['ypos'].value()+nodeYOffset*1.5)

            rlLastNode = m
            rln+=1
            shuf.setInput(0, layerDot)
            
        #rlDot['xpos'].setValue(node['xpos'].value() - (nodeXOffset/2)*rlnLength)
        if 'rawLight_s' in locals():
            rawLight_switch = nuke.createNode("Merge2", "operation copy", False)
            rawLight_switch['ypos'].setValue(rlLastNode['ypos'].value())
            rawLight_switch['output'].setValue('rgb')
            rawLight_switch.setInput(1, rlLastNode)
            rawLight_switch.setInput(0, rawLight_s)
            rawLight_m.setInput(1, rawLight_switch)
            rawLight_switch['label'].setValue(rawLight_switch.input(0)['label'].value())
        
        #reverse the dot order and connection
        try:
            last_rl_dot = dots[0]
        except:
            last_rl_dot = node
        rl_dots=reversed(rl_dots)
        
        for dot in rl_dots:
            dot.setInput(0, last_rl_dot)
            last_rl_dot = dot
            

    ##end of rawLight nodes


    ##EXTRA TEXTURES BREAKOUT
    ##
    nuke.selectAll()
    nuke.invertSelection()
    for layer in xtex_Layers:
        layerDot = nuke.createNode("Dot", inpanel=False)
        layerDot['ypos'].setValue(node['ypos'].value() + nodeYOffset * 0.5)
        layerDot['xpos'].setValue(node['xpos'].value() + (nodeXOffset*(bln+rsn))+dot_offset)
        dots.append(layerDot)
        layerDot.setInput(0, tempNode)
        tempNode = layerDot
        
        shuf = nuke.createNode('Shuffle', inpanel=False)
        shuf['in'].setValue(layer)
        shuf['in2'].setValue('alpha')
        shuf['alpha'].setValue('red2')
        shuf['label'].setValue(layer)
        shuf['postage_stamp'].setValue(True)
        shuf['tile_color'].setValue(2190700799)
        shuf['ypos'].setValue(node['ypos'].value() + nodeYOffset)
        shuf['xpos'].setValue(node['xpos'].value() + nodeXOffset*(bln+rsn))   
        shuf.setInput(0, layerDot)
        shuffles.append(shuf) 
        bln+=1
    
    ##end of extra layers


    ##EXTRA LAYERS BREAKOUT
    ##
    nuke.selectAll()
    nuke.invertSelection()
    for layer in extraLayers:
        layerDot = nuke.createNode("Dot", inpanel=False)
        layerDot['ypos'].setValue(node['ypos'].value() + nodeYOffset * 0.5)
        layerDot['xpos'].setValue(node['xpos'].value() + (nodeXOffset*(bln+rsn))+dot_offset)
        layerDot.setInput(0, tempNode)
        dots.append(layerDot)
        tempNode = layerDot
        
        shuf = nuke.createNode('Shuffle', inpanel=False)
        shuf['in'].setValue(layer)
        shuf['in2'].setValue('alpha')
        shuf['alpha'].setValue('red2')
        shuf['label'].setValue(layer)
        shuf['postage_stamp'].setValue(True)
        shuf['tile_color'].setValue(2384272895)
        shuf['ypos'].setValue(node['ypos'].value() + nodeYOffset)
        shuf['xpos'].setValue(node['xpos'].value() + nodeXOffset*(bln+rsn))   
        shuf.setInput(0, layerDot)
        shuffles.append(shuf) 
        bln+=1
    
    ##end of extra layers     

    for merge in merges:
        merge['Achannels'].setValue('rgb')
        
    
    if splitRawSpec == True:
        try:
            specular_m.setInput(1, rawSpec_switch)
        except:
            pass
        
        
        
    nuke.selectAll()
    nuke.invertSelection()
    
    for node in basicLayerNodes:
        node['selected'].setValue(True)
        
        if splitRawLight == True:
            if node['label'].value().lower()=='rawlight':
                node['selected'].setValue(False)
                rawLight_switch['selected'].setValue(True)
        if splitRawSpec == True:
            if 'spec' in node['label'].value().lower():
                node['selected'].setValue(False)
                rawSpec_switch['selected'].setValue(True)
        
    gradeNodes=[]
    connectionNodes = nuke.selectedNodes()
    nuke.selectAll()
    nuke.invertSelection()

    for i in connectionNodes:
        i['selected'].setValue(True)
        g = nuke.createNode("Grade", inpanel=False)
        g['xpos'].setValue(i['xpos'].value())
        g['ypos'].setValue(node['ypos'].value()+nodeYOffset*2.1)
        g['unpremult'].setValue('rgba.alpha')
        gradeNodes.append(g)
        nuke.selectAll()
        nuke.invertSelection()

    o = None
    if bnLastNode != None:
        o = nuke.createNode("Output", inpanel=False)
        o.setInput(0, bnLastNode)
        o['xpos'].setValue(bnLastNode['xpos'].value())
        o['ypos'].setValue(bnLastNode['ypos'].value()+200)

        lastDot.setInput(0,o)
        nuke.delete(lastDot)

    
    firstDot['xpos'].setValue(firstDot['xpos'].value()+dot_offset)
    


    if showInputs == False:
        for shuf in shuffles:
            shuf['hide_input'].setValue(True)
        for dot in dots:
            nuke.delete(dot)

    ##:(
    try:
        ambOcc_m.setInput(1, white_m)
    except:
        pass 
    try:
        depth_m.setInput(1, depthconst_m)
    except:
        pass


    return o

