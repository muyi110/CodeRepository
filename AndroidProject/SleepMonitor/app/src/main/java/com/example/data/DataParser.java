package com.example.data;

public class DataParser {
    private static final int PARSER_CODE_ATTENTION = 0x04;
    private static final int PARSER_CODE_MEDITATION = 0x05;
    private static final int PARSER_CODE_POOR_SIGNAL = 0x02;
    private static final int PARSER_CODE_EEG_RAW = 0x80;
    private static final int PARSER_CODE_EEG_POWER = 0X83;
    private static final int PARSER_CODE_MPU6050 = 0x06;
    private static final int PARSER_CODE_SHT11 = 0x07;
    private static final int PARSER_CODE_MLX90615 = 0x08;

    private static final int PARSER_SYNC_BYTE = 0xAA;

    private static final int PARSER_STATE_SYNC = 1;
    private static final int PARSER_STATE_SYNC_CHECK = 2;
    private static final int PARSER_STATE_PAYLOAD_LENGTH = 3;
    private static final int PARSER_STATE_PAYLOAD = 4;
    private static final int PARSER_STATE_CHKSUM = 5;

    private int parserStatus;
    private int payloadLength;
    private int payloadBytesReceived;
    private int payloadSum;
    private int checkSum;
    private byte[] payload = new byte[512];

    private EEGPowerDataPack eegPowerDataPack = new EEGPowerDataPack();
    private EEGRawDataPack eegRawDataPack = new EEGRawDataPack();
    private OtherSensorDataPack otherSensorDataPack = new OtherSensorDataPack();

    public DataParser(){
        parserStatus = PARSER_STATE_SYNC;
    }
    public int parserByte(byte buffer){
        int returnValue = 0;
        switch (parserStatus){
            case 1:
                if((buffer & 0xFF) != PARSER_SYNC_BYTE) break;
                parserStatus = PARSER_STATE_SYNC_CHECK;
                break;
            case 2:
                if((buffer & 0xFF) == PARSER_SYNC_BYTE)
                    parserStatus = PARSER_STATE_PAYLOAD_LENGTH;
                else
                    parserStatus = PARSER_STATE_SYNC;
                break;
            case 3:
                payloadLength = (buffer & 0xFF);
                payloadBytesReceived = 0;
                payloadSum = 0;
                parserStatus = PARSER_STATE_PAYLOAD;
                break;
            case 4:
                payload[payloadBytesReceived++] = buffer;
                payloadSum += (buffer & 0xFF);
                if(payloadBytesReceived < payloadLength) break;
                parserStatus = PARSER_STATE_CHKSUM;
                break;
            case 5:
                checkSum = (buffer & 0xFF);
                parserStatus = PARSER_STATE_SYNC;
                if(checkSum != ((~payloadSum) & 0xFF)){
                    returnValue = -2;
                }
                else{
                    returnValue = 1;
                    parsePacketPayload();
                }
                break;
        }
        return returnValue;
    }
    private void parsePacketPayload(){
        int i = 0;
        int valueBytesLength;
        int code;

        while (i < payloadLength){
            code = payload[i++] & 0xFF;
            valueBytesLength = payload[i++] & 0xFF;
            if(code == PARSER_CODE_EEG_RAW){
                int count = 0;
                byte highOrderByte;
                byte lowOrderByte;
                while(count < valueBytesLength) {
                    highOrderByte = payload[i+count];
                    count++;
                    lowOrderByte = payload[(i + count)];
                    count++;
                    eegRawDataPack.rawData = getRawWaveValue(highOrderByte, lowOrderByte);
                    if (eegRawDataPack.rawData > 32768) eegRawDataPack.rawData -= 65536;
                    //这里将原始数据存放在缓冲中
                }
                i += valueBytesLength;
            }
            else{
                switch (code){}
            }
        }

    }
    private int getRawWaveValue(byte highOrderByte, byte lowOrderByte){
        int hi = (int)highOrderByte;
        int lo = ((int)lowOrderByte) & 0xFF;
        return (hi << 8) | lo;
    }
    private int getEEGPowerValue(byte highOrderByte, byte midOrderByte, byte lowOrderByte){
        int hi = (int)highOrderByte;
        int mi = (int)midOrderByte;
        int lo = ((int)lowOrderByte) & 0xFF;
        return (hi << 16) | (mi << 8) | lo;
    }

    private class EEGPowerDataPack{
        public int delta;
        public int theta;
        public int lowalpha;
        public int highalpha;
        public int lowbeta;
        public int highbeta;
        public int lowgamma;
        public int midgamma;
        public int attention;
        public int meditation;
    }
    private class EEGRawDataPack{
        private int rawData;
    }
    private class OtherSensorDataPack{
        public float mpu6050_pitch;
        public float mpu6050_roll;
        public float mpu6050_yaw;
        public float sht11_temp;
        public float sht11_humi;
        public float mlx90615_temp;
    }
}