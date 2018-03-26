#此模块为数据解析模块

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
            self.payloadSum = 0
            self.parserStatus = self.PARSER_STATE_PAYLOAD
        elif self.parserStatus == self.PARSER_STATE_PAYLOAD:
            self.payload.append(data)               #存储一包的有效数据
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
                    rawWaveData = self.getRawWaveValue(highOrderByte, lowOrderByte)
                    if rawWaveData > 32768:
                        rawWaveData = rawWaveData - 65536
                    #这里存放原始脑波数据
                i = i + valueBytesLength
            else:
                if code == self.PARSER_CODE_POOR_SIGNAL:
                    signal = self.payload[i] & 0xFF
                    i = i + valueBytesLength
                elif code == self.PARSER_CODE_EEG_POWER: #8种脑电波形
                    if signal == 0:
                        highOrderByte = self.payload[i]
                        midOrderByte = self.payload[i + 1]
                        lowOrderByte = self.payload[i + 2]
                        delta = self.getEEGPowerValue(highOrderByte, midOrderByte. lowOrderByte)
                        #这里存放delta波
                        highOrder = self.payload[i + 3]
                        midOrderByte = self.payload[i + 4]
                        lowOrderByte = self.payload[i + 5]
                        theta = self.getEEGPowerValue(highOrderByte, midOrderByte. lowOrderByte)
                        #这里存放theta波
                        highOrder = self.payload[i + 6]
                        midOrderByte = self.payload[i + 7]
                        lowOrderByte = self.payload[i + 8]
                        lowalpha = self.getEEGPowerValue(highOrderByte, midOrderByte. lowOrderByte)
                        #这里存放lowalpha波
                        highOrder = self.payload[i + 9]
                        midOrderByte = self.payload[i + 10]
                        lowOrderByte = self.payload[i + 11]
                        highalpha = self.getEEGPowerValue(highOrderByte, midOrderByte. lowOrderByte)
                        #这里存放highalpha波
                        highOrder = self.payload[i + 12]
                        midOrderByte = self.payload[i + 13]
                        lowOrderByte = self.payload[i + 14]
                        lowbeta = self.getEEGPowerValue(highOrderByte, midOrderByte. lowOrderByte)
                        #这里存放lowbeta波
                        highOrder = self.payload[i + 15]
                        midOrderByte = self.payload[i + 16]
                        lowOrderByte = self.payload[i + 17]
                        highbeta = self.getEEGPowerValue(highOrderByte, midOrderByte. lowOrderByte)
                        #这里存放highbeta波
                        highOrder = self.payload[i + 18]
                        midOrderByte = self.payload[i + 19]
                        lowOrderByte = self.payload[i + 20]
                        lowgamma = self.getEEGPowerValue(highOrderByte, midOrderByte. lowOrderByte)
                        #这里存放lowgamma波
                        highOrder = self.payload[i + 21]
                        midOrderByte = self.payload[i + 22]
                        lowOrderByte = self.payload[i + 23]
                        midgamma = self.getEEGPowerValue(highOrderByte, midOrderByte. lowOrderByte)
                        #这里存放midgamma波
                    i = i + valueBytesLength
                elif code == self.PARSER_CODE_ATTENTION:
                    if signal == 0:
                        attention = self.payload[i] & 0xFF
                        #这里存放注意力
                    i = i + valueBytesLength
                elif code == self.PARSER_CODE_MEDITATION:
                    if signal == 0:
                        meditation = self.payload[i]
                        #这里存放冥想度
                    i = i + valueBytesLength
                elif code == self.PARSER_CODE_DEBUG_ONE:
                    if valueBytesLength == self.EEG_DEBUG_ONE_BYTE_LENGTH:
                        i = i + valueBytesLength
                elif code == self.PARSER_CODE_DEBUG_TWO:
                    if valueBytesLength == self.EEG_DEBUG_TWO_BYTE_LENGTH:
                        i = i + valueBytesLength
        self.parserStatus = self.PARSER_STATE_SYNC
    
    def getRawWaveValue(self, highOrder, lowOrderByte):
        hi = highOrderByte
        lo = (lowOrderByte) & 0xFF
        value = (hi << 8) | lo
        return value
    
    def getEEGPowerValue(self, highOrder, midOrderByte, lowOrderByte):
        hi = highOrderByte
        mi = midOrderByte
        lo = (lowOrderByte) & 0xFF
        value = (hi << 16) | (mi << 8) | lo
        return value

class DataParserECG():
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
            self.payloadSum = 0
            self.parserStatus = self.PARSER_STATE_PAYLOAD
        elif self.parserStatus == self.PARSER_STATE_PAYLOAD:
            self.payload.append(data)               #存储一包的有效数据
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
                    rawWaveData = self.getRawWaveValue(highOrderByte, lowOrderByte)
                    if rawWaveData > 32768:
                        rawWaveData = rawWaveData - 65536
                    #这里存放原始心电数据
                i = i + valueBytesLength
            else:
                if code == self.PARSER_CODE_POOR_SIGNAL:
                    signal = self.payload[i] & 0xFF
                    i = i + valueBytesLength
                elif code == self.PARSER_CODE_HEARTRATE:
                    if signal == 0:
                        heartRateValue = self.payload[i] & 0xFF
                        #这里存放心率值
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
    
    def getRawWaveValue(self, highOrder, lowOrderByte):
        hi = highOrderByte
        lo = (lowOrderByte) & 0xFF
        value = (hi << 8) | lo
        return value