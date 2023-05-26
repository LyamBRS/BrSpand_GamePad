#====================================================================#
# File Information
#====================================================================#
"""
    receiver.py
    =============
    ----------------------------------
"""

#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("BFIODriver.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import time
import threading
import serial

#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
# LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Variables
#====================================================================#

#====================================================================#
# Classes
#====================================================================#


class BFIODriver:
    """
        BFIODriver:
        =====
        Summary:
        --------
        Backend driver that reads at fasts intervals the BFIODriver
        of a raspberry pi.
    """
    thread = None
    stopEvent = threading.Event()
    isStarted: bool = False

    serialPort:str = None
    """
        serialPort:
        ===========
        summary:
        --------
        The name of the serial port you want to use.
        Defaults to NONE so be careful.
    """

    serialPortObject = None

    maxGroupsSlots = 10
    """
        Defines how many groups of
        arrived passengers you can store
        in your BFIO class. Defaults to 10.
        After which, no more groups are stored.
        They are ignored.
    """

    planesToWrite:list = []
    groupsOfArrivedPassengers:list = []

    _lock = threading.Lock()

    @staticmethod
    def _reading_thread(uartClass, UART):
        from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO, NewArrival, PassengerTypes, MandatoryPlaneIDs
        ################################################
        while True:

            if uartClass.stopEvent.is_set():
                break

            with uartClass._lock:
                pass0
        ################################################
        uartClass.isStarted = False

    @staticmethod
    def _writing_thread(uartClass):
        pass

    @staticmethod
    def StartDriver():
        """
            StartDriver:
            ============
            Summary:
            --------
            Starts a thread that reads
            all the informations of BFIODriver
            pins at intervals of 3 seconds

            Returns:
            --------
        """
        Debug.Start("BFIODriver -> StartDriver")

        if(Information.platform != "Linux"):
            Debug.Error(f"You cannot use this driver on your platform: {Information.platform}")
            Debug.End()
            return Execution.Incompatibility

        if BFIODriver.isStarted == False:
            if not BFIODriver.thread or not BFIODriver.thread.is_alive():
                BFIODriver.stopEvent.clear()
                # BFIODriver.stopEventWriting.clear()
                BFIODriver.serialPortObject = serial.Serial(BFIODriver.serialPort, baudrate=9600, timeout=0.01)
                BFIODriver.thread = threading.Thread(target=BFIODriver._reading_thread, args=(BFIODriver,))
                # BFIODriver.TXthread = threading.Thread(target=BFIODriver._writing_thread, args=(BFIODriver,))
                BFIODriver.thread.daemon = True
                # BFIODriver.TXthread.daemon = True
                BFIODriver.thread.start()
                # BFIODriver.TXthread.start()
                BFIODriver.isStarted = True
                Debug.End()
                return Execution.Passed
        else:
            Debug.Error("Threads are already started. You cannot start more than 2.")
            Debug.End()
            return Execution.Unecessary
        Debug.Log("BFIODriver is now started")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def StopDriver():
        """
            StopDriver:
            ============
            Summary:
            --------
            Stops the thread that reads
            BFIODriver pins values through
            terminal.
        """
        Debug.Start("BFIODriver -> StopDriver")
        BFIODriver.stopEvent.set()
        BFIODriver.stopEventWriting.set()

        if BFIODriver.thread and BFIODriver.thread.is_alive():
            BFIODriver.thread.join()

        if BFIODriver.TXthread and BFIODriver.TXthread.is_alive():
            BFIODriver.TXthread.join()
        
        Debug.Log("Stopping Serial Port Object.")
        try:
            BFIODriver.serialPortObject.close()
        except:
            Debug.Error("serialPortObject couldn't be closed. maybe its None typed and wasn't ever opened.")
        Debug.Log("Success.")

        BFIODriver.isStarted = False
        Debug.Log("thread is stopped.")
        Debug.Log("TXthread is stopped.")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def GetReceivedPlanes() -> list:
        """
            GetReceivedPlanes:
            ==================
            Summary:
            --------
            Updates the received plane list. 

            Returns:
            --------
            - [{},{},{} ...]
            - `Execution.Failed` = thread isn't started.
        """
        Debug.Start("GetList")
        if BFIODriver.isStarted:
            with BFIODriver._lock:
                Debug.Log("Returning values from the thread")
                Debug.End()
                return BFIODriver.groupsOfArrivedPassengers
        else:
            Debug.Log("thread WAS NOT STARTED. Execution.Failed is returned")
            Debug.End()
            return Execution.Failed
        
    def QueuePlaneOnTaxiway(planeToTakeOff) -> Execution:
        """
            QueuePlaneOnTaxiway:
            ====================
            Summary:
            --------
            Puts a plane to be sent on Serial.

            Returns:
            --------
            - [{},{},{} ...]
            - `Execution.Failed` = thread isn't started.
        """
        Debug.Start("QueuePlaneOnTaxiway")
        if BFIODriver.isStarted:
            with BFIODriver._lock:
                BFIODriver.planesToWrite.append(planeToTakeOff)
                Debug.End()
                return Execution.Passed
        else:
            Debug.Log("TXthread WAS NOT STARTED. Execution.Failed is returned")
            Debug.End()
            return Execution.Failed

    @staticmethod
    def GetOldestReceivedGroupOfPassengers() -> list:
        """
            GetOldestReceivedGroupOfPassengers:
            ===================================
            Summary:
            --------
            Method that returns the oldest received
            group of passengers. it also removes
            it from the list of saved groups of passengers

        """
        Debug.Start("GetOldestReceivedGroupOfPassengers")

        if(BFIODriver.isStarted):
            
            try:
                BFIODriver.GetReceivedPlanes()
                OldestGroupOfPassengers = BFIODriver.groupsOfArrivedPassengers.pop(0)
            except:
                Debug.Warn("No groups of passengers to return.")
                Debug.End()
                return None

            Debug.Log(f"Returning a group of passengers")
            Debug.End()
            return OldestGroupOfPassengers
        else:
            Debug.Log("BFIODriver thread WAS NOT STARTED.")
            Debug.End()
            return Execution.Failed
#====================================================================#
LoadingLog.End("driver.py")