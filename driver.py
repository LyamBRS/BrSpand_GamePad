#====================================================================#
# File Information
#====================================================================#
"""
    Gamepad.py
    ==========
    Summary:
    --------
    This file contains the high level classes and functions made to
    a Gamepad BrSpand card.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("driver.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
# from ...Utilities.Information import Information
# from ...Utilities.FileHandler import JSONdata, CompareKeys, AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import JSONdata, AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.addons import AddonFoundations, AddonInfoHandler, AddonEnum
from Libraries.BRS_Python_Libraries.BRS.PnP.controls import Controls
from Libraries.BRS_Python_Libraries.BRS.Hardware.UART.receiver import UART
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
# LoadingLog.Import('KivyMD')
#endregion
from Programs.Local.FileHandler.Profiles import ProfileHandler
#====================================================================#
# Variables
#====================================================================#
_EmptyJsonStructure:dict = {
    "version" : 0.1,
    "name" : "Gamepad",
    "saved-profiles" : {

    }
}

def FakeButtonCallBack(*args):
    return True

def FakeAxisCallback(*args):
    return 1

hardwareControlsTemplate:dict = {
                        "axes" : { 
                                "left-x-positive" : {  "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : FakeAxisCallback},
                                "left-x-negative" : { "binded" : False, 
                                                 "bindedTo" : None,
                                                 "getter" : FakeAxisCallback},
                                "left-y-positive" : {  "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : FakeAxisCallback},
                                "left-y-negative" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : FakeAxisCallback},
                                "right-x-positive" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : FakeAxisCallback},
                                "right-x-negative" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : FakeAxisCallback},
                                "right-y-positive" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : FakeAxisCallback},
                                "right-y-negative" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : FakeAxisCallback}
                        },
                        "buttons" : {
                                    "left-joystick-button" : {  "binded" : False, 
                                                                "bindedTo" : None,
                                                                "getter" : FakeButtonCallBack},
                                    "right-joystick-button" : {  "binded" : False, 
                                                                "bindedTo" : None,
                                                                "getter" : FakeButtonCallBack},
                                    "switch1" : {  "binded" : False, 
                                                    "bindedTo" : None,
                                                    "getter" : FakeButtonCallBack},
                                    "switch2" : { "binded" : False, 
                                                    "bindedTo" : None,
                                                    "getter" : FakeButtonCallBack},
                                    "switch3" : { "binded" : False, 
                                                    "bindedTo" : None,
                                                    "getter" : FakeButtonCallBack},
                                    "switch4" : { "binded" : False, 
                                                    "bindedTo" : None,
                                                    "getter" : FakeButtonCallBack},
                                    "switch5" : { "binded" : False, 
                                                    "bindedTo" : None,
                                                    "getter" : FakeButtonCallBack}
                        } 
}

profileExample = {
    "hardware" : {
                    "axes" : { 
                                "left-x-positive" : {  "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "left-x-negative" : { "binded" : False, 
                                                 "bindedTo" : None,
                                                 "getter" : None},
                                "left-y-positive" : {  "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "left-y-negative" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "right-x-positive" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "right-x-negative" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "right-y-positive" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "right-y-negative" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None}
                            },
                    "buttons" : {
                                "left-joystick-button" : {  "binded" : False, 
                                                            "bindedTo" : None,
                                                            "getter" : None},
                                "right-joystick-button" : {  "binded" : False, 
                                                            "bindedTo" : None,
                                                            "getter" : None},
                                "switch1" : {  "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "switch2" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "switch3" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "switch4" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "switch5" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None}
                    } 
    },
    "actions" : {

    }
}

#====================================================================#
# Classes
#====================================================================#
class Gamepad(AddonFoundations):
    #region   --------------------------- DOCSTRING
    """
        Gamepad:
        ==============
        Summary:
        --------
        This class handles the backend of trying
        to interface an Gamepad addon card
        with the Raspberry Pi.
    """
    #endregion
    #region   --------------------------- MEMBERS
    profileData:JSONdata = None

    hardwareControls:dict = {
        "axes" : {
                    "left-x-positive" : {  "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : FakeAxisCallback},
                    "left-x-negative" : { "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : FakeAxisCallback},
                    "left-y-positive" : {  "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : FakeAxisCallback},
                    "left-y-negative" : { "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : FakeAxisCallback},
                    "right-x-positive" : { "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : FakeAxisCallback},
                    "right-x-negative" : { "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : FakeAxisCallback},
                    "right-y-positive" : { "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : FakeAxisCallback},
                    "right-y-negative" : { "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : FakeAxisCallback}
                 },
                    "buttons" : {
                                "left-joystick-button" : {  "binded" : False, 
                                                            "bindedTo" : None,
                                                            "getter" : FakeButtonCallBack},
                                "right-joystick-button" : {  "binded" : False, 
                                                            "bindedTo" : None,
                                                            "getter" : FakeButtonCallBack},
                                "switch1" : {  "binded" : False, 
                                                "bindedTo" : None,
                                                "getter" : FakeButtonCallBack},
                                "switch2" : { "binded" : False, 
                                                "bindedTo" : None,
                                                "getter" : FakeButtonCallBack},
                                "switch3" : { "binded" : False, 
                                                "bindedTo" : None,
                                                "getter" : FakeButtonCallBack},
                                "switch4" : { "binded" : False, 
                                                "bindedTo" : None,
                                                "getter" : FakeButtonCallBack},
                                "switch5" : { "binded" : False, 
                                                "bindedTo" : None,
                                                "getter" : FakeButtonCallBack}
                    } 
    }

    loadedProfileName:str = None

    addonInformation:AddonInfoHandler = None
    #endregion
    #region   --------------------------- METHODS
    #region ----------------------- ADDON
    def Launch() -> Execution:
        """
            Launch:
            =======
            Summary:
            --------
            Launches the Gamepad addon.
            returns Execution to indicate how
            the launch went.

            Returns:
            --------
            - `Execution.Passed` = Addon was launched.
            - `Execution.Failed` = Error occured
            - `Execution.Incompatibility` = Failed to verify for compatibility.
        """
        Debug.Start("Gamepad -> Launch")

        Debug.Log("Creating AddonInfoHandler")
        Gamepad.addonInformation = AddonInfoHandler(
            name="Gamepad",
            description="BrSpand Gamepad card giving extra hardware controls to your devices",
            version="0.0.1",
            type="brspand",
            repository="https://github.com/LyamBRS/BrSpand_GamePad.git",
            hasHardwareButtons= True,
            hasHardwareAxes= True,
            readsSoftwareButtons= False,
            readsSoftwareAxes= False,
            MDIcon= "gamepad-variant",
            LaunchFunction = Gamepad.Launch,
            StopFunction = Gamepad.Stop,
            UninstallFunction = Gamepad.Uninstall,
            UpdateFunction = Gamepad.Update,
            GetStateFunction = Gamepad.GetState,
            ClearProfileFunction= Gamepad.ClearProfile,
            SaveProfile = Gamepad.SaveProfile,
            ChangeProfile= Gamepad.ChangeProfile,
            LoadProfile= Gamepad.LoadProfile,
            UnloadProfile= Gamepad.UnloadProfile,
            PeriodicCallback= Gamepad.PeriodicCallback,
            GetAllHardwareControls= Gamepad.GetAllHardwareControls,
            GetAllSoftwareActions= Gamepad.GetAllSoftwareActions,
            ChangeButtonActionBinding= Gamepad.ChangeButtonActionBinding,
            ChangeAxisActionBinding= Gamepad.ChangeAxisActionBinding,
            UnbindButtonBinding= Gamepad.UnbindButtonBinding,
            UnbindAxisBinding= Gamepad.UnbindAxisBinding,
            ChangeButtonBinding= Gamepad.ChangeButtonBinding,
            ChangeAxisBinding= Gamepad.ChangeAxisBinding
        )

        Debug.Log("Checking if we need to load in a current profile.")
        profileName = ProfileHandler.currentName
        if(profileName != None):
            Gamepad.loadedProfileName = profileName
            Gamepad.LoadProfile(profileName)

        result = Gamepad.VerifyForExecution()
        if(result != Execution.Passed):
            Debug.Error("The BrSpand card cannot run on your device.")
            Debug.Log("Adding addon to application...")
            Gamepad.addonInformation.DockAddonToApplication(False)
            Debug.End()
            return result

        result = UART.StartDriver()
        if(result == Execution.Failed):
            Debug.Error("Failed to start backend driver UART")
            Gamepad.addonInformation.DockAddonToApplication(False)
            Debug.End()
            return Execution.Failed

        Debug.Log("Addon started successfully.")
        Debug.Log("Adding addon to application...")
        Gamepad.addonInformation.DockAddonToApplication(True)
        Gamepad.state = True
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def Stop() -> Execution:
        """
            Stop:
            ==========
            Summary:
            --------
            Stops the addon from running.
            Closes the thread that is running it.
            Gone, reduced to atoms.
            Oh, and it unbinds stuff too.
        """
        Debug.Start("Gamepad -> Stop")

        if(Gamepad.state == True):
            Debug.Log("Stopping Reader")
            # result = ADXL343.StopDriver()
            # if(result != Execution.Passed):
                # Debug.Error("Error when trying to stop Gamepad")
                # Debug.End()
                # return Execution.Failed
            Debug.Log("Gamepad is now OFF")
            Gamepad.profileData.SaveFile()
            Gamepad.state = False
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. Gamepad is not running.")
            Debug.End()
            return Execution.Unecessary
    # -----------------------------------
    def GetAllHardwareControls() -> Execution:
        """
            GetAllHardwareControls:
            =======================
            Summary:
            --------
            Returns a dictionary of all
            the current hardware controls
            of this addon.

            Returns:
            --------
            - `Execution.Failed` = Something fucked up.
            - `dict` see :ref:`hardwareControls`
        """
        Debug.Start("Gamepad -> GetAllHardwareControls")
        if(Gamepad.state == True):
            Debug.Log("Returning proper values")
            Debug.End()
            return Gamepad.hardwareControls
        else:
            Debug.Log("Unecessary. Gamepad is not running.")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def LoadProfile(profileToLoad: str) -> Execution:
        """
            LoadProfile:
            ============
            Summary:
            --------
            This function loads a profile
            saved in the JSONs of this addon.
            if no profiles are found with this
            name, default values are loaded
            and the profile is created.
        """
        Debug.Start("Gamepad -> LoadProfile")

        if(Gamepad.state == True):
            Debug.Log(f"Trying to load {profileToLoad} from Profiles.json")

            try:
                profile = Gamepad.profileData.jsonData["saved-profiles"][profileToLoad]
                Debug.Log(f"{profileToLoad} was found in the JSON.")
            except:
                Debug.Log(f"{profileToLoad} doesn't exist in the JSON... Creating it.")
                Gamepad._AddNewProfile(profileToLoad)

                Debug.Log("Saving JSON file...")
                saved = Gamepad.profileData.SaveFile()
                if(not saved):
                    Debug.Error("Failed to save JSON file...")
                    Debug.End()
                    return Execution.Failed
                Debug.Log("Success")
                profile = Gamepad.profileData.jsonData["saved-profiles"][profileToLoad]

            Debug.Log(f"Loading {profileToLoad}'s data.")
            Gamepad.loadedProfileName = profileToLoad
            result = Gamepad._LoadProfileBindsInApplication()
            if(result != Execution.Passed):
                Debug.Error(f"Failed to keybinds of {Gamepad.loadedProfileName} into the Controls class.")
                Debug.End()
                return result
            
            Debug.Log("Profile loaded in successfully.")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Warn("Gamepad is not running.")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def UnloadProfile(profileToUnload: str) -> Execution:
        """
            UnloadProfile:
            ============
            Summary:
            --------
            Unloads a specified profile from
            the addon. This does not turn off
            the addon.

            Usually used when someone is logging
            out of their profiles.
        """
        Debug.Start("Gamepad -> UnloadProfile")

        if(Gamepad.state == True):
            Debug.Log(f"Unloading the current profile.")
            result = Gamepad._UnbindEverything()
            if(result != Execution.Passed):
                Debug.Error(f"_UnbindEverything returned error code: {result}")
                Debug.End()
                return result

            Debug.Log("Clearing saved profile's name.")
            Gamepad.loadedProfileName = None
        else:
            Debug.Warn("Gamepad is not running.")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def SaveProfile(profileToSave: str = None) -> Execution:
        """
            SaveProfile:
            ============
            Summary:
            --------
            Attempts to save either the
            currently loaded profile, or
            a specific profile with the
            currently loaded informations.
        """
        Debug.Start("Gamepad -> SaveProfile")

        if(Gamepad.state == True):
            if(Gamepad.loadedProfileName == None and profileToSave == None):
                Debug.Error("No profiles were loaded in the class.")
                Debug.End()
                return Execution.Failed

            if(profileToSave == None):
                Debug.Log("Saving loaded profile.")
                profileToSave = Gamepad.loadedProfileName

            existing = Gamepad._DoesProfileExist(profileToSave)
            if(not existing):
                Debug.Log(f"{profileToSave} does not exist. Creating it.")
                Gamepad._AddNewProfile(profileToSave)
                Gamepad._PutBindsInProfile(profileToSave)
            else:
                Debug.Log(f"Putting live binds in {profileToSave}")
                Gamepad._PutBindsInProfile(profileToSave)

            saved = Gamepad.profileData.SaveFile()
            if(not saved):
                Debug.Error("Saving failed.")
                Debug.End()
                return Execution.Failed

            Debug.Log(">>> SUCCESS")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. Gamepad is not running.")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def ClearProfile(profileToClear: str) -> Execution:
        """
            ClearProfile:
            =============
            Summary:
            --------
            Attempts to clear a given profile
            from the cache of this addon.
        """
        Debug.Start("Gamepad -> ClearProfile")
        if(Gamepad.profileData.jsonData == None):
            Debug.Error("No json is loaded. Gamepad cannot delete anything.")
            Debug.End()
            return Execution.ByPassed

        existing = Gamepad._DoesProfileExist(profileToClear)
        if(not existing):
            Debug.Warn(f"Gamepad has no cached data for {profileToClear}")
            Debug.End()
            return Execution.Unecessary

        savedProfiles:dict = Gamepad.profileData.jsonData["saved-profiles"]
        savedProfiles.pop(profileToClear)
        Debug.Log(f"{profileToClear} no longer exists in Gamepad's cached profiles.")
        Gamepad.profileData.jsonData["saved-profiles"] = savedProfiles
        Gamepad.profileData.SaveFile()
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def ChangeAxisBinding(nameOfSoftwareAxis: str, nameOfHardwareAxis: str) -> Execution:
        """
            ChangeAxisBinding:
            ==================
            Summary:
            --------
            This method attempts to firstly
            un-bind anything binded to
            :ref:`nameOfHardwareAxis` then
            tries to bind it to :ref:`nameOfSoftwareAxis`

            Arguments:
            ----------
            - `nameOfSoftwareAxis` : Axis taken from SoftwareAxis in controls.py
            - `nameOfHardwareAxis` : Hardware axis to bind to :ref:`nameOfSoftwareAxis`
        """
        Debug.Start("Gamepad -> ChangeAxisBinding")

        if(Gamepad.state == True):
            result = Gamepad.UnbindAxisBinding(nameOfSoftwareAxis)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Failed to unbind software axis: {nameOfSoftwareAxis}")
                Debug.End()
                return Execution.Failed

            result = Gamepad._UnbindHardwareAxis(nameOfHardwareAxis)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Failed to unbind hardware axis: {nameOfHardwareAxis}")
                Debug.End()
                return Execution.Failed

            Debug.Log(f"Gamepad no longer holds bindings for the software axis: {nameOfSoftwareAxis} as well as the hardware axis: {nameOfHardwareAxis}")

            result = Gamepad._BindAxis(nameOfSoftwareAxis, nameOfHardwareAxis)
            if(result != Execution.Passed):
                Debug.Error(f"Something went wrong when trying to bind {nameOfHardwareAxis} to {nameOfSoftwareAxis}")
                Debug.End()
                return result

            Debug.Log(f"Saving {Gamepad.loadedProfileName}'s new binds.")
            Gamepad._PutBindsInProfile(Gamepad.loadedProfileName)

            saved = Gamepad.profileData.SaveFile()
            if(not saved):
                Debug.Log("Failed to save Profile.json")
                Debug.End()
                return Execution.Crashed

            Debug.Log(">>> Success")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. ADXL343 is not running.")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def ChangeButtonBinding(nameOfSoftwareButton: str, nameOfHardwareButton: str) -> Execution:
        """
            ChangeButtonBinding:
            ==================
            Summary:
            --------
            This method attempts to firstly
            un-bind anything binded to
            :ref:`nameOfHardwareButton` then
            tries to bind it to :ref:`nameOfSoftwareButton`

            Arguments:
            ----------
            - `nameOfSoftwareButton` : Axis taken from SoftwareButtons in controls.py
            - `nameOfHardwareButton` : Hardware axis to bind to :ref:`nameOfSoftwareButton`
        """
        Debug.Start("Gamepad -> ChangeButtonBinding")

        if(Gamepad.state == True):
            result = Gamepad.UnbindButtonBinding(nameOfSoftwareButton)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Failed to unbind software button: {nameOfSoftwareButton}")
                Debug.End()
                return Execution.Failed

            result = Gamepad._UnbindHardwareButton(nameOfHardwareButton)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Failed to unbind hardware button: {nameOfHardwareButton}")
                Debug.End()
                return Execution.Failed

            Debug.Log(f"Gamepad no longer holds bindings for the software button: {nameOfSoftwareButton} as well as the hardware button: {nameOfHardwareButton}")

            result = Gamepad._BindButton(nameOfSoftwareButton, nameOfHardwareButton)
            if(result != Execution.Passed):
                Debug.Error(f"Something went wrong when trying to bind {nameOfHardwareButton} to {nameOfSoftwareButton}")
                Debug.End()
                return result

            Debug.Log(f"Saving {Gamepad.loadedProfileName}'s new binds.")
            Gamepad._PutBindsInProfile(Gamepad.loadedProfileName)

            saved = Gamepad.profileData.SaveFile()
            if(not saved):
                Debug.Log("Failed to save Profile.json")
                Debug.End()
                return Execution.Crashed

            Debug.Log(">>> Success")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. Gamepad is not running.")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def UnbindAxisBinding(nameOfSoftwareAxis:str) -> Execution:
        """
            UnbindAxisBinding:
            ==================
            Summary:
            --------
            This method attempts to
            un-bind anything binded to
            :ref:`nameOfSoftwareAxis`.

            Arguments:
            ----------
            - `nameOfSoftwareAxis` : Axis taken from SoftwareAxis in controls.py that needs to be unbinded.
        """
        Debug.Start("Gamepad -> UnbindAxisBinding")

        if(Gamepad.state):
            whateverAxisHadItBinded = Gamepad._WhoHasThatAxisBinded(nameOfSoftwareAxis)
            if(whateverAxisHadItBinded == Execution.Unecessary):
                Debug.Log(f"{nameOfSoftwareAxis} isn't currently binded by the Gamepad.")
                Debug.End()
                return Execution.Unecessary

            result = Gamepad._UnbindSoftwareAxis(nameOfSoftwareAxis, whateverAxisHadItBinded)
            if(result != Execution.Passed):
                Debug.Log(f"Error occured when unbinding {nameOfSoftwareAxis}. Return code: {result}")

            Debug.Log("Updating profile with new informations.")
            Gamepad._PutBindsInProfile(Gamepad.loadedProfileName)
            Gamepad.profileData.SaveFile()
            Debug.Log(">>> Success")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Warn("Gamepad is not running.")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def UnbindButtonBinding(nameOfSoftwareButton:str) -> Execution:
        """
            UnbindButtonBinding:
            ====================
            Summary:
            --------
            This method attempts to
            un-bind anything binded to
            :ref:`nameOfSoftwareButton`.

            Arguments:
            ----------
            - `nameOfSoftwareButton` : button taken from nameOfSoftwareButton in controls.py that needs to be unbinded.
        """
        Debug.Start("Gamepad -> UnbindButtonBinding")

        if(Gamepad.state):
            whateverButtonHadItBinded = Gamepad._WhoHasThatButtonBinded(nameOfSoftwareButton)
            if(whateverButtonHadItBinded == Execution.Unecessary):
                Debug.Log(f"{nameOfSoftwareButton} isn't currently binded by the Gamepad.")
                Debug.End()
                return Execution.Unecessary

            result = Gamepad._UnbindSoftwareButton(nameOfSoftwareButton, whateverButtonHadItBinded)
            if(result != Execution.Passed):
                Debug.Log(f"Error occured when unbinding {nameOfSoftwareButton}. Return code: {result}")

            Debug.Log("Updating profile with new informations.")
            Gamepad._PutBindsInProfile(Gamepad.loadedProfileName)
            Gamepad.profileData.SaveFile()
            Debug.Log(">>> Success")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Warn("Gamepad is not running.")
            Debug.End()
            return Execution.ByPassed
    #endregion
    #region --------------------- PRIVATE
    def _UnbindEverything():
        """
            _UnbindEverything:
            ===================
            Summary:
            --------
            This private method's goal is
            to unload all the binds as
            well as the current profile.
        """
        Debug.Start("_UnbindEverything")

        for hardwareAxis, data in Gamepad.hardwareControls["axes"].items():
            Debug.Log(f"Unbinding {hardwareAxis} from the Gamepad.")
            result = Gamepad._UnbindHardwareAxis(hardwareAxis)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Fatal error occured when trying to unbind {hardwareAxis}. Return code: {result}")
                Debug.End()
                return Execution.Failed
            
        for hardwareButton, data in Gamepad.hardwareControls["buttons"].items():
            Debug.Log(f"Unbinding {hardwareButton} from the Gamepad.")
            result = Gamepad._UnbindHardwareButton(hardwareButton)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Fatal error occured when trying to unbind {hardwareButton}. Return code: {result}")
                Debug.End()
                return Execution.Failed

        Debug.Log("Everything has been un-binded.")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _UnbindHardwareAxis(nameOfHardwareAxis:str):
        """
            _UnbindHardwareAxis:
            ============
            Summary:
            --------
            This method tries to unbind
            a given hardware axis both from
            local dictionaries as well as from
            the Controls class.
        """
        Debug.Start("_UnbindHardwareAxis")

        Debug.Log(f"Getting what is binded to {nameOfHardwareAxis}")
        whatItsBindedTo = Gamepad.hardwareControls["axes"][nameOfHardwareAxis]["bindedTo"]
        if(whatItsBindedTo == None):
            Debug.Log(f"{nameOfHardwareAxis} isn't binded to any software axis.")
            Debug.End()
            return Execution.Passed

        Debug.Log(f"Unbinding {nameOfHardwareAxis} from {whatItsBindedTo}")
        result = Controls.UnbindAxis("Gamepad", nameOfSoftwareAxis=whatItsBindedTo)
        if(result != Execution.Passed):
            Debug.Log(f"Failed to unbind {nameOfHardwareAxis} from {whatItsBindedTo}")
            Debug.End()
            return result

        Gamepad.hardwareControls["axes"][nameOfHardwareAxis]["binded"] = False
        Gamepad.hardwareControls["axes"][nameOfHardwareAxis]["bindedTo"] = None
        Debug.Log(f"{nameOfHardwareAxis} is now default values.")

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _UnbindHardwareButton(nameOfHardwareButton:str):
        """
            _UnbindHardwareButton:
            ============
            Summary:
            --------
            This method tries to unbind
            a given hardware button both from
            local dictionaries as well as from
            the Controls class.
        """
        Debug.Start("_UnbindHardwareAxis")

        Debug.Log(f"Getting what is binded to {nameOfHardwareButton}")
        whatItsBindedTo = Gamepad.hardwareControls["buttons"][nameOfHardwareButton]["bindedTo"]
        if(whatItsBindedTo == None):
            Debug.Log(f"{nameOfHardwareButton} isn't binded to any software buttons.")
            Debug.End()
            return Execution.Passed

        Debug.Log(f"Unbinding {nameOfHardwareButton} from {whatItsBindedTo}")
        result = Controls.UnbindButton("Gamepad", nameOfSoftwareButton=whatItsBindedTo)
        if(result != Execution.Passed):
            Debug.Log(f"Failed to unbind {nameOfHardwareButton} from {whatItsBindedTo}")
            Debug.End()
            return result

        Gamepad.hardwareControls["buttons"][nameOfHardwareButton]["binded"] = False
        Gamepad.hardwareControls["buttons"][nameOfHardwareButton]["bindedTo"] = None
        Debug.Log(f"{nameOfHardwareButton} is now default values.")

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _UnbindSoftwareAxis(nameOfSoftwareAxis:str, nameOfHardwareAxis:str):
        """
            _UnbindSoftwareAxis:
            ============
            Summary:
            --------
            This method tries to unbind
            a given hardware axis both from
            local dictionaries as well as from
            the Controls class.
        """
        Debug.Start("_UnbindSoftwareAxis")

        Debug.Log(f"Unbinding {nameOfHardwareAxis} from {nameOfSoftwareAxis} in the Controls class.")
        result = Controls.UnbindAxis("Gamepad", nameOfSoftwareAxis=nameOfSoftwareAxis)
        if(result != Execution.Passed):
            Debug.Log(f"Failed to unbind {nameOfHardwareAxis} from {nameOfSoftwareAxis}")
            Debug.End()
            return result

        Gamepad.hardwareControls["axes"][nameOfHardwareAxis]["binded"] = False
        Gamepad.hardwareControls["axes"][nameOfHardwareAxis]["bindedTo"] = None
        Debug.Log(f"{nameOfHardwareAxis} is now default values.")

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _UnbindSoftwareButton(nameOfSoftwareButton:str, nameOfHardwareButton:str):
        """
            _UnbindSoftwareButton:
            ============
            Summary:
            --------
            This method tries to unbind
            a given hardware button both from
            local dictionaries as well as from
            the Controls class.
        """
        Debug.Start("_UnbindSoftwareButton")

        Debug.Log(f"Unbinding {nameOfHardwareButton} from {nameOfHardwareButton} in the Controls class.")
        result = Controls.UnbindButton("Gamepad", nameOfSoftwareAxis=nameOfHardwareButton)
        if(result != Execution.Passed):
            Debug.Log(f"Failed to unbind {nameOfHardwareButton} from {nameOfHardwareButton}")
            Debug.End()
            return result

        Gamepad.hardwareControls["buttons"][nameOfHardwareButton]["binded"] = False
        Gamepad.hardwareControls["buttons"][nameOfHardwareButton]["bindedTo"] = None
        Debug.Log(f"{nameOfHardwareButton} is now default values.")

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _BindAxis(nameOfSoftwareAxis:str, nameOfHardwareAxis:str):
        """
            _BindAxis:
            ============
            Summary:
            --------
            This method tries to bind
            a given hardware axis both from
            local dictionaries as well as from
            the Controls class.
        """
        Debug.Start("_BindAxis")

        Debug.Log(f"Binding {nameOfHardwareAxis} to {nameOfSoftwareAxis} in Controls class.")
        result = Controls.BindAxis("Gamepad", nameOfSoftwareAxis, nameOfHardwareAxis, Gamepad.hardwareControls["axes"][nameOfHardwareAxis]["getter"])
        if(result != Execution.Passed):
            Debug.Log(f"Failed to bind {nameOfHardwareAxis} to {nameOfSoftwareAxis} with error code: {result}")
            Debug.End()
            return result

        Gamepad.hardwareControls["axes"][nameOfHardwareAxis]["binded"] = True
        Gamepad.hardwareControls["axes"][nameOfHardwareAxis]["bindedTo"] = nameOfSoftwareAxis
        Debug.Log(f"{nameOfHardwareAxis} is now binded to {nameOfSoftwareAxis}.")

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _BindButton(nameOfSoftwareButton:str, nameOfHardwareButton:str):
        """
            _BindButton:
            ============
            Summary:
            --------
            This method tries to bind
            a given hardware axis both from
            local dictionaries as well as from
            the Controls class.
        """
        Debug.Start("_BindAxis")

        Debug.Log(f"Binding {nameOfHardwareButton} to {nameOfHardwareButton} in Controls class.")
        result = Controls.BindButton("Gamepad", nameOfHardwareButton, nameOfHardwareButton, Gamepad.hardwareControls["buttons"][nameOfHardwareButton]["getter"])
        if(result != Execution.Passed):
            Debug.Log(f"Failed to bind {nameOfHardwareButton} to {nameOfHardwareButton} with error code: {result}")
            Debug.End()
            return result

        Gamepad.hardwareControls["buttons"][nameOfHardwareButton]["binded"] = True
        Gamepad.hardwareControls["buttons"][nameOfHardwareButton]["bindedTo"] = nameOfHardwareButton
        Debug.Log(f"{nameOfHardwareButton} is now binded to {nameOfHardwareButton}.")

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _WhoHasThatAxisBinded(nameOfSoftwareAxis:str):
        """
            _WhoHasThatAxisBinded:
            ======================
            Summary:
            --------
            Checks if any of the hardware
            axis binded that software axis.
            If so, the name of the hardware
            axis is returned.
        """
        Debug.Start("_WhoHasThatAxisBinded")

        for hardwareAxis, axisData in Gamepad.hardwareControls["axes"].items():
            if(axisData["bindedTo"] == nameOfSoftwareAxis):
                Debug.Log(f"{nameOfSoftwareAxis} is binded to {hardwareAxis}")
                Debug.End()
                return hardwareAxis

        Debug.Log(f"No axis has {nameOfSoftwareAxis} binded to them.")
        Debug.End()
        return Execution.Unecessary
    # -----------------------------------
    def _WhoHasThatButtonBinded(nameOfSoftwareButton:str):
        """
            _WhoHasThatButtonBinded:
            ======================
            Summary:
            --------
            Checks if any of the hardware
            axis binded that software axis.
            If so, the name of the hardware
            axis is returned.
        """
        Debug.Start("_WhoHasThatButtonBinded")

        for hardwareButton, axisData in Gamepad.hardwareControls["buttons"].items():
            if(axisData["bindedTo"] == nameOfSoftwareButton):
                Debug.Log(f"{nameOfSoftwareButton} is binded to {hardwareButton}")
                Debug.End()
                return hardwareButton

        Debug.Log(f"No button has {nameOfSoftwareButton} binded to them.")
        Debug.End()
        return Execution.Unecessary
    # -----------------------------------
    def _InitializeProfileJson() -> Execution:
        """
            _InitializeProfileJson:
            =======================
            Summary:
            --------
            Attempts to load a JSON at a specific
            path or creates it if it doesn't exist.
        """
        Debug.Start("_InitializeProfileJson")

        path = os.getcwd()
        path = AppendPath(path, "/BrSpand/Drivers/Gamepad/")

        Gamepad.profileData = JSONdata("Profiles", path)
        if(Gamepad.profileData.jsonData == None):
            Debug.Warn("No profile json file found for Gamepad")
            Gamepad.profileData.CreateFile(_EmptyJsonStructure)
            Gamepad.profileData = JSONdata("Profiles", path)
            if(Gamepad.profileData.jsonData == None):
                Debug.Error("Failed to create and load JSON after second attempt.")
                Debug.End()
                return Execution.Failed
            Debug.Log("New JSON created.")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _LoadProfileBindsInApplication() -> Execution:
        """
            _LoadProfileBindsInApplication:
            ===============================
            Summary:
            --------
            Loads a profile's saved hardware binds
            into the application's Controls class.

            Will return errors if some could not be
            loaded.

            Will update the hardwareControl dictionary
            of this class with what could be loaded
            and what couldn't.
        """ 
        Debug.Start("_LoadProfileBindsInApplication")

        if(Gamepad.loadedProfileName == None):
            Debug.Error("saved profile name is None. Something fucked up.")
            Debug.End()
            return Execution.Failed

        profile = Gamepad.profileData.jsonData["saved-profiles"][Gamepad.loadedProfileName]
        hardwareAxes = profile["hardware"]["axes"]
        hardwareButtons = profile["hardware"]["buttons"]

        for hardwareAxis, data in hardwareAxes.items():
            Debug.Log(f"Loading {hardwareAxis}...")

            if(data["bindedTo"] == None):
                Debug.Log(">>> SKIPPED: not specified.")
            else:
                bindedTo = data["bindedTo"]
                getter = data["getter"]

                result = Controls.BindAxis("Gamepad", bindedTo, hardwareAxis, getter)
                if(result != Execution.Passed):
                    Debug.Warn(f"Failed to bind {hardwareAxis} to {bindedTo} as Kontrol")
                    Gamepad.hardwareControls["axes"][hardwareAxis]["binded"] = False,
                    Gamepad.hardwareControls["axes"][hardwareAxis]["bindedTo"] = None
                else:
                    Gamepad.hardwareControls["axes"][hardwareAxis]["binded"] = True,
                    Gamepad.hardwareControls["axes"][hardwareAxis]["bindedTo"] = bindedTo

        for hardwareButton, data in hardwareButtons.items():
            Debug.Log(f"Loading {hardwareButtons}...")

            if(data["bindedTo"] == None):
                Debug.Log(">>> SKIPPED: not specified.")
            else:
                bindedTo = data["bindedTo"]
                getter = data["getter"]

                result = Controls.BindButton("Gamepad", bindedTo, hardwareButton, getter)
                if(result != Execution.Passed):
                    Debug.Warn(f"Failed to bind {hardwareButton} to {bindedTo} as Kontrol")
                    Gamepad.hardwareControls["buttons"][hardwareButton]["binded"] = False,
                    Gamepad.hardwareControls["buttons"][hardwareButton]["bindedTo"] = None
                else:
                    Gamepad.hardwareControls["buttons"][hardwareButton]["binded"] = True,
                    Gamepad.hardwareControls["buttons"][hardwareButton]["bindedTo"] = bindedTo

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _AddNewProfile(nameOfProfile) -> Execution:
        """
            _AddNewProfile:
            ===============
            Adds a new profile to the JSON data.
            Does not save it tho.
        """
        Debug.Start("_AddNewProfile")
        Gamepad.profileData.jsonData["saved-profiles"][nameOfProfile] = profileExample
        Debug.Log(f"Default parameters set for {nameOfProfile}")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _DoesProfileExist(nameOfProfile) -> bool:
        """
            _DoesProfileExist:
            ===============
            tells you if a profile exist in that JSON file.
        """
        Debug.Start("_DoesProfileExist")

        profiles = Gamepad.profileData.jsonData["saved-profiles"]

        if nameOfProfile in profiles:
            Debug.Log(f"{nameOfProfile} is already in the JSON")
            Debug.End()
            return True
        else:
            Debug.Log(f"{nameOfProfile} is not in the JSON")
            Debug.End()
            return False
    # -----------------------------------
    def _PutBindsInProfile(profileToSaveBinds:str):
        """
            _PutBindsInProfile:
            ===================
            Summary:
            --------
            Function that puts the current hardwarecontrol
            binds into a specified profile.

            Does not check if it exists.
        """
        Debug.Start("_PutBindsInProfile")
        Debug.Log(f"Updating {profileToSaveBinds}'s bindings")
        for axis in Gamepad.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["axes"]:
            Gamepad.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["axes"][axis]["binded"] = Gamepad.hardwareControls["axes"][axis]["binded"]
            Gamepad.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["axes"][axis]["bindedTo"] = Gamepad.hardwareControls["axes"][axis]["bindedTo"]
        
        for button in Gamepad.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["buttons"]:
            Gamepad.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["buttons"][button]["binded"] = Gamepad.hardwareControls["buttons"][button]["binded"]
            Gamepad.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["buttons"][button]["bindedTo"] = Gamepad.hardwareControls["buttons"][button]["bindedTo"]
        Debug.End()
    # -----------------------------------
    def VerifyForExecution() -> Execution:
        """
            VerifyForExecution:
            ===================
            Summary:
            --------
            Function that returns Execution.Passed
            if the hardware and software allows
            ADXL343 to interface with Kontrol.
            Otherwise, Execution.Failed is returned.
        """
        Debug.Start("VerifyForExecution")

        if(not Information.initialized):
            Debug.Error("Information class is not initialized")
            Debug.End()
            return Execution.Failed

        # if(Information.platform != "Linux"):
            # Debug.Error("This addon only works on Linux.")
            # Debug.End()
            # return Execution.Incompatibility

        result = Gamepad._InitializeProfileJson()
        if(result != Execution.Passed):
            Debug.Error("JSON could not be created and loaded.")
            Debug.End()
            return Execution.Failed

        Debug.Log("Seems alright.")
        Debug.End()
        return Execution.Passed
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("driver.py")