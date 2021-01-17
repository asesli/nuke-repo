import re
import importAssets
import nuke


def replacePattern(string, pattern, replace):
    #removes the result of first pattern from the string
    #removePattern('some string for sure', r"(\d{3})")
    _pattern = re.compile(pattern, re.I)
    _match = _pattern.search(string)
    try:
        _match = _match.group()
        _match = string.replace(_match,replace)
        return _match
    except AttributeError:
        return ''

def grabPattern(string, pattern):
    #returns the first matching pattern group in string
    #grabPattern('some string for sure', r"(\d{3})")
    _pattern = re.compile(pattern, re.I)
    _match = _pattern.search(string)
    try:
        _match = _match.group()
        return _match
    except AttributeError:
        return ''
    
def removePattern(string, pattern):
    #removes the result of first pattern from the string
    #removePattern('some string for sure', r"(\d{3})")
    _pattern = re.compile(pattern, re.I)
    _match = _pattern.search(string)

    try:
        _match = _match.group()
        _match = string.replace(_match,'')
        return _match

    except AttributeError:
        return ''

def matchgrade_setup(outfile,plate,cutref):
    
    nuke.nodePaste("//qumulo/Libraries/HAL/LIVEAPPS/apps/Scripts/NUKE/scripts/MatchCutref.nk")

    for i in nuke.selectedNodes('MatchGrade'):
        i['outfile'].setValue(outfile)

    for i in nuke.selectedNodes('Dot'):
        if i['label'].value().lower() == 'plate':
            i.setInput(0,plate)
            plate['xpos'].setValue(i['xpos'].value() - plate.screenWidth()/2)
            plate['ypos'].setValue(i['ypos'].value() - plate.screenHeight()*2)
            
        if i['label'].value().lower() == 'cutref':
            i.setInput(0,cutref)
            cutref['xpos'].setValue(i['xpos'].value() - cutref.screenWidth()/2)
            cutref['ypos'].setValue(i['ypos'].value() - cutref.screenHeight()*2)
            
    
    nuke.selectAll()
    nuke.invertSelection()

def matchCutref():

    orig_sel = nuke.selectedNodes('Read')
    


    if len(orig_sel) < 1:
        
        nk_file = nuke.Root().name() #Q:/Impulse/IMP210/05_COMP/IMP210_017_070/IMP210_017_070_Comp_V002.nk
        if nk_file == 'Root':
            nuke.message('Untitled script. You can only run this command inside of a shot script. Or you must select a plate to run this on.')
            return
        shot_name = nk_file.split('/')[-2] #IMP210_017_070
        precomp_lut_dir = '/'.join(nk_file.split('/')[0:-1])+'/02_OUTPUT/01_precomp/'+shot_name+'_LUT.csp'
        print 'Creating matchgrade template based on nuke file name : {0}'.format(shot_name) 
        try:
            c = importAssets.ImportAssets().importCutrefs()[-1]
        except TypeError:
            nuke.message('Could not find a cutref for this shot.')
            c = nuke.createNode('NoOp', inpanel=False)  
            c.setSelected(False)
        try:
            p = importAssets.ImportAssets().importPlates()[0]
        except TypeError:
            nuke.message('Could not find a plate for this shot.')
            p = nuke.createNode('NoOp', inpanel=False)  
            p.setSelected(False)
        matchgrade_setup(precomp_lut_dir,p,c)

    else:
        for p in orig_sel:
            
            plate_file = p['file'].value() #Q:/Impulse/IMP210/01_PLATES/IMP210_017_070/PLATE/PLATE_O/01_EXRS/IMP210_017_070.####.exr
            proj_plate_dir = grabPattern(plate_file, r".*/01_PLATES/")
            shot_plate_dir = grabPattern(plate_file, r".*/01_PLATES/(\w)*/")
            if shot_plate_dir == '':
                nuke.message('Are you sure the selected node is EXR/DPX plate inside the 01_PLATES directory?')
                return
            shot_comp_dir = shot_plate_dir.replace('01_PLATES', '05_COMP')
            shot_name = shot_comp_dir.split('/')[-2]
            precomp_lut_dir = shot_comp_dir + '/02_OUTPUT/01_precomp/' + shot_name + '_LUT.csp'
            plate_file = plate_file.replace('01_PLATES', '05_COMP')
            plate_file = '/'.join(plate_file.split('/')[0::-1])
            
            print 'Creating matchgrade template based on selected read node : {0}'.format(shot_name)

            try:
                c = importAssets.ImportAssets().importCutrefs()[-1]
            except TypeError:
                nuke.message('Could not find a cutref for this shot.')
                c = nuke.createNode('NoOp', inpanel=False)  
                c.setSelected(False)

            nuke.selectAll()
            nuke.invertSelection()
            p.setSelected(True)
            matchgrade_setup(precomp_lut_dir, p, c)
