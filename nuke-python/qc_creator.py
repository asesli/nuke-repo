import os, sys
import nuke
import nukescripts
import autoBackdrop
import importAssets

class InitQC():
    def __init__(self, *_infos):
        nuke.Root().begin()

        if _infos:
            self.infos = _infos[0]
        else:
            self.infos = [['CHM201_029_010', 'Q:/Charmed_S2/CHM201/'],
                    ['CHM201_031_100', 'Q:/Charmed_S2/CHM201/'],
                    ['CHM201_031_110', 'Q:/Charmed_S2/CHM201/'],
                    ['CHM201_029_010', 'Q:/Charmed_S2/CHM201/'],
                    ['CHM201_031_100', 'Q:/Charmed_S2/CHM201/'],
                    ['CHM201_031_110', 'Q:/Charmed_S2/CHM201/']]

        self.base_path = ''
        self.shot_code = ''
            
    

    def create_read(self, file, first, last):
        r = nuke.createNode('Read', inpanel=False)
        r['first'].setValue(first)
        r['last'].setValue(last)
        r['file'].setValue(file)
        return r

    def get_read_data(self, _path, _file_type, _shot_code):

        _files = sorted([f for f in os.listdir(_path) if ( ('.{}'.format(_file_type) in f.upper()) and ( _shot_code in f.upper()) and ('.nk' not in f.lower()) ) ])

        if len(_files) > 1:
            _first, _last = int(_files[0].split('.')[-2]), int(_files[-1].split('.')[-2])
            _file = _files[0].split('.')
            _file[-2] = '%0{}d'.format(len(_file[-2]))
            _file = '.'.join(_file)
            _file = os.path.join(_path, _file)
            _file = _file.replace('\\','/')
            return _file,_first, _last

    def get_plate(self):
        file_type = 'EXR'
        file_type_prefix = '01_EXRS'
        plate_path = os.path.join(*[self.base_path,'01_PLATES',self.shot_code])
        plate_path = os.path.join(plate_path, 'PLATE/')
        
        plate_types = os.listdir(plate_path)
        plate_type = 'PLATE_O'
        if 'PLATE_R' in plate_types:
            plate_type = 'PLATE_R'
        if 'PLATE_M' in plate_types:
            plate_type = 'PLATE_M'

        
        plate_o_path = os.path.join(plate_path, '{}/'.format(plate_type))
        plate_o_exr = os.path.join(plate_o_path, file_type_prefix)
        plate_o_exr = os.path.normpath(plate_o_exr)

        plate_file, first, last = self.get_read_data(plate_o_exr, file_type, self.shot_code)

        r = self.create_read(plate_file, first, last)
        r['label'].setValue(plate_type)
        r['tile_color'].setValue(536805631)
        return r

    def get_comp(self):

        comp_o_path = os.path.join(*[self.base_path,'05_COMP',self.shot_code,'02_OUTPUT/03_comp/'])
        comp_o_path = os.path.normpath(comp_o_path)
        versions = sorted([d for d in os.listdir(comp_o_path) if ((len(os.listdir( os.path.join(comp_o_path, d) )) > 1) and ('.' not in d) and (self.shot_code in d))])
        versions.reverse()
        latest_n_versions = 2
        versions = versions[:latest_n_versions]
        
        rs = []

        for i,v in enumerate(versions):
            v_path = os.path.join(comp_o_path, v)
            types = [t for t in os.listdir(v_path) if ('.' not in t) and (len(t)<5)]
            
            for t in types:
                file_type = t
                t_path = os.path.join(v_path, t)

                comp_file, first, last = self.get_read_data(t_path, file_type, self.shot_code)
                r = self.create_read(comp_file, first, last)
                r['label'].setValue('{} V{}'.format(file_type, comp_file.split('.')[0].split('_V')[-1]))
                color = 0
                if i == 0:#new v
                    if file_type == 'JPEG':
                        color = 2243922687
                        rs.append(r)
                    else:
                        color = 968836351
                        if r['file'].value().split('/')[-1].split('_')[0][:3] in ['OMN', 'OMS', 'OLD', 'SMN']:
                            r['colorspace'].setValue('SLog3')
                        rs.append(r)
                else: #old v
                    if file_type == 'JPEG':
                        color = 4289901311
                        rs.append(r)
                    else:
                        color = 4283190527
                        if r['file'].value().split('/')[-1].split('_')[0][:3] in ['OMN', 'OMS', 'OLD', 'SMN']:
                            r['colorspace'].setValue('SLog3')
                        rs.append(r)

                r['tile_color'].setValue(color)
        return rs


    def get_cutref(self):
        cutref = importAssets.ImportAssets().importCutrefs()
        if cutref:
            cutref[0]['label'].setValue('CUTREF')
            return cutref[0]
        else:
            return



    def create(self):
        for i,info in enumerate(self.infos):

            self.shot_code = info[0]
            self.base_path = info[1]
            
            cmps = self.get_comp()
            nuke.selectAll()
            nuke.invertSelection()
            for cmp in cmps:
                cmp['selected'].setValue(True)
                nuke.autoplace(cmp)
            #nuke.autoplace_all()
            #_autoplace()

            x = autoBackdrop.autoBackdrop()
            x['bdheight'].setValue(x['bdheight'].value()+100)
            x['ypos'].setValue(x['ypos'].value()-50)
            nuke.selectAll()
            nuke.invertSelection()
            
            p = self.get_plate()
            p['xpos'].setValue(x['xpos'].value()+20)
            p['ypos'].setValue(x['ypos'].value()+20)
            c = self.get_cutref()
            if c:
                c['xpos'].setValue(p['xpos'].value()+100)
                c['ypos'].setValue(p['ypos'].value())
                c['selected'].setValue(True)
            p['selected'].setValue(True)
            

            x['label'].setValue(self.shot_code)
            x['ypos'].setValue(x['ypos'].value()-40)
            x['bdheight'].setValue(x['bdheight'].value()+40)
            #print nuke.selectedNode()['tile_color'].value()
            if i%2:
                x['tile_color'].setValue(1431655935)
            else:
                x['tile_color'].setValue(2088533247)

'''
t = [['CHM201_029_010', 'Q:/Charmed_S2/CHM201/'],
    ['CHM201_031_100', 'Q:/Charmed_S2/CHM201/'],
    ['CHM201_031_110', 'Q:/Charmed_S2/CHM201/'],
    ['CHM201_029_010', 'Q:/Charmed_S2/CHM201/'],
    ['CHM201_031_100', 'Q:/Charmed_S2/CHM201/'],
    ['CHM201_031_110', 'Q:/Charmed_S2/CHM201/']]

n = InitQC(t)
n.create()
'''