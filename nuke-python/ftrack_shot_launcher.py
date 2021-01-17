import threading
import ftrack
import os
import glob
import nuke
import re
import sys
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QCompleter, QLineEdit, QStringListModel, QPixmap, QIcon
import urllib
import operator
from operator import itemgetter


import ftrack_api
import os
import getpass
import ftrack_api.symbol
import threading
import time


#Ftrack shot launcher for Nuke
#Artists can open tasks assigned to them through this UI.
#Retrieves Notes, Task type, shot name, and other important information
#This is essentially Ctrl+O combined with Ftrack
class FTrackShotLaunch(QtGui.QMainWindow):

    #Creates the main GUI and collects the results from ftrack
    def __init__(self):
        #self.user = ftrack.getUser(os.environ.get('USERNAME'))
        self.user = getpass.getuser()
        #if self.user == 'luxali':   self.user = 'johnm'


        os.environ['FTRACK_SERVER'] = 'https://domain.ftrackapp.com'
        os.environ['FTRACK_API_USER'] = self.user
        os.environ['FTRACK_API_KEY'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

        session = ftrack_api.Session()
        active_status = ("In Progress", "Not Started")
        assigned_tasks = session.query(
            'select status.name, status.color, name, priority.name, priority.color, parent from Task '
            'where (assignments any (resource.username = "{0}")) '
            'and project.status is active '
            'and name is "Compositing" '
            'and status.state.name in {1}'
            .format(self.user, active_status)
        )

        self.tasks = assigned_tasks.all()
        self.server_location = session.get('Location', ftrack_api.symbol.SERVER_LOCATION_ID)
        #self.task_items = []

        #######################################################################################


        #self.tasks = self.user.getTasks(states=[ftrack.IN_PROGRESS, ftrack.NOT_STARTED])

        self.sep = '-'*100
        self.result = []
        super(FTrackShotLaunch, self).__init__()

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('FTrack Shot Launch')
        # main button
        self.addButton = QtGui.QPushButton('Refresh Task List')
        self.addButton.clicked.connect(self.build_tabs_from_ftrack_tasks)

        # scroll area widget contents - layout
        self.scrollLayout = QtGui.QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QtGui.QVBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.scrollArea)

        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)
        self.setGeometry(300, 200, 440, 800)
        self.show()
        self.build_tabs_from_ftrack_tasks()
        #threading.Thread(target=self.build_tabs_from_ftrack_tasks).start()
    def clearLayout(self):
        _layout = self.scrollLayout
        while _layout.count():
            child = _layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())

    #returns a dict for each ftrack collection item
    #dict is used to build each tabs parameter
    #such as name, type, status, notes, etc.
    def ftrack_item_to_dict(self, task):
        '''
        shot_name = task['parent']['name']
        status = task['status']
        task_name = task['name']
        #notes = task['notes']
        thumbnail = task['parent']['thumbnail']
        priority = task['priority']
        parnt = task['parent']
        '''
        try:
            thumbnail = task['parent']['thumbnail']
            #thumbnail_url = self.server_location.get_thumbnail_url(thumbnail)
            thumbnail_url_tiny = self.server_location.get_thumbnail_url(thumbnail, size=150)
        except:
            #thumbnail_url_tiny = 'L:\\HAL\\LIVEAPPS\\apps\\Scripts\\NUKE\\icons\\ftrack_noimg.jpg'
            thumbnail_url_tiny = 'file:///L:/HAL/LIVEAPPS/apps/Scripts/NUKE/icons/ftrack_noimg.jpg'

        #print task_name, shot_name, status_name, thumbnail_url_tiny
        '''
        task_dict = { 
            'Task': task_name, 
            'Shot': shot_name, 
            'Status': status, 
            'Thumbnail': thumbnail_url_tiny, 
            #'Notes': notes, 
            'Priority': priority, 
            'Parent': parnt
        }
        '''
        task_dict = { 
            'Task': task['name'], 
            'Shot': task['parent']['name'], 
            'Status': task['status']['name'], 
            'Status_c': task['status']['color'], 
            'Priority': task['priority']['name'], 
            'Priority_c': task['priority']['color'], 
            'Thumbnail': thumbnail_url_tiny, 
            'Parent': task['parent']
        }
        '''
        for key, value in task_dict.iteritems() :
            print key, value
        '''
        #print shot_name, status_name, task_name, notes, thumbnail, priority

        return task_dict


    #Builds a taskTab for each item collected from ftrack
    #uses the dict to build each TaskTab 
    def build_tabs_from_ftrack_tasks(self):

        self.clearLayout()

        try:
            del prog
        except:
            pass
        if len(self.tasks) > 0:
            prog = nuke.ProgressTask('Retrieving available tasks from FTrack...')


            progIncr = 100.0 / len(self.tasks)

            
            for i, task in enumerate(self.tasks):
                self.result = []
                if prog.isCancelled():
                    #nuke.executeInMainThread(nuke.message, args=('Aborted',))
                    return
                #####Start


                #convert each task into a dictionary
                task_item = self.ftrack_item_to_dict(task)


                #use the task_item dictionary to populate TaskTab parameters
                self.scrollLayout.addRow( TaskTab(task_item) )


                #####End
                progMsg = ' '.join([task_item['Task'],task_item['Shot']])
                prog.setProgress(int(i * progIncr))
                prog.setMessage(progMsg)
        else:
            print "No Compositing tasks assigned to Artist. Talk to RJ!"

#Ftrack Task item, meant to mimick the task tabs from Ftrack. 
#TaskTab paramater input is a dict that contains all the info per task
#this dict is generated through collecting from ftrack, and sorting the collection into a list of dicts
#each dict in list is used to create TaskTab
class TaskTab(QtGui.QWidget):

    #Main layout for the Task Tab, similar to Ftrack tabs.
    #ShotName, TaskType, Priority, Thumbnail, Status, Notes, BidInfo
    def __init__( self, _task_items, parent=None):
        super(TaskTab, self).__init__(parent)

        font = QtGui.QFont()
        font.setPointSize(12)
        p_font = QtGui.QFont()
        p_font.setPointSize(7)


        self.imglink = urllib.urlopen(_task_items['Thumbnail']).read()
        self.image = QtGui.QImage()
        self.image.loadFromData(self.imglink)
        self.image_label = QtGui.QLabel(self)
        self.image_label.setPixmap(QtGui.QPixmap(self.image))


        #self.shot_label = QtGui.QLabel('''<a href='%s'>%s</a>'''%(_task_items['Task'], _task_items['Shot'].upper()))
        self.shot_label = QtGui.QLabel(_task_items['Shot'].upper())
        self.shot_label.setTextFormat(QtCore.Qt.RichText)
        self.shot_label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.shot_label.setOpenExternalLinks(True)
        self.shot_label.setFont(font)
        self.shot_label.setObjectName('shot_label')

        self.task_label = QtGui.QLabel(_task_items['Task'])
        self.task_label.setFont(QtGui.QFont().setPointSize(8))
        self.task_label.setStyleSheet("color:#00A6FF;")
        self.task_label.setObjectName('task_label')

        self.status_label = QtGui.QLabel()
        self.status_label.setFont(p_font)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.gray)
        self.status_label.setPalette(palette)
        self.status_label.setObjectName('status_label')
        self.status_label.setText(' '+_task_items['Status']+'             ')
        self.status_label.setStyleSheet("background-color: %s;"%(_task_items['Status_c']))


        self.priority_label = QtGui.QLabel()
        self.priority_label.setStyleSheet("background-color: %s;"%(_task_items['Priority_c']))
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.black)
        self.priority_label.setPalette(palette)
        self.priority_label.setFont(p_font)
        self.priority_label.setText('<b>'+_task_items['Priority']+' ')
        self.priority_label.setObjectName('priority_label')

        self.launch_shot_button = QtGui.QPushButton("Open Script...")
        self.launch_folder_button = QtGui.QPushButton("Open Renders...")

        latest_script = 0
        latest_render = 0
        _link_names = [i['name'] for i in _task_items['Parent']['link']]
        #_tl1 = '\\'.join(_link_names[0:-1])
        _tl1 = _link_names[0]
        _tl2 = _link_names[-1]
        _link = 'Q:\\{0}\\05_COMP\\{1}\\'.format(_tl1,_tl2)
        import glob, os
        if not os.path.isdir(_link):
            _tl0 = _tl2.split('_')[0]
            _link = 'Q:\\{0}\\{2}\\05_COMP\\{1}\\'.format(_tl1,_tl2,_tl0)

        #print _tl2
        os.chdir(_link)

        _scripts = [file for file in glob.glob("*.nk") if _tl2.lower()+'_v' in file.lower()]
        _scripts = sorted(_scripts)

        v_nums = [file.lower().split('_v')[-1].split('.')[0] for file in _scripts]
        v_nums = sorted(v_nums)

        latest_script = 'v'+str(v_nums[-1])
        slink = _link + _scripts[-1]



        self.quick_launch_shot_button = QtGui.QPushButton(str(latest_script))
        self.quick_launch_folder_button = QtGui.QPushButton("Latest")    

        #link_names = [i['name'] for i in _task_items['Parent']['link']]
        #tl1 = '\\'.join(link_names[0:-1])
        #tl2 = link_names[-1]
        #link = 'Q:\\{0}\\05_COMP\\{1}\\'.format(tl1,tl2)
        link = _task_items['Parent']['link']
        #print link
        '''
        for key, value in _task_items['Parent'].iteritems() :
            print key, str(value)
        '''

        self.launch_shot_button.setObjectName('launch_shot_button')
        self.launch_shot_button.clicked.connect(lambda: self.launch_shot_in_nuke(link))

        self.launch_folder_button.setObjectName('launch_folder_button')
        self.launch_folder_button.clicked.connect(lambda: self.launch_folder(link))

        self.quick_launch_shot_button.setObjectName('quick_launch_shot_button')
        self.quick_launch_shot_button.clicked.connect(lambda: self.quick_launch_shot_in_nuke(slink))

        self.quick_launch_folder_button.setObjectName('quick_launch_folder_button')
        self.quick_launch_folder_button.clicked.connect(lambda: self.launch_folder(link))

        #self.priority_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        shotLayout = QtGui.QGridLayout()
        shotLayout.setSpacing(0)

        shotLayout.addWidget(self.image_label, 0,0,4,2, QtCore.Qt.AlignTop)
        shotLayout.addWidget(self.status_label, 3,0,1,1, QtCore.Qt.AlignBottom)
        shotLayout.addWidget(self.priority_label, 3,1,1,1, QtCore.Qt.AlignBottom)
        shotLayout.addWidget(self.task_label, 0,2,1,2, QtCore.Qt.AlignTop)
        shotLayout.addWidget(self.shot_label, 1,2,1,2, QtCore.Qt.AlignTop)
        shotLayout.addWidget(self.launch_shot_button, 2,2,1,2)
        shotLayout.addWidget(self.launch_folder_button, 3,2,1,2)

        shotLayout.addWidget(self.quick_launch_shot_button, 2,4,1,1)
        shotLayout.addWidget(self.quick_launch_folder_button, 3,4,1,1)

        self.task_group = QtGui.QGroupBox()
        self.task_group.setObjectName('task_group')


        self.task_group.setMinimumHeight(120)
        self.task_group.setMinimumWidth(350)
        #bgcolor = _task_items['s_color']
        #self.task_group.setStyleSheet("background-color: %s;"%(bgcolor))
        self.task_group.setLayout(shotLayout)

        self.task_box = QtGui.QHBoxLayout()
        
        self.task_box.addStretch()
        self.task_box.addWidget(self.task_group)


        self.setLayout(self.task_box)
        self.setStyleSheet("background-color:#212121;")

    def quick_launch_shot_in_nuke(self, _link):
        try:
            #nuke.scriptClear()
            nuke.scriptClose()
            nuke.scriptOpen(_link)
        except:
            pass
        #print self.task_items
        #nuke.scriptClear()
        #nuke.scriptOpen(nk)
        return

    def launch_shot_in_nuke(self, _link):

        link_names = [i['name'] for i in _link if '_seq' not in i['name'].lower()]
        tl1 = '\\'.join(link_names[0:-1])
        tl2 = link_names[-1]

        link = 'Q:\\{0}\\05_COMP\\{1}\\'.format(tl1,tl2)
        if not os.path.isdir(link):
            tl0 = tl2.split('_')[0]
            link = 'Q:\\{0}\\{2}\\05_COMP\\{1}\\'.format(tl1,tl2,tl0)
        #print link

        try:
            nuke.scriptOpen('''{0}\\02_OUTPUT'''.format(link))
        except:
            pass
        #print self.task_items
        #nuke.scriptClear()
        #nuke.scriptOpen(nk)
        return
    def launch_folder(self, _link):

        link_names = [i['name'] for i in _link if '_seq' not in i['name'].lower()]
        #print link_names
        #print link_names
        tl1 = '\\'.join(link_names[0:-1])
        tl2 = link_names[-1]
        link = 'Q:\\{0}\\05_COMP\\{1}\\'.format(tl1,tl2)
        #print link
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
        _browse('{0}02_OUTPUT\\03_comp\\'.format(link))
        #print self.task_items
        #nuke.scriptClear()
        #nuke.scriptOpen(nk)
        return

'''
def Start_FTrackShotLaunch():
    m = FTrackShotLaunch()
    #m.show()
    return m


if __name__ == "__main__":
    import sys
    app=QtGui.QApplication.instance()    # checks if QApplication already exists
    if not app:    # create QApplication if it doesnt exist
        app = QtGui.QApplication(sys.argv)
    window = Start_FTrackShotLaunch()
    app.exec_()

'''
def showDialog():
    #app = QtGui.QApplication(sys.argv)

    ex = FTrackShotLaunch()
    app = ex(__name__)
    sys.exit(app.exec_())
    #ex.show()
    #win = FTrackShotLaunch(parent=QtGui.QApplication.activeWindow())
    #win.show()
#showDialog()
