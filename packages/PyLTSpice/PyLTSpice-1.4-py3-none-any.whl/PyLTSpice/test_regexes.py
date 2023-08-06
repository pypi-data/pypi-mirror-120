import os
import re

import LTSpiceBatch
from SpiceEditor import REPLACE_REGXES, get_line_command, UNIQUE_SIMULATION_DOT_INSTRUCTIONS, SPICE_DOT_INSTRUCTIONS

# Compile all regex expressions
regexes = {}

for key, value in REPLACE_REGXES.items():
    regexes[key] = re.compile(value)

# walk all the local files in c:\

for root, dirs, files in os.walk("c:\\SVN"):
    #print(root)
    for f in files:
        if f.endswith(".asc"):
            filenamep = os.path.join(root, f)

            # Failing Netlists
            if filenamep in (
r"c:\SVN\Electronic_Libraries\Altium\trunk\Scripts\ADLT\Joint_Electronics_-_MCU_Control.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\branches\old_top\SIMULATION\TopSheet.asc"
r" c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\tags\002916_REV_08 (Variosystem rework)\LTSpice\WC_Shunt_Regulator_Ref_10V.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\tags\002916_REV_08 (Variosystem rework)\LTSpice\WC_Shunt_Regulator_TLV1701_W.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\tags\002916_REV_08 (Variosystem rework)\SIMULATION\Controller_Board_Connectors.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\tags\002916_REV_08 (Variosystem rework)\SIMULATION\EPOS_Interface.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\tags\002916_REV_08 (Variosystem rework)\SIMULATION\HMI.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\tags\002916_REV_08 (Variosystem rework)\SIMULATION\Peripherals.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\tags\002916_REV_08 (Variosystem rework)\SIMULATION\Power_Bus.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\trunk\LTSpice\WC_Shunt_Regulator_Ref_10V.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\trunk\LTSpice\WC_Shunt_Regulator_TLV1701_W.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\trunk\SIMULATION\Controller_Board_Connectors.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\trunk\SIMULATION\EPOS_Interface.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\trunk\SIMULATION\HMI.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\trunk\SIMULATION\Peripherals.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\trunk\SIMULATION\Power_Bus.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\branches\old_top\SIMULATION\CAN_Relays.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\branches\old_top\SIMULATION\Testbench CAN Relays.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\branches\old_top\SIMULATION\testbench_cmchoke.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\branches\old_top\SIMULATION\TestOPA333.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\branches\old_top\SIMULATION\Full_Emergency_Heartbeat\003234_Power_Switch.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev02 (Variosystem)\SIMULATION\CAN_Relays.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev02 (Variosystem)\SIMULATION\TestOPA333.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev07 (Protoelectronique)\SIMULATION\CAN_Relays.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev07 (Protoelectronique)\SIMULATION\Testbench CAN Relays.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev07 (Protoelectronique)\SIMULATION\testbench_cmchoke.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev07 (Protoelectronique)\SIMULATION\TestOPA333.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\branches\old_top\SIMULATION\TopSheet.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev07 (Protoelectronique)\SIMULATION\TopSheet.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev08 (Variosystems)\SIMULATION\SPI_CAN_Controller.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev08 (Variosystems)\SIMULATION\TopSheet.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev09 (Variosystems)\SIMULATION\SPI_CAN_Controller.asc",
r"c:\SVN\L6_Electronics\002916_L6_Instrument_Arm_Interface\tags\002916_REV_08 (Variosystem rework)\LTSpice\WC_Shunt_Regulator_Ref_10V.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev07 (Protoelectronique)\SIMULATION\Full_Emergency_Heartbeat\003234_Power_Switch.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev08 (Variosystems)\SIMULATION\CAN_Relays.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev08 (Variosystems)\SIMULATION\Testbench CAN Relays.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev08 (Variosystems)\SIMULATION\testbench_cmchoke.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev08 (Variosystems)\SIMULATION\TestOPA333.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev08 (Variosystems)\SIMULATION\Full_Emergency_Heartbeat\003234_Power_Switch.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev09 (Variosystems)\SIMULATION\CAN_Relays.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev09 (Variosystems)\SIMULATION\TopSheet.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\trunk\SIMULATION\SPI_CAN_Controller.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev09 (Variosystems)\SIMULATION\Testbench CAN Relays.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev09 (Variosystems)\SIMULATION\testbench_cmchoke.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev09 (Variosystems)\SIMULATION\TestOPA333.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\tags\002933 Rev09 (Variosystems)\SIMULATION\Full_Emergency_Heartbeat\003234_Power_Switch.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\trunk\SIMULATION\CAN_Relays.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\trunk\SIMULATION\TopSheet.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\trunk\SIMULATION\Testbench CAN Relays.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\trunk\SIMULATION\testbench_cmchoke.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\trunk\SIMULATION\TestOPA333.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\trunk\SIMULATION\Full_Emergency_Heartbeat\003234_Power_Switch.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\trunk\SIMULATION\NEW\CAN.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\trunk\SIMULATION\NEW\PowerDistributionTPS.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\trunk\SIMULATION\NEW\PowerSupply.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\trunk\SIMULATION\NEW\StaticDisplay.asc",
r"c:\SVN\L6_Electronics\002933_L6_Surgeon_Console_Main_Board_Controller\trunk\SIMULATION\NEW\TopSheet.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\branches\Rework_on V04\SIMULATION\002942 L6 Master_Arm_Controller_Piccolo_BrakeControl.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\branches\Rework_on V04\SIMULATION\Delfino_IF.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\branches\Rework_on V04\SIMULATION\DMN3115UDM_testbench.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\branches\Rework_on V04\SIMULATION\Fan_Control_transistor.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\branches\Rework_on V04\SIMULATION\HighPowerswitch.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\branches\Rework_on V04\SIMULATION\HighPowerswitch_tb1.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\branches\Rework_on V04\SIMULATION\Main.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\branches\Rework_on V04\SIMULATION\Remote_Control_IF.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\branches\Rework_on V04\SIMULATION\resistor_testbench.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\branches\Rework_on V04\SIMULATION\Top.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\branches\Rework_on V04\SIMULATION\TVS24V_Testbench.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V04 (Variosystems) 20200613\SIMULATION\002942 L6 Master_Arm_Controller_Piccolo_BrakeControl.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V04 (Variosystems) 20200613\SIMULATION\Delfino_IF.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V04 (Variosystems) 20200613\SIMULATION\DMN3115UDM_testbench.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V04 (Variosystems) 20200613\SIMULATION\Fan_Control_transistor.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V04 (Variosystems) 20200613\SIMULATION\HighPowerswitch.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V04 (Variosystems) 20200613\SIMULATION\HighPowerswitch_tb1.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V04 (Variosystems) 20200613\SIMULATION\Main.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V04 (Variosystems) 20200613\SIMULATION\Remote_Control_IF.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V04 (Variosystems) 20200613\SIMULATION\resistor_testbench.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V04 (Variosystems) 20200613\SIMULATION\Top.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V04 (Variosystems) 20200613\SIMULATION\TVS24V_Testbench.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V06 (Variosystems Rework from 04) 2020.10.08\SIMULATION\002942 L6 Master_Arm_Controller_Piccolo_BrakeControl.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V06 (Variosystems Rework from 04) 2020.10.08\SIMULATION\Delfino_IF.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V06 (Variosystems Rework from 04) 2020.10.08\SIMULATION\DMN3115UDM_testbench.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V06 (Variosystems Rework from 04) 2020.10.08\SIMULATION\Fan_Control_transistor.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V06 (Variosystems Rework from 04) 2020.10.08\SIMULATION\HighPowerswitch.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V06 (Variosystems Rework from 04) 2020.10.08\SIMULATION\HighPowerswitch_tb1.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V06 (Variosystems Rework from 04) 2020.10.08\SIMULATION\Main.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V06 (Variosystems Rework from 04) 2020.10.08\SIMULATION\Remote_Control_IF.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V06 (Variosystems Rework from 04) 2020.10.08\SIMULATION\resistor_testbench.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V06 (Variosystems Rework from 04) 2020.10.08\SIMULATION\Top.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\002937 V06 (Variosystems Rework from 04) 2020.10.08\SIMULATION\TVS24V_Testbench.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\1v0_ordered\SIMULATION\002938 Patient Cart High-Powerswitch.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\V02 (Protoelectronique)\SIMULATION\Power_Distribution.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\V02 (Protoelectronique)\SIMULATION\002942 L6 Master_Arm_Controller_Piccolo_BrakeControl.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\V02 (Protoelectronique)\SIMULATION\CAN_Logger_IF.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\V02 (Protoelectronique)\SIMULATION\Delfino_IF.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\V02 (Protoelectronique)\SIMULATION\HighPowerswitch_tb1.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\V02 (Protoelectronique)\SIMULATION\HighPowerswitch_tb2.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\V02 (Protoelectronique)\SIMULATION\Isolated_Fan_Control.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\V02 (Protoelectronique)\SIMULATION\Main.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\V02 (Protoelectronique)\SIMULATION\Pos_Pillar_Control.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\V02 (Protoelectronique)\SIMULATION\Power_Filter.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\V02 (Protoelectronique)\SIMULATION\Remote_Control_IF.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\tags\V02 (Protoelectronique)\SIMULATION\Top.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\Project Outputs for 002938_L6_PatientCart_Mainboard\testbench_Brake_switch_only.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\Project Outputs for 002938_L6_PatientCart_Mainboard\Main.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\Project Outputs for 002938_L6_PatientCart_Mainboard\testbench_HighPowerSwitch.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\Project Outputs for 002938_L6_PatientCart_Mainboard\Top.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\SIMULATION\002942 L6 Master_Arm_Controller_Piccolo_BrakeControl.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\SIMULATION\Delfino_IF.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\SIMULATION\DMN3115UDM_testbench.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\SIMULATION\Fan_Control_transistor.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\SIMULATION\HighPowerswitch.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\SIMULATION\HighPowerswitch_tb1.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\SIMULATION\Main.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\SIMULATION\Remote_Control_IF.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\SIMULATION\resistor_testbench.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\SIMULATION\Top.asc",
r"c:\SVN\L6_Electronics\002937_L6_Patient_Cart_Main_Board_Controller\trunk\SIMULATION\TVS24V_Testbench.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\tags\002941 Rev04\SIMULATION\MasterMCU.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\tags\002941 Rev04\SIMULATION\MasterSSI.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\tags\002941 Rev04\SIMULATION\SafetyMCU.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\tags\002941 Rev04\SIMULATION\SafetySSI.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\tags\02 (protoelectronics)\SIMULATION\002942_L6_Master_Arm_Controller_Piccolo_MasterMCU.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\tags\02 (protoelectronics)\SIMULATION\002942_L6_Master_Arm_Controller_Piccolo_MasterSSI.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\tags\02 (protoelectronics)\SIMULATION\002942_L6_Master_Arm_Controller_Piccolo_SafetyMCU.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\tags\02 (protoelectronics)\SIMULATION\002942_L6_Master_Arm_Controller_Piccolo_SafetySSI.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\tags\02 (protoelectronics)\SIMULATION\002942_L6_Master_Arm_Controller_Piccolo_VCUT_Top_3Channels.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\trunk\SIMULATION\MasterMCU.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\trunk\SIMULATION\MasterSSI.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\trunk\SIMULATION\SafetyMCU.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\trunk\SIMULATION\SafetySSI.asc",
r"c:\SVN\L6_Electronics\002941 L6 Master_Arm_Controller_Piccolo\trunk\SIMULATION\test_OPA333\test_cmchoke.asc",
r"c:\SVN\L6_Electronics\003233_L6_BaseboardPresub\tags\003233 V02 (Variosystem first batch)\SIMULATION\003234_BaseboardPresub.asc",
r"c:\SVN\L6_Electronics\003233_L6_BaseboardPresub\tags\003233 V02 (Variosystem first batch)\SIMULATION\003234_Power_Switch.asc",
r"c:\SVN\L6_Electronics\003233_L6_BaseboardPresub\trunk\SIMULATION\003234_BaseboardPresub.asc",
r"c:\SVN\L6_Electronics\003233_L6_BaseboardPresub\trunk\SIMULATION\003234_Power_Switch.asc",
r"c:\SVN\L6_Electronics\004990_L6_Surgeon_Console_Patient_Cart_Interposer_Debug_Interface\trunk\SIMULATION\Interposer_Channel.asc",
r"c:\SVN\L6_Electronics\004990_L6_Surgeon_Console_Patient_Cart_Interposer_Debug_Interface\trunk\SIMULATION\Power_Supply.asc",
r"c:\SVN\L6_Electronics\006188_Floor_Lock_Controller\trunk\Project Outputs for 006188_Floor_Lock_Controller\Command_Input.asc",
r"c:\SVN\L6_Electronics\006188_Floor_Lock_Controller\trunk\Project Outputs for 006188_Floor_Lock_Controller\HBridge_and_Encoder.asc",
r"c:\SVN\L6_Electronics\006188_Floor_Lock_Controller\trunk\Project Outputs for 006188_Floor_Lock_Controller\Top.asc",
r"c:\SVN\L6_Electronics\006188_Floor_Lock_Controller\trunk\SIMULATION\Command_Input.asc",
r"c:\SVN\L6_Electronics\006188_Floor_Lock_Controller\trunk\SIMULATION\HBridge_Power.asc",
r"c:\SVN\L6_Electronics\006188_Floor_Lock_Controller\trunk\SIMULATION\LED_Driver.asc",
r"c:\SVN\L6_Electronics\006188_Floor_Lock_Controller\trunk\SIMULATION\Motor_Voltage.asc",
r"c:\SVN\L6_Electronics\006188_Floor_Lock_Controller\trunk\SIMULATION\Top.asc",
r"c:\SVN\L6_Firmware\System\trunk\00_SystemTests\Report_Vector\Can_Log_Failure.asc",
r"c:\SVN\L6_Firmware\System\trunk\00_SystemTests\Report_Vector\C_\Users\SwTestbenchPc_01.DIS\Desktop\Logging.asc",
            ):
                continue

            print(filenamep)
            netfile = filenamep[:-4]+'.net'
            if not os.path.exists(netfile):
                # creates the netlist
                LTS = LTSpiceBatch.SimCommander(filenamep)

                if not os.path.exists(netfile):
                    print(f'Unable to create netlist in file->r"{filenamep}",<-')
                    continue

            netlist = open(netfile)
            for line in netlist:
                prefix = get_line_command(line)
                if prefix in regexes:
                    m = regexes[prefix].match(line)
                    if m is None:
                        print("non matching line ", line)
                elif prefix in ('*', '.', '+'):
                    pass  # This is OK
                elif prefix in UNIQUE_SIMULATION_DOT_INSTRUCTIONS:
                    pass  # This is also OK
                elif prefix in SPICE_DOT_INSTRUCTIONS:
                    pass
                else:
                    print("Command not found in line ", line)







