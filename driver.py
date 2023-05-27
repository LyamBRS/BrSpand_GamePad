#====================================================================#
# File Information
#====================================================================#
"""
    GamePad.py
    ==========
    Summary:
    --------
    This file contains the high level classes and functions made to
    a GamePad BrSpand card.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO
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
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Utilities.addons import AddonFoundations, AddonInfoHandler, AddonEnum
from Libraries.BRS_Python_Libraries.BRS.PnP.controls import Controls
from Libraries.BRS_Python_Libraries.BRS.Hardware.UART.receiver import UART
from BrSpand.Drivers.GamePad.BFIO import BFIODriver
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
    "name" : "GamePad",
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
                                                  "getter" : BFIODriver.Get_LeftJoystickXPositive},
                                "left-x-negative" : { "binded" : False,
                                                 "bindedTo" : None,
                                                 "getter" : BFIODriver.Get_LeftJoystickXNegative},
                                "left-y-positive" : {  "binded" : False,
                                                  "bindedTo" : None,
                                                  "getter" : BFIODriver.Get_LeftJoystickYPositive},
                                "left-y-negative" : { "binded" : False,
                                                  "bindedTo" : None,
                                                  "getter" : BFIODriver.Get_LeftJoystickYNegative},
                                "right-x-positive" : { "binded" : False,
                                                  "bindedTo" : None,
                                                  "getter" : BFIODriver.Get_RightJoystickXPositive},
                                "right-x-negative" : { "binded" : False,
                                                  "bindedTo" : None,
                                                  "getter" : BFIODriver.Get_RightJoystickXNegative},
                                "right-y-positive" : { "binded" : False,
                                                  "bindedTo" : None,
                                                  "getter" : BFIODriver.Get_RightJoystickYPositive},
                                "right-y-negative" : { "binded" : False,
                                                  "bindedTo" : None,
                                                  "getter" : BFIODriver.Get_RightJoystickYNegative}
                        },
                        "buttons" : {
                                    "left-joystick-button" : {  "binded" : False,
                                                                "bindedTo" : None,
                                                                "getter" : BFIODriver.Get_LeftJoystickButton},
                                    "right-joystick-button" : {  "binded" : False,
                                                                "bindedTo" : None,
                                                                "getter" : BFIODriver.Get_RightJoystickButton},
                                    "switch1" : {  "binded" : False,
                                                    "bindedTo" : None,
                                                    "getter" : BFIODriver.Get_Switch1},
                                    "switch2" : { "binded" : False,
                                                    "bindedTo" : None,
                                                    "getter" : BFIODriver.Get_Switch2},
                                    "switch3" : { "binded" : False,
                                                    "bindedTo" : None,
                                                    "getter" : BFIODriver.Get_Switch3},
                                    "switch4" : { "binded" : False,
                                                    "bindedTo" : None,
                                                    "getter" : BFIODriver.Get_Switch4},
                                    "switch5" : { "binded" : False,
                                                    "bindedTo" : None,
                                                    "getter" : BFIODriver.Get_Switch5}
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
class GamePad(AddonFoundations):
    #region   --------------------------- DOCSTRING
    """
        GamePad:
        ==============
        Summary:
        --------
        This class handles the backend of trying
        to interface an GamePad addon card
        with the Raspberry Pi.
    """
    #endregion
    #region   --------------------------- MEMBERS
    profileData:JSONdata = None

    hardwareControls:dict = {
        "axes" : {
                    "left-x-positive" : {  "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : BFIODriver.Get_LeftJoystickXPositive},
                    "left-x-negative" : { "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : BFIODriver.Get_LeftJoystickXNegative},
                    "left-y-positive" : {  "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : BFIODriver.Get_LeftJoystickYPositive},
                    "left-y-negative" : { "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : BFIODriver.Get_LeftJoystickYNegative},
                    "right-x-positive" : { "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : BFIODriver.Get_RightJoystickXPositive},
                    "right-x-negative" : { "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : BFIODriver.Get_RightJoystickXNegative},
                    "right-y-positive" : { "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : BFIODriver.Get_RightJoystickYPositive},
                    "right-y-negative" : { "binded" : False,
                                        "bindedTo" : None,
                                        "getter" : BFIODriver.Get_RightJoystickYNegative}
                 },
                    "buttons" : {
                                "left-joystick-button" : {  "binded" : False,
                                                            "bindedTo" : None,
                                                            "getter" : BFIODriver.Get_LeftJoystickButton},
                                "right-joystick-button" : {  "binded" : False,
                                                            "bindedTo" : None,
                                                            "getter" : BFIODriver.Get_RightJoystickButton},
                                "switch1" : {  "binded" : False,
                                                "bindedTo" : None,
                                                "getter" : BFIODriver.Get_Switch1},
                                "switch2" : { "binded" : False,
                                                "bindedTo" : None,
                                                "getter" : BFIODriver.Get_Switch2},
                                "switch3" : { "binded" : False,
                                                "bindedTo" : None,
                                                "getter" : BFIODriver.Get_Switch3},
                                "switch4" : { "binded" : False,
                                                "bindedTo" : None,
                                                "getter" : BFIODriver.Get_Switch4},
                                "switch5" : { "binded" : False,
                                                "bindedTo" : None,
                                                "getter" : BFIODriver.Get_Switch5}
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
            Launches the GamePad addon.
            returns Execution to indicate how
            the launch went.

            Returns:
            --------
            - `Execution.Passed` = Addon was launched.
            - `Execution.Failed` = Error occured
            - `Execution.Incompatibility` = Failed to verify for compatibility.
        """
        Debug.Start("GamePad -> Launch")

        Debug.Log("Creating AddonInfoHandler")
        GamePad.addonInformation = AddonInfoHandler(
            name="GamePad",
            description="BrSpand GamePad card giving extra hardware controls to your devices",
            version="0.0.1",
            type="brspand",
            repository="https://github.com/LyamBRS/BrSpand_GamePad.git",
            hasHardwareButtons= True,
            hasHardwareAxes= True,
            readsSoftwareButtons= False,
            readsSoftwareAxes= False,
            MDIcon= "gamepad-variant",
            LaunchFunction = GamePad.Launch,
            StopFunction = GamePad.Stop,
            UninstallFunction = GamePad.Uninstall,
            UpdateFunction = GamePad.Update,
            GetStateFunction = GamePad.GetState,
            ClearProfileFunction= GamePad.ClearProfile,
            SaveProfile = GamePad.SaveProfile,
            ChangeProfile= GamePad.ChangeProfile,
            LoadProfile= GamePad.LoadProfile,
            UnloadProfile= GamePad.UnloadProfile,
            PeriodicCallback= GamePad.PeriodicCallback,
            GetAllHardwareControls= GamePad.GetAllHardwareControls,
            GetAllSoftwareActions= GamePad.GetAllSoftwareActions,
            ChangeButtonActionBinding= GamePad.ChangeButtonActionBinding,
            ChangeAxisActionBinding= GamePad.ChangeAxisActionBinding,
            UnbindButtonBinding= GamePad.UnbindButtonBinding,
            UnbindAxisBinding= GamePad.UnbindAxisBinding,
            ChangeButtonBinding= GamePad.ChangeButtonBinding,
            ChangeAxisBinding= GamePad.ChangeAxisBinding
        )

        Debug.Log("Checking if we need to load in a current profile.")
        profileName = ProfileHandler.currentName

        from kivymd.uix.dialog import MDDialog
        # dialog = MDDialog(
            # title="Debug",
            # text=f"loading: {profileName}"
                # )
        # dialog.open()

        if(profileName != None):
            GamePad.loadedProfileName = profileName
            GamePad.LoadProfile(profileName)

        result = GamePad.VerifyForExecution()
        if(result != Execution.Passed):
            Debug.Error("The BrSpand card cannot run on your device.")
            Debug.Log("Adding addon to application...")
            GamePad.addonInformation.DockAddonToApplication(False)
            Debug.End()
            return result

        result = UART.StartDriver()
        if(result == Execution.Failed):
            Debug.Error("Failed to start backend driver UART")
            GamePad.addonInformation.DockAddonToApplication(False)
            Debug.End()
            return Execution.Failed

        result = BFIODriver.StartDriver()
        if(result != Execution.Passed):
            Debug.Error("Failed to start backend driver UART")
            GamePad.addonInformation.DockAddonToApplication(False)
            dialog = MDDialog(
                title=_("GamePad Driver Error"),
                text=_("GamePad failed to start its BFIO Drivers. Kontrol will not be able to gather inputs from the connected GamePad")
                )
            dialog.open()
            Debug.End()
            return Execution.Failed

        Debug.Log("Addon started successfully.")
        Debug.Log("Adding addon to application...")
        GamePad.addonInformation.DockAddonToApplication(True)
        GamePad.state = True
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
        Debug.Start("GamePad -> Stop")

        if(GamePad.state == True):
            Debug.Log("Stopping Reader")
            result = BFIODriver.StopDriver()
            if(result != Execution.Passed):
                Debug.Error("Failed to stop BFIODrivers")
                Debug.End()
                return Execution.Failed
            Debug.Log("GamePad is now OFF")
            GamePad.profileData.SaveFile()
            GamePad.UnloadProfile(GamePad.loadedProfileName)
            GamePad.state = False
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. GamePad is not running.")
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
        Debug.Start("GamePad -> GetAllHardwareControls")
        if(GamePad.state == True):
            Debug.Log("Returning proper values")
            Debug.End()
            return GamePad.hardwareControls
        else:
            Debug.Log("Unecessary. GamePad is not running.")
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
        Debug.Start("GamePad -> LoadProfile")

        if(GamePad.state == True):
            Debug.Log(f"Trying to load {profileToLoad} from Profiles.json")

            try:
                profile = GamePad.profileData.jsonData["saved-profiles"][profileToLoad]
                Debug.Log(f"{profileToLoad} was found in the JSON.")
            except:
                Debug.Log(f"{profileToLoad} doesn't exist in the JSON... Creating it.")
                GamePad._AddNewProfile(profileToLoad)

                Debug.Log("Saving JSON file...")
                saved = GamePad.profileData.SaveFile()
                if(not saved):
                    Debug.Error("Failed to save JSON file...")
                    Debug.End()
                    return Execution.Failed
                Debug.Log("Success")
                profile = GamePad.profileData.jsonData["saved-profiles"][profileToLoad]

            Debug.Log(f"Loading {profileToLoad}'s data.")
            GamePad.loadedProfileName = profileToLoad
            result = GamePad._LoadProfileBindsInApplication()
            if(result != Execution.Passed):
                Debug.Error(f"Failed to keybinds of {GamePad.loadedProfileName} into the Controls class.")
                Debug.End()
                return result
            
            Debug.Log("Profile loaded in successfully.")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Warn("GamePad is not running.")
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
        Debug.Start("GamePad -> UnloadProfile")

        if(GamePad.state == True):
            Debug.Log(f"Unloading the current profile.")
            result = GamePad._UnbindEverything()
            if(result != Execution.Passed):
                Debug.Error(f"_UnbindEverything returned error code: {result}")
                Debug.End()
                return result

            Debug.Log("Clearing saved profile's name.")
            GamePad.loadedProfileName = None
        else:
            Debug.Warn("GamePad is not running.")
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
        Debug.Start("GamePad -> SaveProfile")

        if(GamePad.state == True):
            if(GamePad.loadedProfileName == None and profileToSave == None):
                Debug.Error("No profiles were loaded in the class.")
                Debug.End()
                return Execution.Failed

            if(profileToSave == None):
                Debug.Log("Saving loaded profile.")
                profileToSave = GamePad.loadedProfileName

            existing = GamePad._DoesProfileExist(profileToSave)
            if(not existing):
                Debug.Log(f"{profileToSave} does not exist. Creating it.")
                GamePad._AddNewProfile(profileToSave)
                GamePad._PutBindsInProfile(profileToSave)
            else:
                Debug.Log(f"Putting live binds in {profileToSave}")
                GamePad._PutBindsInProfile(profileToSave)

            saved = GamePad.profileData.SaveFile()
            if(not saved):
                Debug.Error("Saving failed.")
                Debug.End()
                return Execution.Failed

            Debug.Log(">>> SUCCESS")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. GamePad is not running.")
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
        Debug.Start("GamePad -> ClearProfile")
        if(GamePad.profileData.jsonData == None):
            Debug.Error("No json is loaded. GamePad cannot delete anything.")
            Debug.End()
            return Execution.ByPassed

        existing = GamePad._DoesProfileExist(profileToClear)
        if(not existing):
            Debug.Warn(f"GamePad has no cached data for {profileToClear}")
            Debug.End()
            return Execution.Unecessary

        savedProfiles:dict = GamePad.profileData.jsonData["saved-profiles"]
        savedProfiles.pop(profileToClear)
        Debug.Log(f"{profileToClear} no longer exists in GamePad's cached profiles.")
        GamePad.profileData.jsonData["saved-profiles"] = savedProfiles
        GamePad.profileData.SaveFile()
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
        Debug.Start("GamePad -> ChangeAxisBinding")

        if(GamePad.state == True):
            result = GamePad.UnbindAxisBinding(nameOfSoftwareAxis)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Failed to unbind software axis: {nameOfSoftwareAxis}")
                Debug.End()
                return Execution.Failed

            result = GamePad._UnbindHardwareAxis(nameOfHardwareAxis)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Failed to unbind hardware axis: {nameOfHardwareAxis}")
                Debug.End()
                return Execution.Failed

            Debug.Log(f"GamePad no longer holds bindings for the software axis: {nameOfSoftwareAxis} as well as the hardware axis: {nameOfHardwareAxis}")

            result = GamePad._BindAxis(nameOfSoftwareAxis, nameOfHardwareAxis)
            if(result != Execution.Passed):
                Debug.Error(f"Something went wrong when trying to bind {nameOfHardwareAxis} to {nameOfSoftwareAxis}")
                Debug.End()
                return result

            Debug.Log(f"Saving {GamePad.loadedProfileName}'s new binds.")
            GamePad._PutBindsInProfile(GamePad.loadedProfileName)

            saved = GamePad.profileData.SaveFile()
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
        Debug.Start("GamePad -> ChangeButtonBinding")

        if(GamePad.state == True):
            result = GamePad.UnbindButtonBinding(nameOfSoftwareButton)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Failed to unbind software button: {nameOfSoftwareButton}")
                Debug.End()
                return Execution.Failed

            result = GamePad._UnbindHardwareButton(nameOfHardwareButton)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Failed to unbind hardware button: {nameOfHardwareButton}")
                Debug.End()
                return Execution.Failed

            Debug.Log(f"GamePad no longer holds bindings for the software button: {nameOfSoftwareButton} as well as the hardware button: {nameOfHardwareButton}")

            result = GamePad._BindButton(nameOfSoftwareButton, nameOfHardwareButton)
            if(result != Execution.Passed):
                Debug.Error(f"Something went wrong when trying to bind {nameOfHardwareButton} to {nameOfSoftwareButton}")
                Debug.End()
                return result

            Debug.Log(f"Saving {GamePad.loadedProfileName}'s new binds.")
            GamePad._PutBindsInProfile(GamePad.loadedProfileName)

            saved = GamePad.profileData.SaveFile()
            if(not saved):
                Debug.Log("Failed to save Profile.json")
                Debug.End()
                return Execution.Crashed

            Debug.Log(">>> Success")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. GamePad is not running.")
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
        Debug.Start("GamePad -> UnbindAxisBinding")

        if(GamePad.state):
            whateverAxisHadItBinded = GamePad._WhoHasThatAxisBinded(nameOfSoftwareAxis)
            if(whateverAxisHadItBinded == Execution.Unecessary):
                Debug.Log(f"{nameOfSoftwareAxis} isn't currently binded by the GamePad.")
                Debug.End()
                return Execution.Unecessary

            result = GamePad._UnbindSoftwareAxis(nameOfSoftwareAxis, whateverAxisHadItBinded)
            if(result != Execution.Passed):
                Debug.Log(f"Error occured when unbinding {nameOfSoftwareAxis}. Return code: {result}")

            Debug.Log("Updating profile with new informations.")
            GamePad._PutBindsInProfile(GamePad.loadedProfileName)
            GamePad.profileData.SaveFile()
            Debug.Log(">>> Success")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Warn("GamePad is not running.")
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
        Debug.Start("GamePad -> UnbindButtonBinding")

        if(GamePad.state):
            whateverButtonHadItBinded = GamePad._WhoHasThatButtonBinded(nameOfSoftwareButton)
            if(whateverButtonHadItBinded == Execution.Unecessary):
                Debug.Log(f"{nameOfSoftwareButton} isn't currently binded by the GamePad.")
                Debug.End()
                return Execution.Unecessary

            result = GamePad._UnbindSoftwareButton(nameOfSoftwareButton, whateverButtonHadItBinded)
            if(result != Execution.Passed):
                Debug.Log(f"Error occured when unbinding {nameOfSoftwareButton}. Return code: {result}")

            Debug.Log("Updating profile with new informations.")
            GamePad._PutBindsInProfile(GamePad.loadedProfileName)
            GamePad.profileData.SaveFile()
            Debug.Log(">>> Success")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Warn("GamePad is not running.")
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

        for hardwareAxis, data in GamePad.hardwareControls["axes"].items():
            Debug.Log(f"Unbinding {hardwareAxis} from the GamePad.")
            result = GamePad._UnbindHardwareAxis(hardwareAxis)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Fatal error occured when trying to unbind {hardwareAxis}. Return code: {result}")
                Debug.End()
                return Execution.Failed
            
        for hardwareButton, data in GamePad.hardwareControls["buttons"].items():
            Debug.Log(f"Unbinding {hardwareButton} from the GamePad.")
            result = GamePad._UnbindHardwareButton(hardwareButton)
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
        whatItsBindedTo = GamePad.hardwareControls["axes"][nameOfHardwareAxis]["bindedTo"]
        if(whatItsBindedTo == None):
            Debug.Log(f"{nameOfHardwareAxis} isn't binded to any software axis.")
            Debug.End()
            return Execution.Passed

        Debug.Log(f"Unbinding {nameOfHardwareAxis} from {whatItsBindedTo}")
        result = Controls.UnbindAxis("GamePad", nameOfSoftwareAxis=whatItsBindedTo)
        if(result != Execution.Passed):
            Debug.Log(f"Failed to unbind {nameOfHardwareAxis} from {whatItsBindedTo}")
            Debug.End()
            return result

        GamePad.hardwareControls["axes"][nameOfHardwareAxis]["binded"] = False
        GamePad.hardwareControls["axes"][nameOfHardwareAxis]["bindedTo"] = None
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
        whatItsBindedTo = GamePad.hardwareControls["buttons"][nameOfHardwareButton]["bindedTo"]
        if(whatItsBindedTo == None):
            Debug.Log(f"{nameOfHardwareButton} isn't binded to any software buttons.")
            Debug.End()
            return Execution.Passed

        Debug.Log(f"Unbinding {nameOfHardwareButton} from {whatItsBindedTo}")
        result = Controls.UnbindButton("GamePad", nameOfSoftwareButton=whatItsBindedTo)
        if(result != Execution.Passed):
            Debug.Log(f"Failed to unbind {nameOfHardwareButton} from {whatItsBindedTo}")
            Debug.End()
            return result

        GamePad.hardwareControls["buttons"][nameOfHardwareButton]["binded"] = False
        GamePad.hardwareControls["buttons"][nameOfHardwareButton]["bindedTo"] = None
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
        result = Controls.UnbindAxis("GamePad", nameOfSoftwareAxis=nameOfSoftwareAxis)
        if(result != Execution.Passed):
            Debug.Log(f"Failed to unbind {nameOfHardwareAxis} from {nameOfSoftwareAxis}")
            Debug.End()
            return result

        GamePad.hardwareControls["axes"][nameOfHardwareAxis]["binded"] = False
        GamePad.hardwareControls["axes"][nameOfHardwareAxis]["bindedTo"] = None
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
        result = Controls.UnbindButton("GamePad", nameOfSoftwareAxis=nameOfHardwareButton)
        if(result != Execution.Passed):
            Debug.Log(f"Failed to unbind {nameOfHardwareButton} from {nameOfHardwareButton}")
            Debug.End()
            return result

        GamePad.hardwareControls["buttons"][nameOfHardwareButton]["binded"] = False
        GamePad.hardwareControls["buttons"][nameOfHardwareButton]["bindedTo"] = None
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
        result = Controls.BindAxis("GamePad", nameOfSoftwareAxis, nameOfHardwareAxis, GamePad.hardwareControls["axes"][nameOfHardwareAxis]["getter"])
        if(result != Execution.Passed):
            Debug.Log(f"Failed to bind {nameOfHardwareAxis} to {nameOfSoftwareAxis} with error code: {result}")
            Debug.End()
            return result

        GamePad.hardwareControls["axes"][nameOfHardwareAxis]["binded"] = True
        GamePad.hardwareControls["axes"][nameOfHardwareAxis]["bindedTo"] = nameOfSoftwareAxis
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
        Debug.Start("_BindButton")

        Debug.Log(f"Binding {nameOfHardwareButton} to {nameOfHardwareButton} in Controls class.")
        result = Controls.BindButton("GamePad", nameOfSoftwareButton, nameOfHardwareButton, GamePad.hardwareControls["buttons"][nameOfHardwareButton]["getter"])
        if(result != Execution.Passed):
            Debug.Log(f"Failed to bind {nameOfHardwareButton} to {nameOfSoftwareButton} with error code: {result}")
            Debug.End()
            return result

        GamePad.hardwareControls["buttons"][nameOfHardwareButton]["binded"] = True
        GamePad.hardwareControls["buttons"][nameOfHardwareButton]["bindedTo"] = nameOfHardwareButton
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

        for hardwareAxis, axisData in GamePad.hardwareControls["axes"].items():
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

        for hardwareButton, buttonData in GamePad.hardwareControls["buttons"].items():
            if(buttonData["bindedTo"] == nameOfSoftwareButton):
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
        path = AppendPath(path, "/BrSpand/Drivers/GamePad/")

        GamePad.profileData = JSONdata("Profiles", path)
        if(GamePad.profileData.jsonData == None):
            Debug.Warn("No profile json file found for GamePad")
            GamePad.profileData.CreateFile(_EmptyJsonStructure)
            GamePad.profileData = JSONdata("Profiles", path)
            if(GamePad.profileData.jsonData == None):
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

        if(GamePad.loadedProfileName == None):
            Debug.Error("saved profile name is None. Something fucked up.")
            Debug.End()
            return Execution.Failed

        profile = GamePad.profileData.jsonData["saved-profiles"][GamePad.loadedProfileName]
        hardwareAxes = profile["hardware"]["axes"]
        hardwareButtons = profile["hardware"]["buttons"]

        for hardwareAxis, data in hardwareAxes.items():
            Debug.Log(f"Loading {hardwareAxis}...")

            if(data["bindedTo"] == None):
                Debug.Log(">>> SKIPPED: not specified.")
            else:
                bindedTo = data["bindedTo"]
                getter = data["getter"]

                result = Controls.BindAxis("GamePad", bindedTo, hardwareAxis, getter)
                if(result != Execution.Passed):
                    Debug.Warn(f"Failed to bind {hardwareAxis} to {bindedTo} as Kontrol")
                    GamePad.hardwareControls["axes"][hardwareAxis]["binded"] = False,
                    GamePad.hardwareControls["axes"][hardwareAxis]["bindedTo"] = None
                else:
                    GamePad.hardwareControls["axes"][hardwareAxis]["binded"] = True,
                    GamePad.hardwareControls["axes"][hardwareAxis]["bindedTo"] = bindedTo

        for hardwareButton, data in hardwareButtons.items():
            Debug.Log(f"Loading {hardwareButtons}...")

            if(data["bindedTo"] == None):
                Debug.Log(">>> SKIPPED: not specified.")
            else:
                bindedTo = data["bindedTo"]
                getter = data["getter"]

                result = Controls.BindButton("GamePad", bindedTo, hardwareButton, getter)
                if(result != Execution.Passed):
                    Debug.Warn(f"Failed to bind {hardwareButton} to {bindedTo} as Kontrol")
                    GamePad.hardwareControls["buttons"][hardwareButton]["binded"] = False,
                    GamePad.hardwareControls["buttons"][hardwareButton]["bindedTo"] = None
                else:
                    GamePad.hardwareControls["buttons"][hardwareButton]["binded"] = True,
                    GamePad.hardwareControls["buttons"][hardwareButton]["bindedTo"] = bindedTo

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
        GamePad.profileData.jsonData["saved-profiles"][nameOfProfile] = profileExample
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

        profiles = GamePad.profileData.jsonData["saved-profiles"]

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
        for axis in GamePad.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["axes"]:
            GamePad.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["axes"][axis]["binded"] = GamePad.hardwareControls["axes"][axis]["binded"]
            GamePad.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["axes"][axis]["bindedTo"] = GamePad.hardwareControls["axes"][axis]["bindedTo"]
        
        for button in GamePad.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["buttons"]:
            GamePad.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["buttons"][button]["binded"] = GamePad.hardwareControls["buttons"][button]["binded"]
            GamePad.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["buttons"][button]["bindedTo"] = GamePad.hardwareControls["buttons"][button]["bindedTo"]
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

        result = GamePad._InitializeProfileJson()
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