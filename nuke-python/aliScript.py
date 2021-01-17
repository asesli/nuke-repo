import nuke
import sys
import os


#####################################################################
###########    IMPORT READ NODE FROM WRITE      #####################
#####################################################################
#sets framerange to project frame range if path cant be found (or if it hasnt finished rendering)
#it will find the frame range automatically
def importPath():

    # Nuke frame range fixer
    # Select read nodes and run the script. It will find the starting and ending frame in the sequence (if exist), and set the frame range to it. 
    # (It skips other type of nodes, so you may select other types too)
    # FORMAT : .../AX1_020_001-cg_fx_v008_cow_beauty.####.ext
    # by Gabor L. Toth (gltoth@gmail.com)

    import nuke
    import os
    import os.path
    import math
    import glob
    import re
    
    def  glt_reloadRange():
        sn = [n for n in nuke.selectedNodes() if n.Class() == "Read"]
        
        if sn != []:
            for n in sn:
                seqPath = n.knob('file').value()                            #'AUH_010_001-cg_li_v002_H1BodyRL.beauty.%04d.iff'
                if seqPath is not None and re.match('.*\.%0.*', seqPath):
                    indx = seqPath.find('%0')                                       # getting padding format
                    pattern = '%0' + seqPath[indx + 2] + 'd'
                    seqPathMask = seqPath.replace(pattern, '*')    # replacing %04d    'AUH_010_001-cg_li_v002_H1BodyRL.beauty.*.iff'
                    print ''
                    print 'PathMask: %s' % (seqPathMask)
                    seqDir = os.path.dirname(seqPath)
                    print 'Directory: %s' % (seqDir)
                    if os.path.exists(seqDir):
                        files = os.listdir(seqDir)
                        #print files 
                #sorting files
                        filteredFiles = glob.glob(seqPathMask)
                        filteredFiles.sort()
                        if len(filteredFiles) != 0:
                            (firstFileName, ext) = os.path.splitext(filteredFiles[0])
                            firstFileTags =  firstFileName.split('.')
                            sfs = firstFileTags[-1]
                            #print 'Extension: ' + ext 
                            sf = int (sfs)    # converted to int
                            #print "Start frame: %s" % (sf)
                            (lastFileName, ext) = os.path.splitext(filteredFiles[len(filteredFiles)-1])
                            lastFileTags =  lastFileName.split('.')
                            efs = lastFileTags[-1]    
                            ef = int (efs)
                            #print "End frame: %s" % (ef)
                            n.knob('first').setValue(sf)
                            n.knob('last').setValue(ef)
                            return True
                        else:
                            print 'No matching files in this directory! Skipping...'
                            return False
                    else:
                        print 'Warning! Directory doesnt exist: ' + seqDir 
                        return False
                else:
                    pass
                    return False
        else:
            pass
            return False 

    def create_reads(_from):

        read = nuke.createNode('Read')
        read['file'].setValue(_from['file'].value())
        if 'default' in _from['colorspace'].value():
            read['colorspace'].setValue(0)
        else:
            read['colorspace'].setValue(_from['colorspace'].value())
        try: 
            read['raw'].setValue(_from['raw'].value())
        except:
            pass
        nuke.selectAll() 
        nuke.invertSelection() 
        read['selected'].setValue(True)
        if(glt_reloadRange() is not True):
            read['first'].setValue(int(nuke.Root().knob('first_frame').value()))
            read['last'].setValue(int(nuke.Root().knob('last_frame').value()))


    def get_reads(): # processes groups / writes / lux_writes
        for i in nuke.selectedNodes():
            if i.Class() == 'Group':
                if i.knob('discipline') and i.knob('getShotPath'):
                    with i:
                        for w in nuke.selectedNodes():
                            if w.Class() == 'Write' or 'ReadGeo' or 'Read':
                                with nuke.Root():

                                    create_reads(w)
                            else:
                                pass 
                            

            elif i.Class() == 'Write' or 'ReadGeo' or 'Read':

                create_reads(i)

            else:
                pass      
    get_reads()
        
###########################################################
#########   UNPREMULT BY ALPHA IF KNOB EXISTS    ##########
###########################################################
#Unpremultiplies a node with 'unpremult' parameter by 'rgba.alpha'
        
def alphaUnpremult():
    for i in nuke.selectedNodes():
        if i.knob('unpremult'):
            if i['unpremult'].value()=='alpha':
                i['unpremult'].setValue('none')
            else:
                i['unpremult'].setValue('alpha')

                
###########################################################
########   SET BBOX TO B INPUT IF KNOB EXISTS    ##########
###########################################################
#Unpremultiplies a node with 'unpremult' parameter by 'rgba.alpha'                
def bbox_B():
    for i in nuke.selectedNodes():
        if i.knob('bbox'):
            i.knob('bbox').setValue('B')
            
###########################################################
###########   Create a Write for RotoFrames    ############
###########################################################     
def rotoFrameWrite():
    '''
    for i in nuke.selectedNodes():
        ext = 'jpg'
        shotLocalDest = '/03_COORDINATION/RotoFrames/'

        shot = i['file'].value().split('/')[-1].split('.')[0]
        seq = shot.split('_')[0]
        dest = str( i['file'].value().split(seq)[0] ) + str(seq) + shotLocalDest
        
        filePath = dest +  shot + '.%04d.' + ext

        rotoWrite = nuke.createNode('Write', inpanel = False)
         
        rotoWrite['file'].setValue(filePath)
        rotoWrite.setInput(0,i)
    '''
    for r in nuke.selectedNodes('Read'):
        shot_name = r['file'].value().split('/')[-1].split('.')[0]
        shot_name = shot_name.upper().split('_V')[0]
        roto_dir = r['file'].value().upper().split(shot_name)[0]
        roto_dir = '/'.join(roto_dir.split('/')[0:-2])
        roto_dir = roto_dir + '/03_COORDINATION/'
        roto_dir = roto_dir + 'RotoFrames/'
        roto_frame = roto_dir + shot_name + '.%04d.jpeg'
        

        w = nuke.createNode('Write')
        w.setInput(0, r)
        w['file'].setValue(roto_frame)
        

###########################################################
#####################   Get Paths    ######################
###########################################################     


def get_file_paths():
    a = []
    for i in nuke.allNodes():

        try:
            #print i['file'].value()
            a.append(i['file'].value())
        except:
            pass

    a = '\n'.join(a)
    nuke.message(a)

###########################################################
####   Import Jpeg Counterparts of Selected Plates    #####
###########################################################     

def import_jpegs_from_selected():
    for i in nuke.selectedNodes():
        if 'file' in i.knobs():
            full_res_jpeg = i['file'].value()
            full_res_jpeg = full_res_jpeg.replace('.exr', '.jpeg')
            full_res_jpeg = full_res_jpeg.replace('.EXR', '.JPEG')
            full_res_jpeg = full_res_jpeg.replace('01_EXRS', '02_FULL_RES_JPEGS')
            r = nuke.createNode('Read')
            r['file'].setValue(full_res_jpeg)
            r['first'].setValue(i['first'].value())
            r['last'].setValue(i['last'].value())
            

