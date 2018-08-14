#此模块为数据解析模块
import numpy as np
try:
    from DoubleBufferQueue import DoubleBufferQueue_ParseData_eeg, DoubleBufferQueue_ParseData_ecg, DoubleBufferQueue_ParseData_gsr
except ImportError:
    from data_processing.DoubleBufferQueue import DoubleBufferQueue_ParseData_eeg, DoubleBufferQueue_ParseData_ecg, DoubleBufferQueue_ParseData_gsr
class DataParserEEG():
    def __init__(self):
        self.PARSER_CODE_ATTENTION = 4    #注意力
        self.PARSER_CODE_MEDITATION = 5   #冥想
        self.PARSER_CODE_POOR_SIGNAL = 2
        self.PARSER_CODE_CONFIGURATION = 4
        self.PARSER_CODE_RAW = 128        #0x80
        self.PARSER_CODE_DEBUG_ONE = 132
        self.PARSER_CODE_DEBUG_TWO = 133
        self.PARSER_CODE_EEG_POWER = 131  #0x83

        self.RAW_DATA_BYTE_LENGTH = 2
        self.EEG_DEBUG_ONE_BYTE_LENGTH = 5
        self.EEG_DEBUG_TWO_BYTE_LENGTH = 3
        self.PARSER_SYNC_BYTE = 170       #0xAA
        self.PARSER_EXCODE_BYTE = 85      #0x55
        self.MULTI_BYTE_CODE_THRESHOLD = 127
        self.PARSER_STATE_SYNC = 1
        self.PARSER_STATE_SYNC_CHECK = 2
        self.PARSER_STATE_PAYLOAD_LENGTH = 3
        self.PARSER_STATE_PAYLOAD = 4
        self.PARSER_STATE_CHKSUM = 5

        self.payloadLength = 0
        self.payloadBytesReceived = 0
        self.payloadSum = 0
        self.checksum = 0
        self.payload = list()            #存放一包中的有效数据

        self.parserStatus = self.PARSER_STATE_SYNC
        self.double_queue_parse_data_eeg = DoubleBufferQueue_ParseData_eeg() #创建解析后的数据双缓冲实例
        #self.ten_eeg_dict = {'delta':0, 'theta':0, 'lowalpha':0, 'highalpha':0,
        #                    'lowbeta':0, 'highbeta':0, 'lowgamma':0, 'midgamma':0,
        #                    'meditation':0, 'attention':0,}
        self._flag_get_ten_eeg = False
        self._flag_get_eeg_eight = False

    def parseByte(self, data):
        if self.parserStatus == self.PARSER_STATE_SYNC:
            if (data & 0xFF) == self.PARSER_SYNC_BYTE:
                self.parserStatus = self.PARSER_STATE_SYNC_CHECK
            else:
                return -1
        elif self.parserStatus == self.PARSER_STATE_SYNC_CHECK:
            if (data & 0xFF) == self.PARSER_SYNC_BYTE:
                self.parserStatus = self.PARSER_STATE_PAYLOAD_LENGTH
            else:
                self.parserStatus = self.PARSER_STATE_SYNC
                return -1
        elif self.parserStatus == self.PARSER_STATE_PAYLOAD_LENGTH:
            self.payloadLength = (data & 0x0FF)     #获取一包数据的长度
            self.payloadBytesReceived = 0
            self.payload.clear()
            self.payloadSum = 0
            self.parserStatus = self.PARSER_STATE_PAYLOAD
        elif self.parserStatus == self.PARSER_STATE_PAYLOAD:
            self.payload.insert(self.payloadBytesReceived ,data)      #存储一包的有效数据
            self.payloadBytesReceived = self.payloadBytesReceived + 1 #记录一包数据接收的个数
            self.payloadSum = self.payloadSum + (data & 0xFF)
            if self.payloadBytesReceived < self.payloadLength:
                return 0
            self.parserStatus = self.PARSER_STATE_CHKSUM
        elif self.parserStatus == self.PARSER_STATE_CHKSUM:
            self.checksum = (data & 0xFF)
            self.parserStatus = self.PARSER_STATE_SYNC
            if self.checksum == (self.payloadSum ^ 0xFFFFFFFF) & 0xFF:
                self.parsePacketPayload()
            else:
                return -1

    def parsePacketPayload(self):
        i = 0
        extendedCodeLevel = 0
        code = 0
        valueBytesLength = 0
        signal = 0 
        rawWaveData = 0
        ten_eeg_dict = dict()
        while i < self.payloadLength:
            extendedCodeLevel = extendedCodeLevel + 1
            while self.payload[i] == self.PARSER_EXCODE_BYTE:
                i = i + 1
            code = self.payload[i] & 0xFF
            i = i + 1
            if code > self.MULTI_BYTE_CODE_THRESHOLD:
                valueBytesLength = self.payload[i] & 0xFF
                i = i + 1
            else:
                valueBytesLength = 1
            if code == self.PARSER_CODE_RAW:      #脑波原始数据
                if valueBytesLength == self.RAW_DATA_BYTE_LENGTH:
                    highOrderByte = self.payload[i]
                    lowOrderByte = self.payload[(i+1)]
                    rawWaveData = (highOrderByte << 8) | lowOrderByte
                    if rawWaveData > 32768:
                        rawWaveData = rawWaveData - 65536
                    self.double_queue_parse_data_eeg.writer_raw_eeg(rawWaveData)   #这里存放原始脑波数据
                i = i + valueBytesLength
            else:
                if code == self.PARSER_CODE_POOR_SIGNAL:
                    signal = self.payload[i] & 0xFF
                    i = i + valueBytesLength
                elif code == self.PARSER_CODE_EEG_POWER:       #8种脑电波形
                    if signal == 0:
                        self._flag_get_ten_eeg = True
                        highOrderByte = self.payload[i]
                        midOrderByte = self.payload[i + 1]
                        lowOrderByte = self.payload[i + 2]
                        delta = (highOrderByte << 16) | (midOrderByte << 8) | lowOrderByte
                        ten_eeg_dict['delta'] = delta         #这里存放delta波
                        highOrderByte = self.payload[i + 3]
                        midOrderByte = self.payload[i + 4]
                        lowOrderByte = self.payload[i + 5]
                        theta = (highOrderByte << 16) | (midOrderByte << 8) | lowOrderByte
                        ten_eeg_dict['theta'] = theta        #这里存放theta波
                        highOrderByte = self.payload[i + 6]
                        midOrderByte = self.payload[i + 7]
                        lowOrderByte = self.payload[i + 8]
                        lowalpha = (highOrderByte << 16) | (midOrderByte << 8) | lowOrderByte
                        ten_eeg_dict['lowalpha'] = lowalpha  #这里存放lowalpha波
                        highOrderByte = self.payload[i + 9]
                        midOrderByte = self.payload[i + 10]
                        lowOrderByte = self.payload[i + 11]
                        highalpha = (highOrderByte << 16) | (midOrderByte << 8) | lowOrderByte
                        ten_eeg_dict['highalpha'] = highalpha #这里存放highalpha波
                        highOrderByte = self.payload[i + 12]
                        midOrderByte = self.payload[i + 13]
                        lowOrderByte = self.payload[i + 14]
                        lowbeta = (highOrderByte << 16) | (midOrderByte << 8) | lowOrderByte
                        ten_eeg_dict['lowbeta'] = lowbeta    #这里存放lowbeta波
                        highOrderByte = self.payload[i + 15]
                        midOrderByte = self.payload[i + 16]
                        lowOrderByte = self.payload[i + 17]
                        highbeta = (highOrderByte << 16) | (midOrderByte << 8) | lowOrderByte
                        ten_eeg_dict['highbeta'] = highbeta  #这里存放highbeta波
                        highOrderByte = self.payload[i + 18]
                        midOrderByte = self.payload[i + 19]
                        lowOrderByte = self.payload[i + 20]
                        lowgamma = (highOrderByte << 16) | (midOrderByte << 8) | lowOrderByte
                        ten_eeg_dict['lowgamma'] = lowgamma  #这里存放lowgamma波
                        highOrderByte = self.payload[i + 21]
                        midOrderByte = self.payload[i + 22]
                        lowOrderByte = self.payload[i + 23]
                        midgamma = (highOrderByte << 16) | (midOrderByte << 8) | lowOrderByte
                        ten_eeg_dict['midgamma'] = midgamma  #这里存放midgamma波
                    i = i + valueBytesLength
                elif code == self.PARSER_CODE_ATTENTION:
                    if signal == 0:
                        self._flag_get_ten_eeg = True
                        attention = self.payload[i] & 0xFF
                        ten_eeg_dict['attention'] = attention #这里存放注意力
                    i = i + valueBytesLength
                elif code == self.PARSER_CODE_MEDITATION:
                    if signal == 0:
                        self._flag_get_ten_eeg = True
                        meditation = self.payload[i] & 0xFF
                        ten_eeg_dict['meditation'] = meditation #这里存放冥想度
                    i = i + valueBytesLength
        if self._flag_get_ten_eeg:
            self.double_queue_parse_data_eeg.writer_ten_eeg(ten_eeg_dict)  #将10种信号存放在缓存中          
            self._flag_get_ten_eeg = False
            self._flag_get_eeg_eight = True
        self.parserStatus = self.PARSER_STATE_SYNC
# Used for AD8235, if used change "DataParserECG_AD8235" to "DataParserECG"
class DataParserECG():
    def __init__(self):
        self.SPACE = 0x20
        self.rawWaveData = 0
        self.double_queue_parse_data_ecg = DoubleBufferQueue_ParseData_ecg() #创建解析后的数据双缓冲实例
    def parseByte(self, data):
        if (data >= 0x30 and data <= 0x39) or data == self.SPACE or data == 0x0D or data == 0x0A:
            if data >= 0x30 and data <= 0x39:
                self.rawWaveData = (self.rawWaveData * 10) + (data - 48)
            elif data == self.SPACE or data == 0x0D :
                self.double_queue_parse_data_ecg.writer_raw_ecg(self.rawWaveData)  #这里存放原始心电数据
                self.rawWaveData = 0

# Used for BMD101, if used change "DataParserECG_BMD101" to "DataParserECG"
class DataParserECG_BMD101():
    def __init__(self):
        self.PARSER_CODE_HEARTRATE = 3   #心率值
        self.PARSER_CODE_POOR_SIGNAL = 2
        self.PARSER_CODE_CONFIGURATION = 8
        self.PARSER_CODE_RAW = 128        #0x80
        self.PARSER_CODE_DEBUG_ONE = 132
        self.PARSER_CODE_DEBUG_TWO = 133

        self.RAW_DATA_BYTE_LENGTH = 2
        self.EEG_DEBUG_ONE_BYTE_LENGTH = 5
        self.EEG_DEBUG_TWO_BYTE_LENGTH = 3
        self.PARSER_SYNC_BYTE = 170       #0xAA
        self.PARSER_EXCODE_BYTE = 85      #0x55
        self.MULTI_BYTE_CODE_THRESHOLD = 127
        self.PARSER_STATE_SYNC = 1
        self.PARSER_STATE_SYNC_CHECK = 2
        self.PARSER_STATE_PAYLOAD_LENGTH = 3
        self.PARSER_STATE_PAYLOAD = 4
        self.PARSER_STATE_CHKSUM = 5

        self.payloadLength = 0
        self.payloadBytesReceived = 0
        self.payloadSum = 0
        self.checksum = 0
        self.payload = list()            #存放一包中的有效数据

        self.parserStatus = self.PARSER_STATE_SYNC
        self.double_queue_parse_data_ecg = DoubleBufferQueue_ParseData_ecg() #创建解析后的数据双缓冲实例

    def parseByte(self, data):
        if self.parserStatus == self.PARSER_STATE_SYNC:
            if (data & 0xFF) != self.PARSER_SYNC_BYTE:
                return -1
            self.parserStatus = self.PARSER_STATE_SYNC_CHECK
        elif self.parserStatus == self.PARSER_STATE_SYNC_CHECK:
            if (data & 0xFF) == self.PARSER_SYNC_BYTE:
                self.parserStatus = self.PARSER_STATE_PAYLOAD_LENGTH
            else:
                self.parserStatus = self.PARSER_STATE_SYNC
                return -1
        elif self.parserStatus == self.PARSER_STATE_PAYLOAD_LENGTH:
            self.payloadLength = (data & 0x0FF)     #获取一包数据的长度
            self.payloadBytesReceived = 0
            self.payload.clear()
            self.payloadSum = 0
            self.parserStatus = self.PARSER_STATE_PAYLOAD
        elif self.parserStatus == self.PARSER_STATE_PAYLOAD:
            self.payload.insert(self.payloadBytesReceived ,data)      #存储一包的有效数据
            self.payloadBytesReceived = self.payloadBytesReceived + 1 #记录一包数据接收的个数
            self.payloadSum = self.payloadSum + (data & 0xFF)
            if self.payloadBytesReceived < self.payloadLength:
                return -1
            self.parserStatus = self.PARSER_STATE_CHKSUM
        elif self.parserStatus == self.PARSER_STATE_CHKSUM:
            self.checksum = (data & 0xFF)
            self.parserStatus = self.PARSER_STATE_SYNC
            if self.checksum == (self.payloadSum ^ 0xFFFFFFFF) & 0xFF:
                self.parsePacketPayload()
            else:
                return -1

    def parsePacketPayload(self):
        i = 0
        extendedCodeLevel = 0
        code = 0
        valueBytesLength = 0
        signal = 0 
        rawWaveData = 0
        heartRateValue = 0
        while i < self.payloadLength:
            extendedCodeLevel = extendedCodeLevel + 1
            while self.payload[i] == self.PARSER_EXCODE_BYTE:
                i = i + 1
            code = self.payload[i] & 0xFF
            i = i + 1
            if code > self.MULTI_BYTE_CODE_THRESHOLD:
                valueBytesLength = self.payload[i] & 0xFF
                i = i + 1
            else:
                valueBytesLength = 1
            if code == self.PARSER_CODE_RAW:      #心率原始数据
                if valueBytesLength == self.RAW_DATA_BYTE_LENGTH:
                    highOrderByte = self.payload[i]
                    lowOrderByte = self.payload[(i+1)]
                    rawWaveData = (highOrderByte << 8) | lowOrderByte
                    if rawWaveData > 32768:
                        rawWaveData = rawWaveData - 65536
                    self.double_queue_parse_data_ecg.writer_raw_ecg(rawWaveData)  #这里存放原始心电数据
                i = i + valueBytesLength
            else:
                if code == self.PARSER_CODE_POOR_SIGNAL:
                    signal = self.payload[i] & 0xFF
                    i = i + valueBytesLength
                elif code == self.PARSER_CODE_HEARTRATE:
                    if signal == 0:
                        heartRateValue = self.payload[i] & 0xFF
                        self.double_queue_parse_data_ecg.writer_heartValue(heartRateValue) #这里存放心率值
                    i = i + valueBytesLength
                elif code == self.PARSER_CODE_CONFIGURATION:
                    i = i + valueBytesLength
                elif code == self.PARSER_CODE_DEBUG_ONE:
                    if valueBytesLength == self.EEG_DEBUG_ONE_BYTE_LENGTH:
                        i = i + valueBytesLength
                elif code == self.PARSER_CODE_DEBUG_TWO:
                    if valueBytesLength == self.EEG_DEBUG_TWO_BYTE_LENGTH:
                        i = i + valueBytesLength
        self.parserStatus = self.PARSER_STATE_SYNC

class DataParserGSR():
    def __init__(self):
        self.SPACE = 0x20
        self.rawWaveData = 0
        self.count = 0 #存储多个个数字
        self.dot_flag = False
        self.dot_num_behind = 1
        self.array = list()
        self.double_queue_parse_data_gsr = DoubleBufferQueue_ParseData_gsr() #创建解析后的数据双缓冲实例
    def parseByte(self, data):
        if (data >= 0x30 and data <= 0x39) or data == self.SPACE or data == 0x0D or data == 0x0A or data == 0x2E:
            if data >= 0x30 and data <= 0x39:
                if not self.dot_flag:
                    self.rawWaveData = (self.rawWaveData * 10) + (data - 48)
                elif self.dot_flag:
                    self.rawWaveData = self.rawWaveData + ((data - 48) / np.power(10, self.dot_num_behind))
                    self.dot_num_behind += 1
            elif data == self.SPACE :
                self.dot_flag = False
                self.dot_num_behind = 1
                self.count += 1
                self.array.append(self.rawWaveData)
                self.rawWaveData = 0
            elif data == 0x2E:#小数点
                self.dot_flag = True
            elif data == 0x0D:
                self.count += 1
                self.array.append(self.rawWaveData)
                if self.count == 28:
                    for element in self.array[:10]:
                        self.double_queue_parse_data_gsr.writer_raw_gsr(element)
                self.array.clear()
                self.count = 0
                self.rawWaveData = 0
                self.dot_flag = False
                self.dot_num_behind = 1
