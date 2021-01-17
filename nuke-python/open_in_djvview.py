import subprocess
import nuke

def get_img_seq_from_selected_node():

    image_asset = ''
    try:
        selectedNode = nuke.selectedNode()
    except:
        nuke.message('Select Write, Read, or Lux Write node and try again')
        return

    if selectedNode.Class() == 'Group':
        if 'luxwrite' in selectedNode.knobs():
            print 'lx write'
            file_knobs = [k for k in selectedNode.knobs().keys() if 'file_writecode' in k ] 
            #print file_knobs
            img_seq_found = False
            while not img_seq_found:
                for i in file_knobs:
                    if selectedNode[i].value().split('.')[-1].lower() in ['jpeg', 'jpg']: 
                        image_asset = selectedNode[i].value()
                        img_seq_found =True
                break
            if not img_seq_found:
                
                image_asset = selectedNode[file_knobs[0]].value()
    
    elif selectedNode.Class() in ['Write', 'Read']:
        image_asset = nuke.selectedNode()['file'].value()
    
    else:
        nuke.message('Select Write, Read, or Lux Write node and try again')
        return None
    
    image_asset = image_asset.replace('%04d','0000')
    
    
    return image_asset

def launch_with_DJVView(*file):
    if file:
        file = file[0]
    else:
        file = get_img_seq_from_selected_node()

    exe = '"C:/Program Files/djv-1.1.0-Windows-64/bin/djv_view.exe"'
    
    if file is not None:
        print file
        args = exe + ' ' + file
        subprocess.Popen(args, shell=False)
        return

    #launch_with_DJVView()