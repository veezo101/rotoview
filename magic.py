import os
import shutil
import zipfile

import psutil


class Magic:
    def __init__(self, rotoview=None):
        self.rv = rotoview
        self.path = None

        try:
            self.path = self.rv.rotoconfig.getConfig('path').rstrip()
        except IOError:
            self.path = "config.json not found"
        except Exception as ex:
            raise ex

    def updatePathField(self, process_name):
        try:
            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'] == process_name:
                    process_exe_path = psutil.Process(process.info['pid']).exe()
                    self.rv.pathfield.set(str(process_exe_path.rpartition('\\')[0]))
                    self.path = self.rv.pathfield.get()
                    self.rv.rotoconfig.setConfig('path',self.path)
                    self.rv.tabber.statusLbl.configure(text="Successfully detected path")
                    self.rv.tabber.LblPath.configure(text=f"path.txt = {self.path}")
                    self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
                    return
            self.rv.tabber.statusLbl.configure(text="Failed to auto detect path. Make sure the client is open!")
        except Exception as ex:
            self.rv.pathfield.set('')
            raise ex

    def updatePath(self):
        try:
            self.path = self.rv.pathfield.get()
            self.rv.rotoconfig.setConfig('path',self.path)
            self.rv.tabber.LblPath.configure(text=f"path.txt = {self.path}")
            self.rv.tabber.statusLbl.configure(text='Successfully updated path')
            self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
        except Exception as ex:
            self.rv.tabber.statusLbl.configure(text="Error: {0} args: {1}".format(type(ex).__name__, ex.args))
            raise ex

    def getSfxState(self):
        if (not os.path.exists('{0}/PMU.exe'.format(self.path))):
            return "invalidpath"
        isExistSFX = os.path.exists('{0}/SFX'.format(self.path))
        isExistsRotoOG = os.path.exists('{0}/SFX-RotoOG'.format(self.path))
        isExistsRotoSilent = os.path.exists('{0}/SFX-RotoSilent'.format(self.path))
        if isExistSFX and not isExistsRotoSilent and isExistsRotoOG:
            return "muted"
        elif (isExistSFX and not isExistsRotoSilent and not isExistsRotoOG):
            return "clean"
        elif (isExistSFX and isExistsRotoSilent and not isExistsRotoOG):
            return "unmuted"
        elif (isExistSFX and isExistsRotoSilent and isExistsRotoOG):
            return "schrodinger"
        elif (not isExistSFX and isExistsRotoOG):
            return "nosfxbutog"
        else:
            return "raiseResetFlag"

    def sfxResetFolder(self):
        try:
            currentState = self.getSfxState()
            if (currentState == "invalidpath"):
                self.rv.tabber.statusLbl.configure(text="Invalid Game Path!")
                self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
                return
            if currentState == "muted":
                os.rename("{0}/SFX".format(self.path), "{0}/SFX-RotoSilent".format(self.path))
            if os.path.exists('{0}/SFX-RotoSilent'.format(self.path)):
                shutil.rmtree('{0}/SFX-RotoSilent'.format(self.path), ignore_errors=True)
            if os.path.exists('{0}/SFX-RotoOG'.format(self.path)):
                if os.path.exists('{0}/SFX'.format(self.path)):
                    shutil.rmtree('{0}/SFX'.format(self.path), ignore_errors=True)
                os.rename("{0}/SFX-RotoOG".format(self.path), "{0}/SFX".format(self.path))
            else:
                if not os.path.exists('{0}/SFX'.format(self.path)):
                    os.mkdir('{0}/SFX'.format(self.path))
            self.rv.tabber.statusLbl.configure(text="Successfully Restored SFX directory structure")
            self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
        except Exception as ex:
            if type(ex) == PermissionError:
                self.rv.tabber.statusLbl.configure(text="Permission Error. Close the game client and retry.")
                self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
                return
            self.rv.tabber.statusLbl.configure(text="Error: {0} args: {1}".format(type(ex).__name__, ex.args))
            self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
            raise ex

    def mute(self):
        try:
            currentState = self.getSfxState()
            if currentState == "invalidpath":
                self.rv.tabber.statusLbl.configure(text="Invalid Game Path!")
                self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
            if currentState == "muted":
                self.rv.tabber.statusLbl.configure(text="Already muted!")
                self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
                return
            if currentState == "raiseResetFlag" or currentState == "schrodinger" or currentState == "nosfxbutog":
                self.sfxResetFolder()
                self.rv.tabber.statusLbl.configure(text="Folders Reset due to an error. Please try again")
            if currentState == "clean":
                with zipfile.ZipFile('./assets/SFX/SilentSFX.zip', 'r') as silent_zip:
                    silent_zip.extractall('{0}/SFX-RotoSilent'.format(self.path))
                os.rename("{0}/SFX".format(self.path), "{0}/SFX-RotoOG".format(self.path))
                os.rename("{0}/SFX-RotoSilent".format(self.path), "{0}/SFX".format(self.path))
                self.rv.tabber.statusLbl.configure(text="Client successfully muted except shiny")
                if os.path.exists('./assets/SFX/magic838.ogg'):
                    shutil.copy('./assets/SFX/magic838.ogg', "{0}/SFX/magic838.ogg".format(self.path))
                self.rv.tabber.statusLbl.configure(text="Client successfully muted except custom shiny!")
            if currentState == "unmuted":
                os.rename("{0}/SFX".format(self.path), "{0}/SFX-RotoOG".format(self.path))
                self.rv.tabber.statusLbl.configure(text="Moved current to OG")
                os.rename("{0}/SFX-RotoSilent".format(self.path), "{0}/SFX".format(self.path))
                self.rv.tabber.statusLbl.configure(text="Client successfully muted except shiny")
                if (os.path.exists('./assets/SFX/magic838.ogg')):
                    shutil.copy('./assets/SFX/magic838.ogg', "{0}/SFX/magic838.ogg".format(self.path))
                    self.rv.tabber.statusLbl.configure(text="Client successfully muted except custom shiny!")
            self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
        except FileNotFoundError as ex:
            # self.rv.tabber.statusLbl.configure(text="Failed to find folders (SFX-RotoOG or SFX-RotoSilent)")
            self.rv.tabber.statusLbl.configure(text="Error: {0} args: {1}".format(type(ex).__name__, ex.args))
            self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
            raise ex
        except Exception as ex:
            self.rv.tabber.statusLbl.configure(text="Failed to mute client. Try again after closing the Client")
            self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
            # debug
            # self.rv.tabber.statusLbl.configure(text="Error: {0} args: {1}".format(type(ex).__name__,ex.args))
            raise ex

    def unmute(self):
        try:
            currentState = self.getSfxState()
            if (currentState == "invalidpath"):
                self.rv.tabber.statusLbl.configure(text="Invalid Game Path!")
                self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
            if (currentState == "unmuted"):
                self.rv.tabber.statusLbl.configure(text="Already unmuted!")
                return
            if (currentState == "raiseResetFlag" or currentState == "schrodinger" or currentState == "nosfxbutog"):
                self.sfxResetFolder()
                self.rv.tabber.statusLbl.configure(text="Folders Reset due to an error. Please try again")
            if (currentState == "clean"):
                with zipfile.ZipFile('./assets/SFX/SilentSFX.zip', 'r') as silent_zip:
                    silent_zip.extractall('{0}/SFX-RotoSilent'.format(self.path))
                self.rv.tabber.statusLbl.configure(text="Client successfully unmuted")
            if (currentState == "muted"):
                os.rename("{0}/SFX".format(self.path), "{0}/SFX-RotoSilent".format(self.path))
                os.rename("{0}/SFX-RotoOG".format(self.path), "{0}/SFX".format(self.path))
                self.rv.tabber.statusLbl.configure(text="Client successfully unmuted")
            self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
        except FileNotFoundError as ex:
            # self.rv.tabber.statusLbl.configure(text="Failed to find folders (SFX-RotoOG or SFX-RotoSilent)")
            self.rv.tabber.statusLbl.configure(text="Error: {0} args: {1}".format(type(ex).__name__, ex.args))
            self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
            raise ex
        except Exception as ex:
            self.rv.tabber.statusLbl.configure(text="Failed to mute client. Try again after closing the Client")
            self.rv.tabber.SFXStatusLbl.configure(text=self.getSfxState())
            # debug
            # self.rv.tabber.statusLbl.configure(text="Error: {0} args: {1}".format(type(ex).__name__,ex.args))
            raise ex
