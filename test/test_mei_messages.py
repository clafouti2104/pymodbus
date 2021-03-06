#!/usr/bin/env python
'''
MEI Message Test Fixture
--------------------------------

This fixture tests the functionality of all the 
mei based request/response messages:
'''
import unittest
from pymodbus.mei_message import *
from pymodbus.constants import DeviceInformation, MoreData
from pymodbus.pdu import ModbusExceptions
from pymodbus.device import ModbusControlBlock

#---------------------------------------------------------------------------#
# Fixture
#---------------------------------------------------------------------------#
class ModbusMeiMessageTest(unittest.TestCase):
    '''
    This is the unittest for the pymodbus.mei_message module
    '''

    #-----------------------------------------------------------------------#
    # Read Device Information
    #-----------------------------------------------------------------------#

    def testReadDeviceInformationRequestEncode(self):
        ''' Test basic bit message encoding/decoding '''
        params  = {'read_code':DeviceInformation.Basic, 'object_id':0x00 }
        handle  = ReadDeviceInformationRequest(**params)
        result  = handle.encode()
        self.assertEqual(result, '\x0e\x01\x00')
        self.assertEqual("ReadDeviceInformationRequest(1,0)", str(handle))

    def testReadDeviceInformationRequestDecode(self):
        ''' Test basic bit message encoding/decoding '''
        handle  = ReadDeviceInformationRequest()
        handle.decode('\x0e\x01\x00')
        self.assertEqual(handle.read_code, DeviceInformation.Basic)
        self.assertEqual(handle.object_id, 0x00)

    def testReadDeviceInformationRequest(self):
        ''' Test basic bit message encoding/decoding '''
        context = None
        control = ModbusControlBlock()
        control.Identity.VendorName  = "Company"
        control.Identity.ProductCode = "Product"
        control.Identity.MajorMinorevision = "v2.1.12"

        handle  = ReadDeviceInformationRequest()
        result  = handle.execute(context)
        self.assertTrue(isinstance(result, ReadDeviceInformationResponse))
        self.assertTrue(result.information[0x00], "Company")
        self.assertTrue(result.information[0x01], "Product")
        self.assertTrue(result.information[0x02], "v2.1.12")

    def testReadDeviceInformationRequestError(self):
        ''' Test basic bit message encoding/decoding '''
        handle  = ReadDeviceInformationRequest()
        handle.read_code = -1
        self.assertEqual(handle.execute(None).function_code, 0xab)
        handle.read_code = 0x05
        self.assertEqual(handle.execute(None).function_code, 0xab)
        handle.object_id = -1
        self.assertEqual(handle.execute(None).function_code, 0xab)
        handle.object_id = 0x100
        self.assertEqual(handle.execute(None).function_code, 0xab)

    def testReadDeviceInformationResponseEncode(self):
        ''' Test that the read fifo queue response can encode '''
        message  = '\x0e\x01\x83\x00\x00\x03'
        message += '\x00\x07Company\x01\x07Product\x02\x07v2.1.12' 
        dataset  = {
            0x00: 'Company',
            0x01: 'Product',
            0x02: 'v2.1.12',
        }
        handle  = ReadDeviceInformationResponse(
            read_code=DeviceInformation.Basic, information=dataset)
        result  = handle.encode()
        self.assertEqual(result, message)
        self.assertEqual("ReadDeviceInformationResponse(1)", str(handle))

    def testReadDeviceInformationResponseDecode(self):
        ''' Test that the read device information response can decode '''
        message  = '\x0e\x01\x01\x00\x00\x03'
        message += '\x00\x07Company\x01\x07Product\x02\x07v2.1.12' 
        handle  = ReadDeviceInformationResponse(read_code=0x00, information=[])
        handle.decode(message)
        self.assertEqual(handle.read_code, DeviceInformation.Basic)
        self.assertEqual(handle.conformity, 0x01)
        self.assertEqual(handle.information[0x00], 'Company')
        self.assertEqual(handle.information[0x01], 'Product')
        self.assertEqual(handle.information[0x02], 'v2.1.12')

    def testRtuFrameSize(self):
        ''' Test that the read device information response can decode '''
        message = '\x04\x2B\x0E\x01\x81\x00\x01\x01\x00\x06\x66\x6F\x6F\x62\x61\x72\xD7\x3B'
        result  = ReadDeviceInformationResponse.calculateRtuFrameSize(message)
        self.assertEqual(result, 18)


#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
