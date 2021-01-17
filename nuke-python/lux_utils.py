import nuke
import nukescripts
import os, shutil

def updateToLatest(upto):
    for i in nuke.selectedNodes():
        if i.knob('file'):
           
            for x in range(upto):
                nukescripts.version_up()
        
            while i.error():
                nukescripts.version_down()

#updateToLatest(20)


#this is for archiving unused renders
#it will move all unused renders (any folder in the renders directory that is not being sourced by the main pipe in nuke)
def getConnectedReadPaths():

	def _browseDiscipline(_discipline):
	    discipline = _discipline.upper()
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
	        #_browse(path)
	        return path

	    except UnboundLocalError: #if the previous exceptions are not met, the path parameter becomes unrefferenced, so this kills it if no conditions are met.
	        pass



	writenode = nuke.selectedNode()
	connected = nuke.selectConnectedNodes()
	msg = ''
	files = []
	for i in nuke.selectedNodes():
	    if i.Class() == 'Read':
	        file = i['file'].value().replace('\\','/')
	        files.append(file)
	        msg += file+'\n\n'
	nuke.message(msg)

	move = nuke.ask('Should I move the unused renders to "unused" folder for you?')
	if move:
	    unusedFolderName = '__unused__'
	    renders = [i for i in files if ('/FINL/' in i)]
	    rendersDir = _browseDiscipline("06_RENDERS")
	    allRenders = [rendersDir.replace('\\','/')+'/'+i for i in os.listdir(rendersDir) if (unusedFolderName not in i)]
	    unused = (rendersDir + '/' + unusedFolderName).replace('\\','/')

	    try:
	        os.makedirs(unused)
	    except WindowsError:
	        pass

	    removes = []
	    keeps = []
	    for a in allRenders:
	        x = bool([i for i in renders if a in i])
	        if x:
	            keeps.append(a)

	    removes = list(set(allRenders) - set(keeps))
	    
	    if len(removes)>0:
	        for r in removes:
	            rname = r.split('/')[-1]
	            shutil.move(r, unused+'/'+rname)
	            #print r
            nuke.message('<a href =file:///{0}>Here is where I moved the unused renders!</a>'.format(unused))
	            
	        
	else:
	    pass
