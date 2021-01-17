##Contact Sheet Namer
##Select your contact sheet and execute contactSheetNamer() from this script.
## It will add a text node for the shot name and version before each input of the contact sheet.
## It will add a controller node where the artist can change the properties of all text nodes.


import nuke

def contactSheetNamer():
    #select ContactSheet node and execute following code
    try:
        if nuke.selectedNode().Class()=='ContactSheet':
            
            contactSheet = nuke.selectedNode()
            
            contactSheet.knob('selected').setValue(True) 
            readNodes = []
            connectedNodes = []
            textNodes = []
            
            #user controls
            offsetX = -10
            offsetY = 10
            prefix = 'CS_Text_'
            controlName = 'Control_Node_0'
            showVersion = False
            fontSize = 70
            
            #create control  node

            control = nuke.createNode('NoOp', inpanel=False)
            control.setInput(0, contactSheet)
            controlNode = control

            n = nuke.Double_Knob("fontSize") 
            control.addKnob(n)
            control[n.name()].setValue(50)

            '''
            n = nuke.Enumeration_Knob("justifyX", "justifyX" , ['left', 'center', 'right', 'justify']) 
            control.addKnob(n) 
            control[n.name()].setValue(2)

            n = nuke.Enumeration_Knob("justifyX", "justifyX" , ['baseline', 'top', 'center', 'bottom']) 
            control.addKnob(n) 
            control[n.name()].setValue(3)
            '''

            n = nuke.XY_Knob("translate")
            control.addKnob(n)
            control[n.name()].setValue(offsetX, 0)
            control[n.name()].setValue(offsetY, 1)
            
            n = nuke.Double_Knob("kerning") 
            control.addKnob(n)
            control[n.name()].setValue(0)

            n = nuke.Double_Knob("leading") 
            control.addKnob(n)
            control[n.name()].setValue(0)
            ########

            
            #find all read nodes
            def climb(node):
                for n in node.dependencies():
                    climb(n)
                    if(n.Class()=="Read"):
                        readNodes.append(n.name())
            climb(contactSheet)
            
            #delete existing text/control nodes
            def deleteExisting():
                for i in readNodes:
                    deleteName = prefix+i
                    nuke.delete(nuke.toNode(deleteName))
            deleteExisting()    
            
            
            
            #find all nodes that is directly connected to contactSheet
            for x in contactSheet.dependencies():
                connectedNodes.append(x.name())
            
            #creates text nodes everytime a read node is found
            for i in readNodes:
            
                index = readNodes.index(i)
                a =  readNodes[index] #read nodes @ index
                b =  connectedNodes [index] #connected nodes @ index
                
                
                nuke.toNode(i)['before'].setValue('loop')
                nuke.toNode(i)['after'].setValue('loop')
            
                textNode = nuke.createNode('Text', inpanel=False)
                textNode.setName(prefix+i)
                textNode.setInput(0, nuke.toNode(b))
            
                textNode['xjustify'].setValue(2)
                textNode['yjustify'].setValue(3)

                textNode['translate'].setValue(offsetX, 0)
                textNode['translate'].setValue(offsetY, 1)
                textNode['box'].setValue(0,0)
                textNode['box'].setValue(0,1)
                textNode['box'].setValue(textNode.input(0).width(),2)
                textNode['box'].setValue(textNode.input(0).height(),3)
                textNode['size'].setValue(fontSize)

                justifyXExp = "parent."+controlNode.name()+".justifyX"
                justifyYExp = "parent."+controlNode.name()+".justifyY"
                textSizeExp = "parent."+controlNode.name()+".fontSize"
                translateXExp = "parent."+controlNode.name()+".translate.x"
                translateYExp = "parent."+controlNode.name()+".translate.y"
                kerningExp = "parent."+controlNode.name()+".kerning"
                leadingExp = "parent."+controlNode.name()+".leading"

                textNode['kerning'].setExpression(kerningExp)
                textNode['leading'].setExpression(leadingExp)
            
                textNode['size'].setExpression(textSizeExp)
                #textNode['xjustify'].setExpression(justifyXExp)
                #textNode['yjustify'].setExpression(justifyYExp)
                
                textNode['translate'].setExpression(translateXExp, 0)
                textNode['translate'].setExpression(translateYExp, 1)

                textNodes.append(textNode.name())
            
                t_readNode = nuke.toNode(i)
                t_filePath = t_readNode['file'].value()
                t_fullShotName = t_filePath.split('/')[-1]
                t_shotName= t_fullShotName.split('.')[0]
                t_version = t_shotName.split('_')[-1]
                t_splits = t_shotName.split('_')
                index = readNodes.index(i) 
                t_message = ""
            
                #show version or not
                for n in t_splits:
                    t_shotNameVersion = '_'.join(t_splits)
                if (showVersion):
                    t_message = t_shotNameVersion
                elif (not showVersion):
                    t_message = t_shotNameVersion
                textNode['message'].setValue(t_message) 
            
                
            #connect contactSheet to newly created nodes
            for i in textNodes:
                ind = textNodes.index(i)
                contactSheet.setInput(ind, nuke.toNode(i))

        else:
            nuke.message('ContactSheet node must be selected!')
    except:
        nuke.message('ContactSheet node must be selected!')