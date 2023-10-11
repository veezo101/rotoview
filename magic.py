import os
import shutil
import zipfile

import psutil


class Magic:
    def __init__(self, rotoview=None):
        self.rv = rotoview
        self.path = None

        try:
            with open('path.txt', 'r') as file:
                self.path = file.read().rstrip()
        except IOError:
            self.path = "path.txt not found"

    def updatePathField(self, process_name):
        try:
            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'] == process_name:
                    process_exe_path = psutil.Process(process.info['pid']).exe()
                    self.path = str(process_exe_path.rpartition('\\')[0])
                    file = open("path.txt", "w")
                    file.write(self.rv.pathfield.get())
                    file.close()
                    self.rv.pathfield.set(str(process_exe_path.rpartition('\\')[0]))
                    self.rv.statusLbl.config(text="Successfully detected path")
                    self.rv.LblPath.config(text=f"path.txt = {self.path}")
                    self.rv.SFXStatusLbl.config(text=self.getSfxState())
                    return
            self.rv.statusLbl.config(text="Failed to auto detect path. Make sure the client is open!")
        except Exception:
            self.rv.pathfield.set('')

    def updatePath(self):
        try:
            self.path = self.rv.pathfield.get()
            with open('path.txt', 'r') as file:
                file.write(self.path)
            self.rv.statusLbl.config(text='Successfully updated path')
            writtenFile = open('path.txt', 'r')
            self.path = writtenFile.read().rstrip()
            self.rv.LblPath.config(text=f"path.txt = {self.path}")
            self.rv.statusLbl.config(text='Successfully updated and read path')
            self.rv.SFXStatusLbl.config(text=self.getSfxState())
        except Exception as ex:
            self.rv.statusLbl.config(text="Error: {0} args: {1}".format(type(ex).__name__, ex.args))

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
                statusLbl.config(text="Invalid Game Path!")
                SFXStatusLbl.config(text=self.getSfxState())
                return
            if currentState == "muted":
                os.rename("{0}/SFX".format(path), "{0}/SFX-RotoSilent".format(path))
            if os.path.exists('{0}/SFX-RotoSilent'.format(path)):
                shutil.rmtree('{0}/SFX-RotoSilent'.format(path), ignore_errors=True)
            if os.path.exists('{0}/SFX-RotoOG'.format(path)):
                if os.path.exists('{0}/SFX'.format(path)):
                    shutil.rmtree('{0}/SFX'.format(path), ignore_errors=True)
                os.rename("{0}/SFX-RotoOG".format(path), "{0}/SFX".format(path))
            else:
                if not os.path.exists('{0}/SFX'.format(path)):
                    os.mkdir('{0}/SFX'.format(path))
            statusLbl.config(text="Successfully Restored SFX directory structure")
            SFXStatusLbl.config(text=self.getSfxState())
        except Exception as ex:
            if type(ex) == PermissionError:
                statusLbl.config(text="Permission Error. Close the game client and retry.")
                SFXStatusLbl.config(text=self.getSfxState())
                return
            statusLbl.config(text="Error: {0} args: {1}".format(type(ex).__name__, ex.args))
            SFXStatusLbl.config(text=self.getSfxState())

    def mute(self):
        try:
            currentState = self.getSfxState()
            if currentState == "invalidpath":
                self.rv.statusLbl.config(text="Invalid Game Path!")
                self.rv.SFXStatusLbl.config(text=self.getSfxState())
            if currentState == "muted":
                self.rv.statusLbl.config(text="Already muted!")
                self.rv.SFXStatusLbl.config(text=self.getSfxState())
                return
            if currentState == "raiseResetFlag" or currentState == "schrodinger" or currentState == "nosfxbutog":
                self.sfxResetFolder()
                self.rv.statusLbl.config(text="Folders Reset due to an error. Please try again")
            if currentState == "clean":
                with zipfile.ZipFile('./SilentSFX.zip', 'r') as silent_zip:
                    silent_zip.extractall('{0}/SFX-RotoSilent'.format(path))
                os.rename("{0}/SFX".format(path), "{0}/SFX-RotoOG".format(path))
                os.rename("{0}/SFX-RotoSilent".format(path), "{0}/SFX".format(path))
                self.rv.statusLbl.config(text="Client successfully muted except shiny")
                if os.path.exists('./assets/SFX/magic838.ogg'):
                    shutil.copy('./assets/SFX/magic838.ogg', "{0}/SFX/magic838.ogg".format(path))
                self.rv.statusLbl.config(text="Client successfully muted except custom shiny!")
            if currentState == "unmuted":
                os.rename("{0}/SFX".format(path), "{0}/SFX-RotoOG".format(path))
                self.rv.statusLbl.config(text="Moved current to OG")
                os.rename("{0}/SFX-RotoSilent".format(path), "{0}/SFX".format(path))
                self.rv.statusLbl.config(text="Client successfully muted except shiny")
                if (os.path.exists('./assets/SFX/magic838.ogg')):
                    shutil.copy('./assets/SFX/magic838.ogg', "{0}/SFX/magic838.ogg".format(path))
                    statusLbl.config(text="Client successfully muted except custom shiny!")
            self.rv.SFXStatusLbl.config(text=self.getSfxState())
        except FileNotFoundError as ex:
            # statusLbl.config(text="Failed to find folders (SFX-RotoOG or SFX-RotoSilent)")
            statusLbl.config(text="Error: {0} args: {1}".format(type(ex).__name__, ex.args))
            self.rv.SFXStatusLbl.config(text=self.getSfxState())
        except Exception as ex:
            statusLbl.config(text="Failed to mute client. Try again after closing the Client")
            self.rv.SFXStatusLbl.config(text=self.getSfxState())
            # debug
            # statusLbl.config(text="Error: {0} args: {1}".format(type(ex).__name__,ex.args))

    def unmute(self):
        try:
            currentState = self.getSfxState()
            if (currentState == "invalidpath"):
                statusLbl.config(text="Invalid Game Path!")
                SFXStatusLbl.config(text=self.getSfxState())
            if (currentState == "unmuted"):
                statusLbl.config(text="Already unmuted!")
                return
            if (currentState == "raiseResetFlag" or currentState == "schrodinger" or currentState == "nosfxbutog"):
                self.sfxResetFolder()
                statusLbl.config(text="Folders Reset due to an error. Please try again")
            if (currentState == "clean"):
                with zipfile.ZipFile('./SilentSFX.zip', 'r') as silent_zip:
                    silent_zip.extractall('{0}/SFX-RotoSilent'.format(path))
                statusLbl.config(text="Client successfully unmuted")
            if (currentState == "muted"):
                os.rename("{0}/SFX".format(path), "{0}/SFX-RotoSilent".format(path))
                os.rename("{0}/SFX-RotoOG".format(path), "{0}/SFX".format(path))
                statusLbl.config(text="Client successfully unmuted")
            SFXStatusLbl.config(text=self.getSfxState())
        except FileNotFoundError as ex:
            # statusLbl.config(text="Failed to find folders (SFX-RotoOG or SFX-RotoSilent)")
            statusLbl.config(text="Error: {0} args: {1}".format(type(ex).__name__, ex.args))
            SFXStatusLbl.config(text=self.getSfxState())
        except Exception as ex:
            self.rv.statusLbl.config(text="Failed to mute client. Try again after closing the Client")
            self.rv.SFXStatusLbl.config(text=self.getSfxState())
            # debug
            # statusLbl.config(text="Error: {0} args: {1}".format(type(ex).__name__,ex.args))
