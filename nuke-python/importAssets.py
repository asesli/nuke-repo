'''
LUX Visual Effects Inc., Alican Sesli (c) 2020
Initializer script for nuke
'''

import nuke
import os
import re
import getpass
import autoBackdrop
import versionUp

'''ImportAssets class contains many functions to auto populate nuke scripts from associated paths related to the given shot.. 
It is flexible enough to get all data from either a selected node, or from the nuke script itself. Internal functions have overrides as well.
'''

class ImportAssets:

    def __init__(self):

        self.image_types = ['exr', 'jpeg', 'jpg', 'dpx', 'tga', 'targa', 'png']
        self.file_knob_names = ['file', 'main_dir']
        self.plate_reformat_settings = ['','','HALF_HD']

        self.re_shotcode =  r"([a-z]{2,6}(\d{0,3})*_(\d{3}[a-z]{0,2}|[a-z]{3})_\d{3}[a-z]{0,2}([^\_\W])*)" #BEY101_010A_270
        self.re_departments = r"(/\d{2}_[a-z]{2,8}/)" #/01_PLATES/
        self.re_version_tag = r"(_v\d{3})"
        #self.re_sequence_build = r"((^|\r?\n|.*_|.*\.)\d{3,}.*\.[a-z]{3})"
        #self.shotcode = self.getShotCode()

        #project defaults
        self.first_frame = 1
        self.last_frame = 100
        self.width = 640
        self.height = 480 
        self.padding = 4
        self.untitledScriptPath = 'Q:/UnsortedProjects/{}/'.format(getpass.getuser())


    # Functions to retrieve paths

    def getPath(self, *node):
        #Returns a path based on whats selected, if nothing is selected it will retrieve it from script name
        #path = nuke.root()['name'].value()

        path = nuke.root()['name'].value()
        file_knob = None
        if node:
            n = node[0]
            file_knob = [k for k in n.knobs() if k in self.file_knob_names]

        else:
            if len(nuke.selectedNodes()) > 0:
                
                for n in nuke.selectedNodes():

                    file_knob = [k for k in n.knobs() if k in self.file_knob_names]

        if file_knob:
            file_knob_val = n[file_knob[0]].value()
            grab_shotcode = self.grabPattern(file_knob_val, self.re_shotcode)
            if grab_shotcode:
                return file_knob_val 

        return path

    def getRootPath(self, *path):
        '''Retrieves a root path from a path that has a shot code structure
        returns a path, path ends with / eg Omens/OMS101/05_COMP/OMS101_001_010/
        '''
        if not path:
            path = self.getPath()
        else:
            path=path[0]
        _grab = self.grabPattern(path, self.re_shotcode+r'/')
        if _grab:
            root_path = path.split(_grab)[0] + _grab
            return root_path

    def getSubfolders(self, path):
        #Retrieves full path of nested subfolders
        #Returns a list of full path to all subfolders
        subfolders = [x[0].replace('\\','/')+'/' for x in os.walk(path)]

        return subfolders

    def getSequences(self, path):
        #imports all image sequences inside a folder
        #returns a list of dicts to poulate a read node
        seqs = nuke.getFileNameList(path)
        valid_seqs = []
        for i in seqs:
            i = i.replace(".#.", ".####.")
            i = i.replace(".%04d.", ".####.")
            if self.grabPattern(i, r"(\.#{3,}\.[a-z]{3,5} \d{1,}-\d{1,})"):

                if self.grabPattern(i, r"(\.[a-z]{3,5})").replace('.','') in self.image_types:
                    name = i.split(' ')[0] 
                    frames = i.split(' ')[1].split('-')
                    seq_element = {'file' : path + name , 'first' : frames[0] , 'last' : frames[-1]}
                    valid_seqs.append(seq_element)

        #get rid of old versions by cross comparing names + versions



        return valid_seqs

    def getPlatesDirectory(self, *path):
        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

        plates_dir = self.replacePattern(path, self.re_departments, '/01_PLATES/')
        #print path
        split_dir = plates_dir.split('/01_PLATES/')
        shot = split_dir[-1].split('/')[0]
        plates_dir = split_dir[0] + '/01_PLATES/' + shot + '/'

        if not os.path.isdir(plates_dir):
            return None

        plates_dirs = self.getSubfolders(plates_dir)

        raw_dirs =  [x for x in plates_dirs if (('01_exrs' in x.lower() ) or ('01_dpxs' in x.lower() )) ]
        jpg_dirs =  [x for x in plates_dirs if '02_full_res_jpegs' in x.lower()]

        return raw_dirs

    def getCompDirectory(self, *path):

        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

        comp_dir = self.replacePattern(path, self.re_departments, '/05_COMP/')
        #print path
        split_dir = comp_dir.split('/05_COMP/')

        shot = split_dir[-1].split('/')[0]
        
        comp_dir = split_dir[0] + '/05_COMP/' + shot + '/02_OUTPUT/03_comp/'

        if not os.path.isdir(comp_dir):
            return None

        return comp_dir

        #comp_dirs = self.getSubfolders(comp_dir)

        #raw_dirs =  [x for x in comp_dirs if (('01_exrs' in x.lower() ) or ('01_dpxs' in x.lower() )) ]
        #jpg_dirs =  [x for x in comp_dirs if '02_full_res_jpegs' in x.lower()]

        #return raw_dirs

    def getLatestNk(self, *path):

        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

        comp_out = self.getCompDirectory(path)

        comp_dir = comp_out.replace("02_OUTPUT/03_comp/","")

        shot_name = self.getShotCode(path)

        comp_files = [i for i in os.listdir(comp_dir) if (i[-3::]=='.nk') and (shot_name+'_Comp_' in i)]

        #comp_files = sorted(comp_files, reverse=True)

        comp_files = sorted(comp_files, key=lambda s: s.lower(), reverse=True)

        latest = comp_dir + comp_files[0]

        #print latest

        return latest

    def pathsFromShotCode(self, shotcode):
        #Returns a list of all associated paths from shotcode
        return

    def dirname(self, path):
        #same as os.path.dirname() but with / at end
        return os.path.dirname(path)+'/'

    def basename(self, path):
        #same as os.path.basename()
        return os.path.basename(path)

    def getDepartmentDirectory(self, department, *path):
        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

        dept_dir = self.replacePattern(path, self.re_departments, '/{}/'.format(department))
        split_dir = dept_dir.split('/{}/'.format(department))
        shot = split_dir[-1].split('/')[0]

        path = '{}/{}/{}/'.format(split_dir[0],department,shot)

        return path

    def getLatestThumbnail(self, *path):

        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

        thumb_path = self.getDepartmentDirectory("03_COORDINATION", path)
        thumb_path = '/'.join(thumb_path.split('/')[:-2])+'/_thumbs/'
        shot_code = self.getShotCode(path)
        try:
            thumbs = [thumb_path+i for i in os.listdir(thumb_path) if shot_code in i]
            thumbs = sorted(thumbs)
            thumbs = thumbs[-1]
        except:
            thumbs = ''

        return thumbs

    # Node creation functions to populate nuke scripts

    def createRead(self, dct):
        #creates a read node using the information from dict
        #returns a read node

        r_first = dct.get('first')
        r_last = dct.get('last')
        r_path = dct.get('file')
        r_label = dct.get('label')
        r_color = dct.get('tile_color')
        if r_label == None:
            r_label = ''
        #r_color = 0

        if all(v is not None for v in [r_first, r_last, r_path, r_label]):

            readnode = nuke.createNode('Read', inpanel=False)
            readnode['file'].setValue(str(r_path))
            readnode['first'].setValue(int(r_first))
            readnode['last'].setValue(int(r_last))
            readnode['label'].setValue(str(r_label))
            if r_color:
                readnode['tile_color'].setValue(int(r_color))
            return readnode

        else:

            print 'Could not create read node'
        return

    def createGeo(self, dct):
        #creates a read geo node using the information from dict
        #returns a populated read geo node
        r_path = dct.get('file')
        if all(v is not None for v in [r_path]):
            readgeo = nuke.createNode('ReadGeo', inpanel=False)
            readgeo['file'].setValue(r_path)
            return readgeo
        else:

            print 'Could not create geo node'
        return

    def importScript(self, path):
        #container that imports a nuke script. (cameras, precomps, etc)
        nuke.nodePaste(path)
        return

    def createLuxWrites(self, wtype='',**dcts):

        ''' wtype can be either 'OUTPUT', or 'PRECOMP', it will default to 'OUTPUT' if no values entered
            dcts  can be passed to build the write nodes with custom parameters. This will overwrite the default settings. 
                each projects write dct can be defined in the createWriteDict() function. 
        '''

        script_context = self.getScriptContext()

        shotcode = self.getShotCode(self.getPath(nuke.root()))


        discipline = 'OUTPUT'
        tag = shotcode
        lux_writes = []

        if not dcts:
            dcts = self.createWriteDict(shotcode)
        else:
            dcts=dcts['dcts']

        if not wtype:
            if script_context.lower() not in ['comp', 'compositing', '']:
                discipline = 'PRECOMP'
                tag = script_context
                lux_write_dcts = dcts['PRECOMP']
                pass

            else:
                lux_write_dcts = dcts['OUTPUT']
                pass

        else:
            discipline = wtype.upper()
            if discipline == 'PRECOMP':
                tag = script_context
            lux_write_dcts = dcts[discipline]


        for lux_write_dct in lux_write_dcts:

            lux_write = nuke.createNode('lux_write.gizmo')

            #Untitled Script handling
            if not lux_write['root_path'].value():
                lux_write['root_path'].setValue(self.untitledScriptPath)

            if lux_write['tag'].value() in ['ROOT','']:
                lux_write['tag'].setValue('UntitledImage') 

            lux_writes.append(lux_write)
            lux_write['discipline'].setValue(discipline)
            lux_write['tag'].setValue(tag)

            if 'container' in lux_write_dct:
                if 'padding' in lux_write_dct['container']:
                    lux_write['padding'].setValue(int(lux_write_dct['container']['padding']))

            w_count = 2

            for write_dct in lux_write_dct['writes']:
                #print write_dct
                lux_write.knob('add_write').execute()

                filetype = None

                #The Write node inside the LUX_WRITE group
                write_node = nuke.toNode('{}.Write_writecode{}_0'.format( lux_write.name(), str(w_count) ))
                #The Reformat node inside the LUX_WRITE group
                reformat_node = write_node.input(0)

                #LUX_WRITE NODE RELATED
                if write_dct.get('filetype'):

                    filetype = write_dct['filetype'].upper()

                    if filetype == 'JPG':
                        filetype = 'JPEG'

                    write_node['file_type'].setValue(filetype.lower())
                    #set filetype

                if write_dct.get('colorspace'):
                    write_node['colorspace'].setValue(write_dct['colorspace'])
                    #set colorspace

                #REFORMAT NODE RELATED
                if write_dct.get('format'):
                    #set format
                    reformat_node['format'].setValue(write_dct['format'])

                if write_dct.get('disable_reformat'):
                    #set format
                    reformat_node['disable'].setValue(write_dct['disable_reformat'])

                #EXR + DPX specific settings
                if filetype in ['EXR','DPX']:
                    if write_dct.get('datatype'):#EXR,DPX Only
                        datatype = write_dct['datatype']
                        write_node['datatype'].setValue(datatype)
                        #set datatype

                #EXR Specific settings
                if filetype == 'EXR':
                    if write_dct.get('compression'):#EXR Only
                        write_node['compression'].setValue(write_dct['compression'])
                        #set compression

                    if write_dct.get('autocrop'):#EXR Only
                        write_node['autocrop'].setValue(write_dct['autocrop'])
                        #set autocrop

                #DPX Specific Settings
                if filetype == 'DPX':
                    if write_dct.get('transfer'):#DPX Only
                        write_node['transfer'].setValue(write_dct['transfer'])
                        #set transfer

                #JPEG Specific Settings
                if filetype == 'JPEG':
                    #defaults
                    write_node['_jpeg_quality'].setValue(1.0)
                    write_node['_jpeg_sub_sampling'].setValue('4:4:4')

                    #dct override
                    if write_dct.get('quality'):#JPEG Only
                        quality = float(write_dct['quality'])
                        write_node['_jpeg_quality'].setValue(quality)
                        #set quality
                    if write_dct.get('subsampling'):#JPEG Only
                        write_node['_jpeg_sub_sampling'].setValue(write_dct['subsampling'])
                        #set subsampling

                w_count += 1

        return lux_writes

    def createRetimeWrites(self):

        path = self.getPath()
        plates = self.getPlatesDirectory(path)
        shot_code = self.getShotCode(path)

                
        reformat_settings = self.plate_reformat_settings

        if ('OMS' in shot_code) or ('OLD' in shot_code) or ('SMN' in shot_code):
            reformat_settings = ['','DCI_2K 16:9','HALF_HD']

        if not len(plates):
            return
            
        imported_plates = self.importPlates(path)


        for p in imported_plates:

            self.deselectAll()

            plate_dir = p['file'].value()

            retime_plates_dir = plate_dir

            plate_type = plate_dir.split(shot_code)[1][1::].split('/')[1]

            input_plate_type = plate_type

            if 'R' in plate_type.split('_')[-1]:
                continue

            if 'ELEM' in plate_type.split('_')[0]:
                continue

            if '_O' in plate_type:
                plate_type = plate_type.replace('_O', '_R')
            else:
                plate_type = plate_type+'R'

            #retime_plates_dir = retime_plates_dir.split('/PLATE/')[0]+'/PLATE/'+plate_type+'/'

            retime_plates_dir = retime_plates_dir.split('/01_PLATES/')[0]+'/01_PLATES/'+shot_code+'/'+plate_type.split('_')[0]+'/'+plate_type

            # 01_EXRS
            d1 = nuke.createNode('Dot',inpanel=False)
            d1.setInput(0, p)
            r1 = nuke.createNode('Reformat',inpanel=False)
            if reformat_settings[0]:
                r1['format'].setValue(reformat_settings[0])
            r1.setInput(0,d1)

            w1 = nuke.createNode('Write',inpanel=False)
            w1_path = '{retime_plates_dir}/01_EXRS/{shot_code}.####.exr'.format(retime_plates_dir=retime_plates_dir,plate_type=plate_type,shot_code=shot_code)
            w1['file'].setValue(w1_path)
            w1['metadata'].setValue('all metadata')
            w1.setInput(0,r1)

            # 02_FULL_RES_JPEGS
            d2 = nuke.createNode('Dot',inpanel=False)
            d2.setInput(0, d1)

            r2 = nuke.createNode('Reformat',inpanel=False)
            if reformat_settings[1]:
                r2['format'].setValue(reformat_settings[1])
            r2.setInput(0,d2)

            w2 = nuke.createNode('Write',inpanel=False)
            w2_path = '{retime_plates_dir}/02_FULL_RES_JPEGS/{shot_code}.####.jpeg'.format(retime_plates_dir=retime_plates_dir,plate_type=plate_type,shot_code=shot_code)
            w2['file'].setValue(w2_path)
            w2.setInput(0,r2)
            
            #03_HALF_RES_JPEGS
            d3 = nuke.createNode('Dot',inpanel=False)
            d3.setInput(0, d2)

            r3 = nuke.createNode('Reformat',inpanel=False)
            r3.setInput(0,d3)
            if reformat_settings[2]:
                r3['format'].setValue(reformat_settings[2])

            w3 = nuke.createNode('Write',inpanel=False)
            w3_path = '{retime_plates_dir}/03_HALF_RES_JPEGS/{shot_code}.####.jpeg'.format(retime_plates_dir=retime_plates_dir,plate_type=plate_type,shot_code=shot_code)
            w3['file'].setValue(w3_path)
            w3.setInput(0,r3)

            new_nodes = [p, d1,d2,d3, r1,r2,r3, w1,w2,w3]
            for n in new_nodes:
                n.setSelected(True)
                pass
            nuke.autoplace_all()

            #w1['ypos'].setValue(w1['ypos'].value()+200)
            #w2['ypos'].setValue(w2['ypos'].value()+200)
            #w3['ypos'].setValue(w3['ypos'].value()+200)

            bg = autoBackdrop.autoBackdrop()
            bg['bdwidth'].setValue(500)
            bg['label'].setValue('RETIME {2}\nShot: {0}\nInput: {1} \nOutput: {2}'.format(shot_code, input_plate_type, plate_type))

        nuke.autoplace_all()

        return

    def createPlateWrite(self, plate_dir, shot_code):

        new_nodes = []

        file_folders = ['01_EXRS', '02_FULL_RES_JPEGS', '03_HALF_RES_JPEGS']

        d = nuke.createNode('Dot',inpanel=False)

        new_nodes.append(d)

        reformat_settings = self.plate_reformat_settings

        plate_type_ext = plate_dir.split('/')[-2]

        if ('OMS' in shot_code) or ('OLD' in shot_code) or ('SMN' in shot_code):

            reformat_settings = ['','DCI_2K 16:9','HALF_HD']

        for i,f in enumerate(file_folders):

            reformat = reformat_settings[i]

            if f == '01_EXRS':

                r = nuke.createNode('Reformat',inpanel=False)
                if reformat:
                    r['format'].setValue(reformat)
                r.setInput(0,d)

                ext = 'exr'
                file_name = plate_dir + f + '/'+shot_code+'.####.'+ext
                w = nuke.createNode('Write',inpanel=False)
                w['file'].setValue(file_name)
                w['file_type'].setValue('exr')
                w['autocrop'].setValue(True)
                w.setInput(0,r)

            else:

                r = nuke.createNode('Reformat',inpanel=False)
                if reformat:
                    r['format'].setValue(reformat)
                r.setInput(0,d)
                ext = 'jpeg'
                file_name = plate_dir + f + '/'+shot_code+'.####.'+ext
                w = nuke.createNode('Write',inpanel=False)
                w['file'].setValue(file_name)
                w.setInput(0,r)

            new_nodes.append(r)
            new_nodes.append(w)


        d['label'].setValue('Output: {1} \nShot: {0}'.format(shot_code, plate_type_ext))
        d['note_font_size'].setValue( 35 )
        #d['ypos'].setValue( d['ypos'].value() + 200 )
        
        self.deselectAll()

        '''
        #does not work; xpos, ypos gets defined way later... ffffff...
        if new_nodes:
            max_x = new_nodes[0]['xpos'].value()
            max_y = new_nodes[0]['ypos'].value()
            min_x = new_nodes[0]['xpos'].value()
            min_y = new_nodes[0]['ypos'].value()

            for n in new_nodes:
                max_x = max(max_x,n['xpos'].value())
                max_y = max(max_y,n['ypos'].value())
                min_x = min(min_x,n['xpos'].value())
                min_y = min(min_y,n['ypos'].value())
                print max_x, max_y, min_x, min_y
            max_x += 130
            max_y += 50
            min_x -= 50
            min_y -= 50
            w = max_x - min_x
            h = max_y - min_y
            bg = nuke.createNode('BackdropNode')
            bg['xpos'].setValue(int(min_x))
            bg['ypos'].setValue(int(min_y))
            bg['bdwidth'].setValue(int(w))
            bg['bdheight'].setValue(int(h))
            bg['label'].setValue('Shot: {0} \nOutput: {1}'.format(shot_code, plate_type_ext))
            new_nodes.append(bg)
            self.deselectAll()
        '''

        '''
        #does not work. charshes nuke versions 11 and above
        bg = autoBackdrop.autoBackdrop()
        new_nodes.append(bg)
        bg['bdwidth'].setValue(500)
        bg['label'].setValue('Shot: {0} \nOutput: {1}'.format(shot_code, plate_type_ext))
        self.deselectAll()
        '''

        return new_nodes

    def createPlateWritesUI(self, *path):
        '''Creates custom Plate Writes'''

        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

        plates = self.getPlatesDirectory(path)
        shot_code = self.getShotCode(path)

        if not len(plates):
            return


        plate_options = ''
        plate_disciplines = []
        plate_types = []
        plate_types_txt = ''

        plate_dir = plates[0]
        plate_dir = plate_dir.split(shot_code)[0]
        plate_dir = plate_dir + shot_code + '/'

        for p in plates:
            plate_discipline = p.split('/')[-4]
            plate_type = p.split('/')[-3]
            plate_disciplines.append(plate_discipline)
            plate_types_txt+= plate_type +'\n'
            plate_types.append(plate_type)

        plate_disciplines = list(set(plate_disciplines))
        for p in plate_disciplines:
            plate_options += p+' '

        #plate_options+='New..'

        options = nuke.Panel('Plate Ingest Options')

        options.addEnumerationPulldown('Plate Type', '{}'.format(plate_options))
        #p.addSingleLineInput('New Plate/Elem name', 'PLATE')
        options.addBooleanCheckBox('Denoised? (D)', False)
        options.addBooleanCheckBox('Undistorted? (U)', False)
        options.addBooleanCheckBox('Retimed? (R)', False)
        options.addBooleanCheckBox('Merged/Combined (M)?', False)
        options.addBooleanCheckBox('Coloured/LUT (C)?', False)
        options.addBooleanCheckBox('Transformed/Cropped (T)?', False)
        #options.addBooleanCheckBox('Is this for 3D?', False)
        options.addMultilineTextInput('Existing Plates/Elements', plate_types_txt)
        ret = options.show()

        if ret:

            plate_type_ext = ''

            if options.value('Denoised? (D)'):              plate_type_ext += 'D'
            if options.value('Undistorted? (U)'):           plate_type_ext += 'U'
            if options.value('Retimed? (R)'):               plate_type_ext += 'R'
            if options.value('Merged/Combined (M)?'):       plate_type_ext += 'M'
            if options.value('Coloured/LUT (C)?'):          plate_type_ext += 'C'
            if options.value('Transformed/Cropped (T)?'):   plate_type_ext += 'T'

            if not plate_type_ext:
                plate_type_ext = 'O'
                #should never be overwriting O type plates/elements. Thats up to Coordination. 
                nuke.message('You cannot create this Plate/Element. Retry and select at least one option.')
                pass

            plate_type_ext = options.value('Plate Type') + '_' + plate_type_ext #PLATE_O, ELEM01_U

            if plate_type_ext in plate_types:

                ask = nuke.ask('You are about to create an element that already exists. The new renders will overwrite the existing ones. Are you sure you want to create these write nodes?')
                if ask:
                    pass
                if not ask:
                    return


            plate_dir += options.value('Plate Type') + '/' + plate_type_ext + '/'

            #print plate_dir

            self.createPlateWrite(plate_dir, shot_code)




        return

    
    # Sanity Check functions

    def sanityCheck(self):
        #checks the default values of project settings
        #Rturns a nuke message if default values are detected


        if (self.formatCheck() and self.frameRangeCheck()):
            return True
        else:
            if not self.frameRangeCheck():
                reset_frame_range = nuke.ask('Default settings detected, set frame range to plate? ')
                if reset_frame_range:
                    self.deselectAll()
                    img_dirs = self.getPlatesDirectory()#raw_dirs
                    img_dirs = [i for i in img_dirs if '/PLATE/' in i.upper()]
                    img_dirs = sorted(img_dirs)

                    img_seq_info = self.getSequences(img_dirs[0])[0]

                    nuke.Root()['first_frame'].setValue( int(img_seq_info['first']) )
                    nuke.Root()['last_frame'].setValue( int(img_seq_info['last']) )

                return False

            nuke.message('Check Project Settings! Default values detected.')
            return False

    def frameRangeCheck(self):
        #Returns a nuke popup if frame range is not set
        first_frame = int(nuke.Root()['first_frame'].value())
        last_frame  = int(nuke.Root()['last_frame'].value())

        if (first_frame == 1) and (last_frame == 100):
            return False
        else:
            return True

    def formatCheck(self):
        #Returns a nuke popup if format is not set
        current_format = nuke.Root()['format'].value()
        width =  current_format.width()
        height = current_format.height()
        if (width == 640) and (height == 480):
            return False
        else:
            return True

    def versionCheck(self):
        #Asks user to version up if the user opens a v001 script. 
        script = self.getPath()
        script_v = script.split('/')[-1].split('_')[-1].split('.')[0]
        script_v = script_v[1:4]
        if script_v == '001':
            if nuke.ask('This is a V001 script. It is highly recommended for you to version up. \n\n<font color="red">Would you like to version up now?'):
                versionUp.versionUp()

        return

    
    # Utility functions

    def grabPattern(self, string, pattern):
        #returns the first matching pattern group in string
        #grabPattern('some string for sure', r"(\d{3})")
        _pattern = re.compile(pattern, re.I)
        _match = _pattern.search(string)
        try:
            _match = _match.group()
            return _match
        except AttributeError:
            return ''
        
    def removePattern(self, string, pattern):
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

    def replacePattern(self, string, pattern, replace):
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

    def getShotCode(self, *path):
        '''Retrieves a Shot Code from a path.
        1.Try to grab it using shot code template
        2.If unsuccessful, look into file name, and grab the folder after department folder.
        '''
        if not path:
            path = self.getPath()


        else:
            path=path[0]

        shotcode = self.grabPattern(path, self.re_shotcode)
        
        if not shotcode:
            try:
                shotcode = shotcode.split( self.grabPattern(path, self.re_departments ))[1]
                shotcode = shotcode.split('/')[0]
            except ValueError:
                print 'Could not detect shot code. Is this an untitled script?'

        return shotcode 

    def getScriptContext(self):
        '''Gets the script context from nuke script
        '''
        root_name = nuke.root()['name'].value()
        script_name = root_name.split('/')[-1]
        script_context = script_name.split('.')[0]
        script_context = self.removePattern(script_context, self.re_shotcode)
        #shotcode = self.getShotCode()
        if script_context:
        
            if script_context[0] == '_':
                script_context = script_context[1:]
            script_context = self.removePattern(script_context, self.re_version_tag)

            if script_context.lower() in ['comp', 'compositing', '']:
                script_context = 'Comp'

        else:
            print 'No script Context. Is this an untitled script?'

        return script_context

    def createWriteDict(self, shot_code):
        ''' This function constructs the lux_write dict. Use the default_dct as the example construction of the lux_write dict.

            OUTPUT      = Lux Write build for OUTPUT, if its not defined, it will use the OUTPUT from default_dct
            PRECOMP     = Lux Write build for OUTPUT, if its not defined, it will use the PRECOMP from default_dct

                writes      = Main container list. It should contain a list of dict of write settings (List of Dicts)
                    filetype         = File type of the write node (Str), make it all caps for Legacy use.
                    colorspace       = Colorspace for the write node (Str)
                    datatype         = DPX/EXR datatype. (Str) For Exr any either '16 bit half' or '32 bit float'. For DPX use one of '8 bit', '10 bit', '12 bit', '16 bit'
                    quality          = JPEG Quality (Float) Quality Slider from 0 to 1.0
                    subsampling      = JPEG Subsampling (Str), '4:2:2', '4:4:4'
                    compression      = EXR compression settings (Str)
                    autocrop         = EXR autocrop settings (Bool)
                    disable_reformat = Disables the reformat for the write node at hand (Bool)
                    format           = Format name for the reformat node (Str)

                container   = knobs that will apply to all writes in the container (Dict)
                    padding     = custom padding (Int)

            The following parameters are mandatory: filetype, colorspace
        '''

        #DEFAULT Write Settings
        default_dct =  {
                    'OUTPUT':
                        [
                            {   'writes'  :     [{'filetype':'DPX', 'colorspace':'AlexaV3LogC', 'datatype':'12 bit'}], 
                                'container':    {'padding':self.padding},
                            } , 

                            {   'writes'  :     [{'filetype':'JPEG', 'colorspace':'sRGB', 'subsampling':'4:4:4'}], 
                                'container':    {'padding':self.padding} 
                            } 
                        ],

                    'PRECOMP':
                        [
                            {   'writes'  :     [{'filetype':'EXR', 'colorspace':'linear', 'disable_reformat':True, 'datatype':'16 bit half'}], 
                                'container':    {'padding':self.padding},
                            }
                        ]
                }

        dcts = default_dct

        #OMENS, OMENS-LookDev, SWEET MAGNOLIA Write Settings
        if ('OMS' in shot_code) or ('OLD' in shot_code) or ('SMN' in shot_code):

            dcts =  {
                        'OUTPUT':
                            [
                                {   'writes'  :     [{'filetype':'DPX', 'colorspace':'SLog3', 'datatype':'16 bit'}], 
                                    'container':    {'padding':self.padding},
                                } , 

                                {   'writes'  :     [{'filetype':'JPEG', 'colorspace':'sRGB', 'format':'HD_1080'}], 
                                    'container':    {'padding':self.padding} 
                                } 
                            ]
                    }
        #FONZO  Write Settings
        if ('SPD' in shot_code):

            dcts =  {
                        'OUTPUT':
                            [
                                {   'writes'  :     [{'filetype':'DPX', 'colorspace':'AlexaV3LogC', 'datatype':'16 bit'}],
                                    'container':    {'padding':self.padding},
                                } ,

                                {   'writes'  :     [{'filetype':'JPEG', 'colorspace':'sRGB', 'format':'HD_1080'}], 
                                    'container':    {'padding':self.padding},
                                }
                            ]
                    }

        #Use defaults where applicable
        if not dcts.get('PRECOMP'):
            dcts['PRECOMP'] = default_dct['PRECOMP']

        if not dcts.get('OUTPUT'):
            dcts['OUTPUT'] = default_dct['OUTPUT']

        return dcts

    def deselectAll(self):
        nuke.selectAll()
        nuke.invertSelection()


    # Script initializers

    def initScript(self, *dcts):

        '''initializes the v1 script by loading everything needed to start the comp task
        list of dcts is for the write nodes; 
        '''
        self.versionCheck()
        self.importAll()
        self.createLuxWrites()
        self.sanityCheck()

        import ftrack_nuke_utils
        ftrack_nuke_utils.init()


        #ask user to version up

    def initRetimeScript(self, *dcts):

        path = self.getPath()

        #self.importPlates(path)
        self.importCutrefs(path)
        self.createRetimeWrites()
        self.sanityCheck()

        return

    def initSlapComp(self, *dcts):

        return


    # Functions to import assets

    def importAll(self, *path):
        '''Imports all assets related to the shot. Should be the first thing to run on a script.
        '''
        if path:
            path = path[0]
        else:
            path = self.getPath()

        self.importPlates(path)
        self.importCutrefs(path)
        self.importCameras(path)
        self.importGeos(path)
        self.importRenders(path)
        self.importUndistorts(path)

        return

    def importPlates(self, *path):
        '''Imports the plates 
        '''
        
        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

        img_dirs = self.getPlatesDirectory(path)#raw_dirs
        #print img_dirs
        #img_infos = []
        nodes = []
        if len(img_dirs) > 1:
            img_dirs = sorted(img_dirs)

        for d in img_dirs:

            img_seq_info = self.getSequences(d)
            
            for img_seq in img_seq_info:
                #print img_seq
                img_seq['tile_color'] = 1153044991
                readnode = self.createRead(img_seq)
                readnode['label'].setValue(img_seq['file'].split('/')[-3])
                #img_infos.append(s)


                nodes.append(readnode)


        return nodes

    def importCutrefs(self, *path):
        '''Imports the cutrefs 
        '''
        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

        precomp_dir = self.replacePattern(path, self.re_departments, '/05_COMP/')
        precomp_dir += '02_OUTPUT/01_precomp/'
        nodes = []

        if not os.path.isdir(precomp_dir):
            return None
        try:
            cutref_dir = sorted([i for i in os.listdir(precomp_dir) if 'cutref' in i.lower()])[-1]
            cutref_dir = precomp_dir+cutref_dir+'/'
            
            img_seq_info = self.getSequences(cutref_dir)

            for img_seq in img_seq_info:
                img_seq['label'] = img_seq['file'].split('/')[-1].split('.')[0]
                img_seq['tile_color'] = 370581759
                readnode = self.createRead(img_seq)
                nodes.append(readnode)

        except IndexError:
            return None


        return nodes

    def importCameras(self, *path):
        '''Imports the camera nodes 
        '''
        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

        camera_dir = self.replacePattern(path, self.re_departments, '/05_COMP/')
        camera_dir += '01_DATA/camera/'

        if not os.path.isdir(camera_dir):
            return None

        files = os.listdir(camera_dir)

        camera_files = [self.removePattern(c, r"(\d{3}\.nk)") for c in files]

        camera_files = list(set(camera_files))

        print camera_files
        
        for i in camera_files:
            
            version = [i+self.grabPattern(i, r"(\d{3}\.nk)") for c in files if c == self.removePattern(i, r"(\d{3}\.nk)")]
            version = [c for c in files if i in c]
            
            version = sorted(version)[-1]
            version = camera_dir+version

            print version

            self.importScript(version)

        return

    def importGeos(self, *path):
        '''Imports the geos 
        '''
        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

        geo_dir = self.replacePattern(path, self.re_departments, '/05_COMP/')
        geo_dir += '01_DATA/obj/'

        if not os.path.isdir(geo_dir):
            return None

        files = os.listdir(geo_dir)

        geo_files = [self.removePattern(c, r"((\d{3})*\.(abc|obj))") for c in files if self.grabPattern(c, r"(\.(abc|obj))")]
        print geo_files

        geo_files = list(set(geo_files))
        
        for i in geo_files:
            
            version = [i+self.grabPattern(i, r"((\d{3})*\.(abc|obj))") for c in files if c == self.removePattern(i, r"((\d{3})*\.(abc|obj))")]
            version = [c for c in files if i in c]
            
            version = sorted(version)[-1]
            version = geo_dir+version
            
            geo_dict = {'file':version}
            self.createGeo(geo_dict)

        return

    def importRenders(self, *path):
        '''Imports the 3D renders 
        '''
        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())
        #print path
        renders_dir = self.replacePattern(path, self.re_departments, '/06_RENDERS/')
        #print renders_dir
        renders_dir = renders_dir+'FINL/'
        #print renders_dir

        if not os.path.isdir(renders_dir):
            return None

        renders_dirs = self.getSubfolders(renders_dir)

        img_dirs = renders_dirs

        for d in img_dirs:

            img_seq_info = self.getSequences(d)
            print img_seq_info

            for img_seq in img_seq_info:
                #print img_seq
                img_seq['tile_color'] = 2976391167
                self.createRead(img_seq)
            
        return

    def importPrecomps(self, *path):
        '''imports all the precomps
        '''
        return

    def importUndistorts(self, *path):

        #import nukescripts

        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

        plates = self.getPlatesDirectory(path)

        u_plates = []
        nodes = []

        for p in plates:
            if 'PLATE_U' in p.split('/'):
                u_plates.append(p)


        if len(u_plates):
            for u in u_plates:
                nk= u+[i for i in os.listdir(u) if i[-3::] == '.nk'][0]
                label = u.split('/')[-3]
                
                self.deselectAll()

                nuke.nodePaste(nk)

                for i in nuke.selectedNodes():
                    if i.Class() not in ['Group', 'Gizmo']:
                        nuke.delete(i)
                    else:
                        i['label'].setValue(i['label'].value()+'\n'+label)
                        nodes.append(i)


        self.deselectAll()

        return nodes


    def getLatestComps(self,*path):
        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

        comp_out = self.getCompDirectory(path)

        shot_name = self.getShotCode(path)

        versions = [comp_out+i for i in os.listdir(comp_out) if (shot_name in i) and (len(os.listdir(comp_out+i)) != 0 )]

        versions = sorted(versions,reverse=True)

        latest = versions[0] + '/JPEG/'

        #img_folders = [latest+i+'/' for i in  os.listdir(latest)]
        imgs = [latest+i for i in os.listdir(latest) if (i[-5:]=='.jpeg') and (shot_name in i)]

        if imgs:
            return imgs[0]

        return



    def importLatestComps(self, *path):
        '''imports latest comp renders
        '''
        if path:
            path = self.getRootPath(path[0])
        else:
            path = self.getRootPath(self.getPath())

 

        comp_out = self.getCompDirectory(path)

        shot_name = self.getShotCode(path)

        versions = [comp_out+i for i in os.listdir(comp_out) if (shot_name in i) and (len(os.listdir(comp_out+i)) != 0 )]

        versions = sorted(versions,reverse=True)

        latest = versions[0] + '/'

        img_folders = [latest+i+'/' for i in  os.listdir(latest)]

        nodes = []

        for img_folder in img_folders:

            img_seq_info = self.getSequences(img_folder)
            
            for img_seq in img_seq_info:
                #print img_seq
                img_seq['tile_color'] = 1153044991
                readnode = self.createRead(img_seq)
                readnode['label'].setValue(img_seq['file'].split('/')[-2])
                #img_infos.append(s)

                nodes.append(readnode)

        return nodes


    # Autocomp functions

    def slapComp3D(self, ftrack_dict, *path):
        '''This will slapcomp 3d renders'''
        import autoComp

        '''example dict:
            ftrack_dict = {
            'plate' : 'Q:/Omens/OMS103/01_PLATES/OMS103_012_018/PLATE/PLATE_D/01_EXRS/OMS103_012_018.%04d.exr',
            'renders': ['Q:/Omens/OMS103/06_RENDERS/OMS103_012_018/FINL/OMS103_012_018_LIGHTING_v004/beauty/','Q:/Omens/OMS103/06_RENDERS/OMS103_012_018/FINL/OMS103_012_018_LIGHTING_v002/beauty/'],
            'shadows': ['Q:/Omens/OMS103/06_RENDERS/OMS103_012_018/FINL/OMS103_012_018_LIGHTING_v004/matteShadows_util/'],
            'grain': True,
            'mattes': ['Q:/Omens/OMS103/05_COMP/OMS103_012_018/02_OUTPUT/02_mattes/OMS103_012_018_roto_v001','Q:/Omens/OMS103/05_COMP/OMS103_012_018/02_OUTPUT/02_mattes/OMS103_012_018_roto_v001'],
            'colour': True,
            'colour_frame': '1001',
            'lut' : True,
            'version' : 1,
            'user' : 'alicans'
            }
        '''

        plate           = ftrack_dict.get('plate')          #single path/to/img.###.dpx
        renders         = ftrack_dict.get('renders')        #list [path/to/img.###.dpx,path/to/img2.###.dpx]
        shadows         = ftrack_dict.get('shadows')        #list [path/to/img.###.dpx,path/to/img2.###.dpx]
        mattes          = ftrack_dict.get('mattes')         #list [path/to/img.###.dpx,path/to/img2.###.dpx]
        grain           = ftrack_dict.get('grain')          #bool
        colour          = ftrack_dict.get('colour')         #bool
        colour_frame    = ftrack_dict.get('colour_frame')   #str: 1001 or 1001-1201... single string int, or range
        lut             = ftrack_dict.get('lut')            #bool
        distortion      = ftrack_dict.get('distortion')     #bool
        version         = ftrack_dict.get('version')        #int
        user            = ftrack_dict.get('user')           #str

        plate_dir = self.dirname(plate)
        plate_read = self.createRead( self.getSequences(plate_dir)[0] )
        plate_read['auto_alpha'].setValue(True)
        out = plate_read

        shadow_related_nodes = []
        render_related_nodes = []
        matte_related_nodes = []

        if shadows:

            
            matte_shadow_bg = nuke.createNode('Constant', inpanel=False)
            matte_shadow_bg['color'].setValue(1000)
            matte_shadow_outs = [matte_shadow_bg]
            shadow_related_nodes.append(matte_shadow_bg)
            for s in shadows:

                #shadow_dir = self.dirname(s)

                shadow_read = self.createRead( self.getSequences(s)[0] )
                shadow_read['on_error'].setValue('checkerboard')

                self.deselectAll()
                shadow_read.setSelected(True)
                #shadow_out = autoComp.autoComp()
                '''
                shadow_shuffle = nuke.createNode('Shuffle', inpanel=False)
                shadow_shuffle.setInput(0, shadow_read)
                shadow_shuffle['in'].setValue('matteShadow')
                '''

                shadow_shuffle = nuke.createNode('Expression', inpanel=False)
                shadow_shuffle.setInput(0, shadow_read)
                shadow_shuffle['expr0'].setValue('matteShadow.red')
                shadow_shuffle['expr1'].setValue('matteShadow.green')
                shadow_shuffle['expr2'].setValue('matteShadow.blue')


                shadow_out = shadow_shuffle

                shadow_invert = nuke.createNode("Invert", inpanel=False)
                shadow_invert['channels'].setValue('rgba')
                shadow_invert.setInput(0, shadow_out)

                matte_shadow_outs.append(shadow_invert)

                shadow_related_nodes.append(shadow_invert)
                shadow_related_nodes.append(shadow_shuffle)
                shadow_related_nodes.append(shadow_read)

            merge_shadow = nuke.createNode("Merge2", inpanel=False)
            merge_shadow['operation'].setValue('min')

            for i in range(len(matte_shadow_outs)):

                index = i
                if index > 1:
                    index+=1
                merge_shadow.setInput(index, matte_shadow_outs[i])

            merge_shadow_plate = nuke.createNode("Merge2", inpanel=False)
            merge_shadow_plate.setInput(0, out)
            merge_shadow_plate.setInput(1, merge_shadow)
            merge_shadow_plate['operation'].setValue('multiply')

            
            out = merge_shadow_plate

        render_nodes = []
        autoComp_outs = []
        for r in renders:

            #render_dir = self.dirname(r)
            render_read = self.createRead( self.getSequences(r)[0] )
            render_read['on_error'].setValue('checkerboard')
            autoComp_group = nuke.createNode('Group', inpanel=False)
            autoComp_group.setInput(0,render_read)
            autoComp_outs.append( autoComp_group )
            self.deselectAll()
            autoComp_group.begin()

            group_input  = nuke.createNode('Input', inpanel=False)
            group_output = nuke.createNode('Output', inpanel=False)

            group_input.setSelected(True)
            breakout = autoComp.autoComp()
            group_output.setInput(0,breakout)
            nuke.Root().begin()
            
            render_nodes.append(render_read)

            render_related_nodes.append(render_read)
            render_related_nodes.append(autoComp_group)


        merge_renders = nuke.createNode("Merge2", inpanel=False)
        r_out = merge_renders

        for i in range(len(autoComp_outs)):

            index = i
            if index > 1:
                index+=1
            merge_renders.setInput(index, autoComp_outs[i])

        if colour:
            if colour_frame:
                if ',' in colour_frame or '-' in colour_frame:
                    colour_frame = colour_frame.replace('-', '&').replace(',', '&').replace(' ','')
                    colour_frame = colour_frame.split('&')
                    colour_frame = [int(i) for i in colour_frame]
                else:
                    colour_frame = [int(colour_frame),int(colour_frame)]
            else:
                first_frame = int(plate_read['first'].value())
                colour_frame = [first_frame,first_frame]

            bbox = merge_renders.bbox()
            bbox = [bbox.x(),bbox.y(),bbox.w(),bbox.h()]
            bbox = [0,0,plate_read.width(),plate_read.height()]
            
            ct = nuke.createNode('CurveTool')
            ct.setInput(0,plate_read)
            ct['ROI'].setValue(bbox)
            ct['operation'].setValue('Avg Intensities')
            nuke.execute(ct, colour_frame[0], colour_frame[1])
            ct['operation'].setValue('Max Luma Pixel')
            nuke.execute(ct, colour_frame[0], colour_frame[1])

            r_max = [1,1,1,1]
            r_min = [0,0,0,1]

            '''
            ct_r = nuke.createNode('CurveTool')
            ct_r.setInput(0,r_out)
            ct_r['ROI'].setValue(bbox)
            ct_r['operation'].setValue('Max Luma Pixel')
            nuke.execute(ct_r, colour_frame[0], colour_frame[1])
            r_max = ct_r['maxlumapixvalue'].value()+[1]
            r_min = ct_r['minlumapixvalue'].value()+[1]
            '''

            grade_wb = nuke.createNode('Grade', inpanel=False)
            grade_wb['unpremult'].setValue('rgba.alpha')
            grade_wb['black'].setValue(ct['minlumapixvalue'].value()+[1])
            grade_wb['white'].setValue(ct['maxlumapixvalue'].value()+[1])

            grade_wb['blackpoint'].setValue(r_min)
            grade_wb['whitepoint'].setValue(r_max)

            grade_wb.setInput(0,merge_renders)
            r_out = grade_wb

            grade_intensity = nuke.createNode('Grade', inpanel=False)
            grade_intensity['unpremult'].setValue('rgba.alpha')
            intensitydata = ct['intensitydata'].value()
            intensitydata[-1] = 1
            grade_intensity['white'].setValue(intensitydata)
            grade_intensity.setInput(0,r_out)
            r_out = grade_intensity

            sat  = nuke.createNode('ColorCorrect', inpanel=False)
            sat['unpremult'].setValue('rgba.alpha')
            sat['saturation'].setValue(intensitydata)
            sat.setInput(0,r_out)
            r_out = sat

        merge_renders_plate = nuke.createNode("Merge2", inpanel=False)
        merge_renders_plate.setInput(0, out)
        merge_renders_plate.setInput(1, r_out)

        out = merge_renders_plate


        if colour:
            diffusion = nuke.createNode('Blur', inpanel=False)
            diffusion['size'].setValue(100)
            diffusion['mix'].setValue(0.1)
            diffusion.setInput(0, out)
            diffusion.setInput(1, r_out)
            out = diffusion

        if mattes:
            matte_nodes = []
            for m in mattes:
                all_folders = [x[0].replace('\\','/')+'/' for x in os.walk(m)]
                all_matte_seqs = []
                for a in all_folders:
                    seq = self.getSequences(a)
                    if len(seq) > 0:
                        all_matte_seqs+=seq

                
                for a in all_matte_seqs:
                    #print a
                    matte_read = self.createRead( a )
                    matte_nodes.append( matte_read )
                    matte_related_nodes.append(matte_read)

            merge_mattes = nuke.createNode('Merge2', inpanel=False)


            for n in range(len(matte_nodes)):
                index = n
                if index > 1:
                    index+=1
                merge_mattes.setInput(index, matte_nodes[n])

            exp_node = nuke.createNode('Expression', inpanel=False)
            exp_node['expr3'].setValue('clamp(r+g+b)')
            exp_node.setInput(0, merge_mattes)

            mask_merge = nuke.createNode('Merge2', inpanel=False)
            mask_merge['operation'].setValue('mask')
            mask_merge.setInput(1, exp_node)
            mask_merge.setInput(0, plate_read)

            mattes_merge_plate = nuke.createNode('Merge2', inpanel=False)
            mattes_merge_plate.setInput(1, mask_merge)
            mattes_merge_plate.setInput(0, out)

            out = mattes_merge_plate

            
            matte_related_nodes.append(merge_mattes)
            matte_related_nodes.append(exp_node)

        reformat = nuke.createNode('Reformat')
        reformat.setInput(0,out)
        out = reformat

        if lut:

            lut_node = nuke.createNode('OmensLUT.nk')
            lut_node.setInput(0,out)
            lut_node['ftrack_user'].setValue(user)
            lut_node['set'].execute()


        default_dct =  {
                    'PRECOMP':
                        [
                            {   'writes'  :     [{'filetype':'DPX', 'colorspace':'AlexaV3LogC', 'datatype':'12 bit'}], 
                                'container':    {'padding':self.padding},
                            },

                            {   'writes'  :     [{'filetype':'JPEG', 'colorspace':'sRGB', 'subsampling':'4:4:4'}], 
                                'container':    {'padding':self.padding},
                            } 
                        ]
                }

        dcts = default_dct

        #dcts = {'PRECOMP': [{'writes': [{'datatype': '16 bit', 'filetype': 'DPX', 'colorspace': 'SLog3'}], 'container': {'padding': 4}}, {'writes': [{'filetype': 'JPEG', 'colorspace': 'sRGB', 'format': 'HD_1080'}], 'container': {'padding': 4}}], 'OUTPUT': [{'writes': [{'datatype': '16 bit half', 'filetype': 'EXR', 'colorspace': 'linear', 'disable_reformat': True}], 'container': {'padding': 4}}]}
        
        ''' #LUX Writes are problematic to initialize on the farm due to script now living in a weird directorty.......
        writes = self.createLuxWrites( dcts=dcts )
        for w in writes:
            
            if lut and w['file_types'].value() == 'JPEG':
                w.setInput(0, lut_node)
            else:
                w.setInput(0, out)

            w['version'].setValue(version)
        '''

        file_out = ftrack_dict.get('file_out')

        w1 = nuke.createNode('Write', inpanel = False)
        w1['file_type'].setValue('dpx')
        w1['colorspace'].setValue('SLog3')
        w1['file'].setValue(file_out.replace('.ext','.dpx'))
        w1.setInput(0, out)

        w2 = nuke.createNode('Write', inpanel = False)
        w2['file_type'].setValue('jpeg')
        w2['colorspace'].setValue('sRGB')
        w2['file'].setValue(file_out.replace('.ext','.jpeg'))
        if lut:
            w2.setInput(0, lut_node)
        else:
            w2.setInput(0, out)



        plate_read['xpos'].setValue(0)
        plate_read['ypos'].setValue(0)



        merge_shadow_plate['xpos'].setValue(0)
        merge_shadow_plate['ypos'].setValue(500)

        merge_shadow['xpos'].setValue(500)
        merge_shadow['ypos'].setValue(500)


        merge_renders_plate['xpos'].setValue(0)
        merge_renders_plate['ypos'].setValue(1000)

        merge_renders['xpos'].setValue(1000)
        merge_renders['ypos'].setValue(1000)


        if colour:
            diffusion['xpos'].setValue(0)
            diffusion['ypos'].setValue(1100)



        mattes_merge_plate['xpos'].setValue(0)
        mattes_merge_plate['ypos'].setValue(1500)

        mask_merge['xpos'].setValue(-500)
        mask_merge['ypos'].setValue(1000)



        shadow_nodes_x_offset = shadow_related_nodes[0]['xpos'].value()
        shadow_nodes_y_offset = shadow_related_nodes[0]['ypos'].value()
        for i in shadow_related_nodes:
            i['xpos'].setValue( i['xpos'].value() - shadow_nodes_x_offset +500 )
            i['ypos'].setValue( i['ypos'].value() - shadow_nodes_y_offset + 300 )


        render_nodes_x_offset = render_related_nodes[0]['xpos'].value()
        render_nodes_y_offset = render_related_nodes[0]['ypos'].value()
        for i in render_related_nodes:
            i['xpos'].setValue( i['xpos'].value() - render_nodes_x_offset + 1000 )
            i['ypos'].setValue( i['ypos'].value() - render_nodes_y_offset +800 )

        
        matte_nodes_x_offset = matte_related_nodes[0]['xpos'].value()
        matte_nodes_y_offset = matte_related_nodes[0]['ypos'].value()
        for i in matte_related_nodes:
            i['xpos'].setValue( i['xpos'].value() - matte_nodes_x_offset - 1000 )
            i['ypos'].setValue( i['ypos'].value() - matte_nodes_y_offset + 800 )


        return

    def skeletonPipe(self, path):

        return

    # WIP

    def importCompRenders(self, *path):
        '''Imports the latest version of comps 
        '''
        return

    def importCompScript(self, *path):
        '''Imports the latest version of comps 
        '''
        return

    def importAnims(self, *path):
        '''Imports the latest version of anims playblasts 
        '''
        return

    def importSisterShots(self, *path):
        '''Imports the latest version of comps of the sister shots
        '''
        return

