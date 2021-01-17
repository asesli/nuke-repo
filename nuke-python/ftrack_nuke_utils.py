import os, sys
import nuke
import webbrowser as wb
if sys.path[0] != "\\\\qumulo\\Libraries\\python-lib\\FTRACK":
	sys.path.insert(0, "\\\\qumulo\\Libraries\\python-lib\\FTRACK")
import ftrack_api
import getpass
import urllib2
import importAssets
import browseDir


os.environ['FTRACK_API_USER'] = getpass.getuser()
os.environ['FTRACK_SERVER'] = 'https://domain.ftrackapp.com'
os.environ['FTRACK_API_KEY'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


def ftrack_default_knobs():

	knobs = ['unnamed','command_tabs','command_tab','Ftrack','tabs','tab1','tab2',
	'shot_name','spacer1','shot_code','end1','end2','update','div1', 'tags', 
	'shot_description','time_logged','div2','slate_id','frame_range',
	'lens_info','extra_camera_info','camera_tilt','t_stop','focus',
	'filter','camera_height','camera','shutter','links_ids','ftrack_id',
	'ftrack_parent_id','ftrack_url','ftrack_proj_view_url','command_tabs_end',
	'similar_lcp_bool','sister_lcp_bool','assigned_lcp_bool','all_projects_similar_lcp_bool',
	'all_projects_assigned_lcp_bool']
	return knobs

def go_to_url(url):
	#ftrack_url = nuke.Root()['ftrack_url'].value()
	internet = wb.get('windows-default')
	internet.open(url)

def open_in_projects(shot_id):
	url = "https://domain.ftrackapp.com/#entityId={}&entityType=task&itemId=projects&view=tasks".format(shot_id)
	go_to_url(url)

def open_in_dashboard(task_id):
	url = "https://domain.ftrackapp.com/#slideEntityId={}&slideEntityType=task&itemId=home".format(task_id)
	go_to_url(url)


'''edit this so that if Ftrack tab doesnt exist, init() is called'''
def go_to_ftrack_tab():
	nuke.showSettings()
	nuke.Root()['Ftrack'].setFlag(0)

def del_knob(name):
    rr = nuke.Root()
    try:
        rr.removeKnob(rr.knobs()[name])
    except KeyError:
        pass 

def init():

	previous = save_ftrack_ui()
	delete_ftrack_ui()
	create_ftrack_ui()
	populate_ftrack_ui(previous)
	go_to_ftrack_tab()

def save_ftrack_ui():

	ui_dict = {}

	knobs = ftrack_default_knobs()
	r = nuke.Root()

	for knob in knobs:


		try:
			ui_dict[knob] = r[knob].value()
		except NameError:
			pass

	return ui_dict 

def delete_ftrack_ui():

	r = nuke.Root()

	ss_knobs = [del_knob(knob) for knob in r.knobs() if '_ss_' in knob]


	null_knobs = [del_knob(knob) for knob in r.knobs() if 
	('_div_' in knob) or 
	('_end_' in knob) or 
	('_tab_' in knob) or 
	('_spc_' in knob) or 
	('_lcp_' in knob) or 
	('_ss_' in knob) or 
	('_ss2_' in knob) or 
	('_sim_' in knob) or 
	('_ths_' in knob) or 
	('_asg_' in knob) or 
	('_sis_' in knob)]


	knobs_to_delete = ftrack_default_knobs()
	knobs_to_delete = knobs_to_delete+ss_knobs+null_knobs

	for i in knobs_to_delete:
		del_knob(i)

	return

def create_ftrack_ui():

	r = nuke.Root()

	k = nuke.Tab_Knob('Ftrack')
	r.addKnob(k)

	k = nuke.Text_Knob('shot_name', '','<b><font size=5>PRESS UPDATE -->')
	r.addKnob(k)

	k = nuke.Text_Knob('_spc_1', '','          ')
	k.clearFlag(nuke.STARTLINE)
	r.addKnob(k)

	k = nuke.PyScript_Knob('update_lcp_button', 'Update','import ftrack_nuke_utils;reload( ftrack_nuke_utils );ftrack_nuke_utils.update()')
	r.addKnob(k)

	k = nuke.Boolean_Knob('sister_lcp_bool', 'Shots in Sequence', True)
	k.setFlag(nuke.STARTLINE)
	r.addKnob(k)

	k = nuke.Boolean_Knob('similar_lcp_bool', 'Similar Shots', False)
	k.setFlag(nuke.STARTLINE)
	r.addKnob(k)

	k = nuke.Boolean_Knob('all_projects_similar_lcp_bool', 'From All Projects', False)
	k.clearFlag(nuke.STARTLINE)
	r.addKnob(k)

	k = nuke.Boolean_Knob('assigned_lcp_bool', 'Assigned Shots', False)
	k.setFlag(nuke.STARTLINE)
	r.addKnob(k)

	k = nuke.Boolean_Knob('all_projects_assigned_lcp_bool', 'From All Projects', False)
	k.clearFlag(nuke.STARTLINE)
	r.addKnob(k)

	k = nuke.Text_Knob('_div_1','')
	r.addKnob(k)

	#k = nuke.BeginTabGroup_Knob('_tab_s', 'shot name')
	#r.addKnob(k)

	#k = nuke.Tab_Knob('_tab_1', 'shot name')
	#r.addKnob(k)

	k = nuke.Multiline_Eval_String_Knob('shot_description', 'Description', 'Ftrack Shot Description.')
	r.addKnob(k)

	k = nuke.String_Knob('time_logged', 'Time Logged')
	r.addKnob(k)

	k = nuke.Text_Knob('_div_2','')
	r.addKnob(k)

	k = nuke.String_Knob('shot_code', 'Shot Code')
	k.setVisible(False)
	r.addKnob(k)

	k = nuke.String_Knob('slate_id', 'Slate')
	r.addKnob(k)

	k = nuke.String_Knob('frame_range', 'Frame Range')
	r.addKnob(k)

	k = nuke.String_Knob('lens_info', 'Lens Info')
	r.addKnob(k)

	k = nuke.String_Knob('tags', 'Tags')
	r.addKnob(k)

	k = nuke.Tab_Knob('extra_camera_info', 'Extra Camera Info', 1)
	r.addKnob(k)

	k = nuke.String_Knob('camera_tilt', 'Camera Tilt')
	r.addKnob(k)

	k = nuke.String_Knob('t_stop', 'T-Stop')
	r.addKnob(k)

	k = nuke.String_Knob('focus', 'Focus')
	r.addKnob(k)

	k = nuke.String_Knob('filter', 'Filter')
	r.addKnob(k)

	k = nuke.String_Knob('camera_height', 'Camera Height')
	r.addKnob(k)

	k = nuke.String_Knob('camera', 'Camera')
	r.addKnob(k)

	k = nuke.String_Knob('shutter', 'Shutter')
	r.addKnob(k)

	k = nuke.Tab_Knob('_end_1', '', -1)
	r.addKnob(k)


	k = nuke.Tab_Knob('links_ids', 'Links +IDs', 1)
	k.setVisible(False)
	r.addKnob(k)

	k = nuke.String_Knob('ftrack_id', 'Ftrack ID')
	r.addKnob(k)

	k = nuke.String_Knob('ftrack_parent_id', 'Ftrack Parent ID')
	r.addKnob(k)

	k = nuke.String_Knob('ftrack_url', 'Ftrack URL')
	r.addKnob(k)

	k = nuke.String_Knob('ftrack_proj_view_url', 'Ftrack Project URL')
	r.addKnob(k)

	k = nuke.Tab_Knob('_end_2', '', -1)
	r.addKnob(k)

	k = nuke.Text_Knob('_div_3','')
	r.addKnob(k)


	#k = nuke.BeginTabGroup_Knob('spacer1', 'spacer1')
	#r.addKnob(k)

	return

def add_shot_asset_knobs(shot_list,shot_name,knob_prefix):

	r=nuke.Root()
	kp=knob_prefix
	shot_name=shot_name


	for s in shot_list:
		name = s['name']
		_id = s['id']

		first = int(s['custom_attributes']['first_frame'])
		last = int(s['custom_attributes']['last_frame'])
		fps = s['custom_attributes']['fps']
		frame_range_txt = '{} - {} @ {}'.format(first,last, fps)


		path = s['custom_attributes']['out_path']
		name_txt = name



		if len(shot_list)>1:
			if name == shot_name:
				name_txt = '<b>> <i>{}</i></b>'.format(name)
		else:
			name_txt = '<b>{}</b>'.format(name)


		#thumbnail = "Q:/Omens/OMS107/03_COORDINATION/_thumbs/OMS107_001_210_V022.gif"
		thumbnail = importAssets.ImportAssets().getLatestThumbnail(path)
		#thumbnail = s['thumbnail_url']['url']

		'''
		import ftrack_api.symbol
		server_location = session.get('Location', ftrack_api.symbol.SERVER_LOCATION_ID)
		thumbnail_url = server_location.get_thumbnail_url(thumbnail_component)
		thumbnail = thumbnail_url
		'''
		#print thumbnail

		info_text = '<img src="{thumbnail}" height="200">\nShot: {shot_name}\nDescription: {description}\nSlate: {slate}\nFrame Range: {frame_range}\nLens Info: {lens}'
		
		info_text = info_text.format( 
			shot_name=name , 
			description=s['description'].encode('utf-8'), 
			slate=s['custom_attributes']['slate'].encode('utf-8'), 
			frame_range=frame_range_txt, 
			lens=s['custom_attributes']['lens_info'].encode('utf-8'),
			thumbnail=thumbnail
			)
		


		#k = nuke.Text_Knob('{}_ss_'.format(name), name_txt, '')
		#k.setTooltip(info_text)
		#r.addKnob(k)

		nuke_actions = {
			'NUKE/Import All Assets' : 	'import importAssets;importAssets.ImportAssets().importAll("{}")'.format(path), 
			'NUKE/Import Plates':		'import importAssets;importAssets.ImportAssets().importPlates("{}")'.format(path),
			'NUKE/Import Cutrefs':		'import importAssets;importAssets.ImportAssets().importCutrefs("{}")'.format(path),
			'NUKE/Import Geos':			'import importAssets;importAssets.ImportAssets().importGeos("{}")'.format(path),
			'NUKE/Import Cameras':		'import importAssets;importAssets.ImportAssets().importCameras("{}")'.format(path),
			'NUKE/Import 3D Renders':	'import importAssets;importAssets.ImportAssets().importRenders("{}")'.format(path),
			'NUKE/Import LensDistorts':	'import importAssets;importAssets.ImportAssets().importUndistorts("{}")'.format(path),
			'NUKE/Import Comps':			'import importAssets;importAssets.ImportAssets().importLatestComps("{}")'.format(path),
			'NUKE/Create Plate Writes':	'import importAssets;importAssets.ImportAssets().createPlateWritesUI("{}")'.format(path),
			'NUKE/Open Latest Comp in Nuke':		'import nuke,importAssets;nuke.scriptOpen(importAssets.ImportAssets().getLatestNk("{}"))'.format(path),
			'NUKE/Open Latest Comp in DJView':	'import open_in_djvview; open_in_djvview.launch_with_DJVView(importAssets.ImportAssets().getLatestComps("{}"))'.format(path)
			}

		ftrack_actions = {
			'FTRACK/Open Ftrack Link':		'import ftrack_nuke_utils;ftrack_nuke_utils.open_in_projects("{}")'.format(_id),
			'FTRACK/Set Status':		'import ftrack_nuke_utils;ftrack_nuke_utils.open_in_projects("{}")'.format(_id),
			'FTRACK/Add Note':		'import ftrack_nuke_utils;ftrack_nuke_utils.open_in_projects("{}")'.format(_id)
			}
			
		path_actions = {
			'PATH/Open PLATES folder':		'import browseDir;browseDir._browse(importAssets.ImportAssets().getDepartmentDirectory("01_PLATES","{}")+"PLATE/")'.format(path),
			'PATH/Open COMP folder':		'import browseDir;browseDir._browse(importAssets.ImportAssets().getDepartmentDirectory("05_COMP","{}"))'.format(path),
			'PATH/Open 3D RENDERS folder':	'import browseDir;browseDir._browse(importAssets.ImportAssets().getDepartmentDirectory("06_RENDERS","{}")+"FINL/")'.format(path),
			'PATH/Open ANIMATION folder':	'import browseDir;browseDir._browse(importAssets.ImportAssets().getDepartmentDirectory("06_RENDERS","{}")+"ANIM/")'.format(path),
			'PATH/Open CIS folder':			'import browseDir;browseDir._browse("/".join(importAssets.ImportAssets().getDepartmentDirectory("09_QT","{}").split("/")[0:-2])+"/CIS/")'.format(path),
			'PATH/Open 2D VFX Elements':	'import browseDir;browseDir._browse("{}")'.format("T:/Sequences/"),
			'PATH/Open 2D Image Library':	'import browseDir;browseDir._browse("{}")'.format("T:/06_Image_Lib/")
			}

		#k = nuke.BeginTabGroup_Knob('{}_ss_tab'.format(name), name_txt)
		#k.setTooltip(info_text)
		#r.addKnob(k)
		#k = nuke.Tab_Knob('{}_ss_t'.format(name), name_txt)
		#r.addKnob(k)

		#k = nuke.Help_Knob('{}_ss_nuke_info'.format(name),'?')
		#k.setTooltip(info_text)
		#r.addKnob(k)


		if len(shot_list)>1:
			k = nuke.Text_Knob('{}_div_ss{}'.format(name,kp),' ')
			r.addKnob(k)

		k = nuke.Text_Knob('{}_ss_spacer_info{}'.format(name,kp), name_txt,' ')
		k.clearFlag(nuke.STARTLINE)
		r.addKnob(k)

		k = nuke.Text_Knob('{}_ss_image_info{}'.format(name,kp), '','<img src="{}" height="50">'.format(thumbnail))
		k.clearFlag(nuke.STARTLINE)
		k.setTooltip(info_text)
		r.addKnob(k)

		k = nuke.Pulldown_Knob('{}_ss_nuke_actions{}'.format(name,kp), '', nuke_actions)
		k.clearFlag(nuke.STARTLINE)
		k.setTooltip(info_text)
		r.addKnob(k)

		k = nuke.Pulldown_Knob('{}_ss_ftrack_actions{}'.format(name,kp), '', ftrack_actions)
		k.clearFlag(nuke.STARTLINE)
		k.setTooltip(info_text)
		r.addKnob(k)

		k = nuke.Pulldown_Knob('{}_ss_path_actions{}'.format(name,kp), '', path_actions)
		k.clearFlag(nuke.STARTLINE)
		k.setTooltip(info_text)
		r.addKnob(k)

		k = nuke.Text_Knob('{}_ss_id{}'.format(name,kp), '', _id)
		k.setVisible(False)
		r.addKnob(k)

	#k = nuke.EndTabGroup_Knob('{}_ss_tab22'.format(name), '')
	#r.addKnob(k)

def populate_ftrack_ui(knob_dict):

	knobs = ftrack_default_knobs()
	r = nuke.Root()
	ignore_knobs = ['div1','div2','end1','end2','spacer1','extra_camera_info','links_ids']

	for i in ignore_knobs:
		knobs.remove(i)

	for knob in knobs:
		try:
			r[knob].setValue(knob_dict.get(knob))

		except (NameError, TypeError, ValueError) as e:
			pass

	return

'''edit this so that if IDs are not populated, it should querry it using shots name and context and populate it by itself.
This will resolve outdated scripts.'''

def update():

	init()

	import importAssets

	session = ftrack_api.session.Session(auto_connect_event_hub=True)

	#ID parameter detection.
	#get ids from Ftrack if its not populated already. 


	task_id = nuke.Root()['ftrack_id'].value()
	shot_id = nuke.Root()['ftrack_parent_id'].value()
	shot_info = session.query('select custom_attributes, project_id, name, description, parent.id from TypedContext where id is {}'.format(shot_id)).one()
	task_info = session.query('select custom_attributes, time_logged, name, description from TypedContext where id is {}'.format(task_id)).one()
	#print task_info['status']['state']['name']
	#a= task_info['assignments']
	#for i in a:
	#	print i['resource']['username']

	parent_id = shot_info['parent']['id']

	r = nuke.Root()

	ss_knobs = [del_knob(knob) for knob in r.knobs() if '_ss_' in knob]

	task_name = task_info['name']
	shot_name = shot_info['name']
	shot_tags = shot_info['custom_attributes']['tags']
	proj_id = shot_info['project_id']


	#k = nuke.BeginTabGroup_Knob('command_tab_lcp_1', '')
	#r.addKnob(k)



	#k = nuke.Tab_Knob('command_tab_ss_2', 'Commands')
	#r.addKnob(k)

	#add the commands
	'''
	k = nuke.BeginTabGroup_Knob('command_tab_ss_1', '')
	r.addKnob(k)
	k = nuke.Tab_Knob('command_tab_ss_2', 'Commands')
	r.addKnob(k)


	k = nuke.EndTabGroup_Knob('command_tab_ss_end', '')
	r.addKnob(k)

	'''

	###

	add_shot_asset_knobs([shot_info],'','_ths_')
	k = nuke.Text_Knob('_div_ths_1','')
	r.addKnob(k)

	if r['assigned_lcp_bool'].value():

		user = getpass.getuser()  


		'''
		if r['all_projects_assigned_lcp_bool'].value():
			assigned_shots = session.query('select id,name from Shot where children any ((assignments any (resource.username = "{}")) and (status.name in ("Done","Not Started")))'.format(user)).all()
		else: 
			assigned_shots = session.query('select id,name from Shot where (children any (assignments any (resource.username = "{}")) and (status.state.name in ("Done","Not Started"))) and (project_id is "{}")'.format(user,proj_id)).all()
		'''
		statuses = ('In Progress', 'Internal Review',)
		states = ('In Progress', 'Not Started',)

		if r['all_projects_assigned_lcp_bool'].value():
			assigned_tasks = session.query('select parent.id from Task where (assignments any (resource.username = "{}")) and (status.state.name in {}) and (project.status is active)'.format(user,states)).all()
		else:
			assigned_tasks = session.query('select parent.id from Task where (assignments any (resource.username = "{}")) and (status.state.name in {}) and (project.status is active) and (project_id is "{}")'.format(user,states,proj_id)).all()

		#for i in assigned_tasks:
		#	print i['parent']['name']
		ids = [i['parent']['id'] for i in assigned_tasks]
		ids = '", "'.join(ids)
		#ids = tuple(ids)
		assigned_shots = session.query('select id, name, custom_attributes from Shot where (id in ("{}")) and (status.state.name != "Blocked")'.format(ids)).all()
		#for i in assigned_shots:
		#	print i['status']['state']['name']
		#	print i['project'].keys()



		if assigned_shots:

			ss_group_begin = nuke.Tab_Knob('shots_asg_begin', 'Assigned Shots', 1)
			r.addKnob(ss_group_begin)

			assigned_shots = sorted(assigned_shots, key = lambda i: i['name'])

			add_shot_asset_knobs(assigned_shots,shot_name,'_asg_')

			ss_group_end = nuke.Tab_Knob('shots_asg_end', '', -1)
			r.addKnob(ss_group_end)


	if r['sister_lcp_bool'].value():

		sister_shots = session.query('select custom_attributes, name, description, id from TypedContext where parent.id is {}'.format( parent_id )).all()

		if sister_shots:

			ss_group_begin = nuke.Tab_Knob('shots_sis_begin', 'Sister Shots', 1)
			r.addKnob(ss_group_begin)

			sister_shots = sorted(sister_shots, key = lambda i: i['name'])

			add_shot_asset_knobs(sister_shots,shot_name,'_sis_')

			ss_group_end = nuke.Tab_Knob('shots_sis_end', '', -1)
			r.addKnob(ss_group_end)


	if r['similar_lcp_bool'].value():

		similar_shots = []

		for tag in shot_tags:

			if r['all_projects_similar_lcp_bool'].value():

				shots_from_tag = session.query('select custom_attributes, name, description, id from Shot where custom_attributes any (key is "tags" and value in ("{}") )'.format(tag)).all()
			
			else:

				shots_from_tag = session.query('select custom_attributes, name, description, id from Shot where (custom_attributes any (key is "tags" and value in ("{}")) and (project_id is "{}"))'.format(tag,proj_id)).all()
			

			similar_shots += shots_from_tag


		if similar_shots:

			similar_shots = list(set(similar_shots))

			ss_group_begin = nuke.Tab_Knob('shots_sim_begin', 'Similar Shots', 1)
			r.addKnob(ss_group_begin)

			similar_shots = sorted(similar_shots, key = lambda i: i['name'])

			add_shot_asset_knobs(similar_shots,shot_name,'_sim_')


			ss_group_end = nuke.Tab_Knob('shots_sim_end', '', -1)
			r.addKnob(ss_group_end)
		#similar_shots = session.query('select custom_attributes.tags, name from Shot where custom_attributes.tags is [u"smoke"]').one()
		#print similar_shots[0]['custom_attributes']['tags']
		print 




	#k = nuke.BeginTabGroup_Knob('command_tab_lcp_end_', '')
	#r.addKnob(k)

	shot_name_txt = '<b><font size=5>{} - {}</font></b>'.format(shot_name, task_name)
	r['shot_name'].setValue(shot_name_txt)

	#nuke.Root()['_tab_1'].setLabel(shot_name)

	shot_description = shot_info['description']
	r['shot_description'].setValue(shot_description)

	task_time = (float(task_info['time_logged']) / 60 ) / 60
	task_time = '{0:02.0f}:{1:02.0f}'.format(*divmod(task_time * 60, 60))
	r['time_logged'].setValue(task_time)

	r['shot_code'].setValue(shot_name)

	slate_id = shot_info['custom_attributes']['slate']
	if slate_id:
		r['slate_id'].setValue(slate_id)
	else:
		r['slate_id'].setVisible(False)


	first = int(shot_info['custom_attributes']['first_frame'])
	last = int(shot_info['custom_attributes']['last_frame'])
	fps = shot_info['custom_attributes']['fps']
	frame_range_txt = '{} - {} @ {}'.format(first,last, fps)
	if (first and last and fps):
		r['frame_range'].setValue(frame_range_txt)
	else:
		r['frame_range'].setVisible(False)

	lens_info = shot_info['custom_attributes']['lens_info']
	if lens_info:
		r['lens_info'].setValue(lens_info)
	else:
		r['lens_info'].setVisible(False)

	tags = shot_info['custom_attributes']['tags']
	
	if tags:
		tags_txt = ', '.join(tags)
		r['tags'].setValue(tags_txt)
	else:
		r['tags'].setVisible(False)

	camera_tilt = shot_info['custom_attributes']['Camera Tilt']
	if camera_tilt:
		r['camera_tilt'].setValue(camera_tilt)
	else:
		r['camera_tilt'].setVisible(False)

	t_stop = shot_info['custom_attributes']['T-stop']
	if t_stop:
		r['t_stop'].setValue(t_stop)
	else:
		r['t_stop'].setVisible(False)

	focus = shot_info['custom_attributes']['Focus']
	if focus:
		r['focus'].setValue(focus)
	else:
		r['focus'].setVisible(False)

	_filter = shot_info['custom_attributes']['Filter']
	if _filter:
		r['filter'].setValue(_filter)
	else:
		r['filter'].setVisible(False)

	camera_height = shot_info['custom_attributes']['Camera Height']
	if camera_height:
		r['camera_height'].setValue(camera_height)
	else:
		r['camera_height'].setVisible(False)

	camera = shot_info['custom_attributes']['Camera']
	if camera:
		r['camera'].setValue(camera)
	else:
		r['camera'].setVisible(False)

	shutter = shot_info['custom_attributes']['Shutter']
	if shutter:
		r['shutter'].setValue(shutter)
	else:
		r['shutter'].setVisible(False)

	r['extra_camera_info'].setValue(False)
	if not (camera_tilt or t_stop or focus or _filter or camera_height or camera or shutter):
		r['extra_camera_info'].setVisible(False)


	return
