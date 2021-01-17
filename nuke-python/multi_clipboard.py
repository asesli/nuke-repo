import os
import nuke

class multi_clipboard():

    def __init__(self):
        self.repo = "T://_Nuke_tools//global_clipboard//"
        self.saveName = "tempClipBoard"
        self.user = os.environ.get("USERNAME")
        self.savePath = self.repo + self.saveName+"_"+self.user+".nk"

    def getFolder(self):
        pluginPaths = nuke.pluginPath()
        pluginPathList = []

        for i in pluginPaths:
            if '.nuke' in i:
                pluginPathList.append(i)
                
        pluginFolder = pluginPathList[0].split('.nuke')[0]+'.nuke'
        multiCBFolder = pluginFolder +'/'+ 'multi_clipboard'
        return multiCBFolder     
        
        
    def paste(self, num):
        self.loadPath = self.getFolder()
        self.loadPath = str(self.loadPath) + '/'+'mCB_data_'+str(num)+'.nk'
        nuke.nodePaste(self.loadPath)
        

    
    def copy(self, num):
        ### Creates the MultiClipBoard folder inside of user's .nuke folder if it doesnt exist.
        self.loadPath = self.getFolder()
        osdir = nuke.callbacks.filenameFilter(self.loadPath)
        try:
            os.makedirs (osdir)
            print "Initial directories created"
        except OSError:
            pass
        
        
        ### Copies the script
        self.savePath = self.loadPath+'/'+'mCB_data_'+str(num)+'.nk'
        nuke.nodeCopy(self.savePath)
        
        print "Selected nodes saved to "+ self.savePath


