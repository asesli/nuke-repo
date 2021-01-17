import os
import sys
import nuke

#Opens the discipline directory in Win Explorer
#if no applicable node is selected, it will open it up for the current shot.

#WIP: proper error handling

#F2: open comp dir
#F3: open renders dir
#F4: open plates dir

#Alican Sesli 02.14.17

def _browse(_path): 
    browse_dir = _path
    platform = sys.platform

    if platform == 'darwin':
        os.system('open %s' % browse_dir)

    if platform == 'linux2':
        os.system('nautilus %s' % browse_dir)

    if platform == 'win32':
        browse_dir = browse_dir.replace('/', '\\')
        os.system('explorer %s' % browse_dir)




def browseDiscipline(_discipline):
    
    discipline = _discipline.upper()
    try: #if a node is selected with a file path knob, it will treat that node as the asset and derrive the path parameter from nodes settings. 
        if nuke.selectedNode():
            sn = nuke.selectedNode()
            if sn.knob('file'):
                rootDir = sn['file'].value()
                disciplines = ['01_PLATES', '02_INPUT', '03_COORDINATION', '04_3D', '05_COMP', '06_RENDERS', '07_DAILIES', '08_PFTrack', '09_QT']
                for disc in disciplines:
                    if disc in rootDir:
                        tempDir = rootDir.split(disc)
                        rootDir = tempDir[0]
                        shotName = tempDir[-1].split('/')[1]
                        path = os.path.join(rootDir, discipline, shotName)

    except ValueError: #if no node is selected treat script name as the asset
        try:
            scriptName = nuke.Root().name()
            shotName = scriptName.split('/')[-2]
            rootDir = '/'.join(scriptName.split('/')[0:-3])
            path = os.path.join(rootDir, discipline, shotName)

        except IndexError: #if no node is selected and the script is not saved properly
            nuke.message('Could not find the requested directory; Make sure your script is saved inside of the COMP directory.')
            pass


    try: #adds a FINL folder if discipline is set to RENDERS
        if 'RENDERS' in str(discipline):
            path = os.path.join(path, 'FINL')
        _browse(path)

    except UnboundLocalError: #if the previous exceptions are not met, the path parameter becomes unrefferenced, so this kills it if no conditions are met.
        pass


def browseDir():
    if nuke.selectedNodes():
        try:
            node = nuke.selectedNode()
            if node.Class()=='Group':
                if node.knob('main_dir'):
                    path = os.path.dirname(node.knob('main_dir').value())
            else:
                path = os.path.dirname(node.knob('file').value())
        except:
            msg = 'No node with "file" knob selected'
            #nuke.message(msg)
            print msg
            return
    else:
        path = nuke.root().name().split( os.path.basename( nuke.root().name() ) )[0]

    _browse(path)