package com.example.data;

import android.util.Log;

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
    private byte[] payload = new byte[512];

    private EEGPowerDataPack eegPowerDataPack = new EEGPowerDataPack();
    private EEGRawDataPack eegRawDataPack = new EEGRawDataPack();
    private AttentionDataPack attentionDataPack = new AttentionDataPack();
    private MeditationDataPack meditationDataPack = new MeditationDataPack();
    private SignalQualityDataPack signalQualityDataPack = new SignalQualityDataPack();
    private OtherSensorDataPack otherSensorDataPack = new OtherSensorDataPack();

    public static final DataParserResult dataParserResult = new DataParserResult();

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
                int checkSum = (buffer & 0xFF);
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
            if(code == PARSER_CODE_MPU6050){
                otherSensorDataPack.mpu6050_pitch = ((int)payload[i] << 8 | (int)payload[i + 1] & 0xFF) / 100;
                otherSensorDataPack.mpu6050_roll = ((int)payload[i + 2] << 8 | (int)payload[i + 3] & 0xFF) / 100;
                otherSensorDataPack.mpu6050_yaw = ((int)payload[i + 4] << 8 | (int)payload[i + 5] & 0xFF) / 100;
                i += valueBytesLength;
            }
            if(code == PARSER_CODE_SHT11){
                otherSensorDataPack.sht11_temp = ((int)payload[i] << 8 | (int)payload[i + 1] & 0xFF) / 100;
                otherSensorDataPack.sht11_humi = ((int)payload[i + 2] << 8 | (int)payload[i + 3] & 0xFF) / 100;
                i += valueBytesLength;
            }
            if(code == PARSER_CODE_MLX90615){
                otherSensorDataPack.mlx90615_temp = ((int)payload[i] << 8 | (int)payload[i + 1] & 0xFF) / 100;
                i += valueBytesLength;
                if(!dataParserResult.other_sensor_put(otherSensorDataPack)){
                    Log.d("DataParser", "data parser put error!!!!");
                    return;
                }
            }
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
                    if(!dataParserResult.eeg_raw_put(eegRawDataPack)){
                        Log.d("DataParser", "data parser put error!!!!");
                        return;
                    }
                }
                i += valueBytesLength;
            }
            else{
                switch (code){
                    case PARSER_CODE_EEG_POWER:
                        byte highOrderByte;
                        byte lowOrderByte;
                        byte midOrderByte;
                        int count = 0;
                        while(count < valueBytesLength){
                            highOrderByte = payload[i + count];
                            count++;
                            midOrderByte = payload[i + count];
                            count++;
                            lowOrderByte = payload[i + count];
                            count++;
                            eegPowerDataPack.delta = getEEGPowerValue(highOrderByte, midOrderByte, lowOrderByte);
                            highOrderByte = payload[i + count];
                            count++;
                            midOrderByte = payload[i + count];
                            count++;
                            lowOrderByte = payload[i + count];
                            count++;
                            eegPowerDataPack.theta = getEEGPowerValue(highOrderByte, midOrderByte, lowOrderByte);
                            highOrderByte = payload[i + count];
                            count++;
                            midOrderByte = payload[i + count];
                            count++;
                            lowOrderByte = payload[i + count];
                            count++;
                            eegPowerDataPack.lowalpha = getEEGPowerValue(highOrderByte, midOrderByte, lowOrderByte);
                            highOrderByte = payload[i + count];
                            count++;
                            midOrderByte = payload[i + count];
                            count++;
                            lowOrderByte = payload[i + count];
                            count++;
                            eegPowerDataPack.highalpha = getEEGPowerValue(highOrderByte, midOrderByte, lowOrderByte);
                            highOrderByte = payload[i + count];
                            count++;
                            midOrderByte = payload[i + count];
                            count++;
                            lowOrderByte = payload[i + count];
                            count++;
                            eegPowerDataPack.lowbeta = getEEGPowerValue(highOrderByte, midOrderByte, lowOrderByte);
                            highOrderByte = payload[i + count];
                            count++;
                            midOrderByte = payload[i + count];
                            count++;
                            lowOrderByte = payload[i + count];
                            count++;
                            eegPowerDataPack.highbeta = getEEGPowerValue(highOrderByte, midOrderByte, lowOrderByte);
                            highOrderByte = payload[i + count];
                            count++;
                            midOrderByte = payload[i + count];
                            count++;
                            lowOrderByte = payload[i + count];
                            count++;
                            eegPowerDataPack.lowgamma = getEEGPowerValue(highOrderByte, midOrderByte, lowOrderByte);
                            highOrderByte = payload[i + count];
                            count++;
                            midOrderByte = payload[i + count];
                            count++;
                            lowOrderByte = payload[i + count];
                            count++;
                            eegPowerDataPack.midgamma = getEEGPowerValue(highOrderByte, midOrderByte, lowOrderByte);
                            if(!dataParserResult.eeg_power_put(eegPowerDataPack)){
                                Log.d("DataParser", "data parser put error!!!!");
                                return;
                            }
                        }
                        i += valueBytesLength;
                        break;
                    case PARSER_CODE_ATTENTION:
                        int attention_count = 0;
                        byte attention_orderByte;
                        while(attention_count < valueBytesLength){
                            attention_orderByte = payload[i + attention_count];
                            attention_count++;
                            attentionDataPack.attention = attention_orderByte;
                            if(!dataParserResult.attention_put(attentionDataPack)){
                                Log.d("DataParser", "data parser put error!!!!");
                                return;
                            }
                        }
                        i += valueBytesLength;
                        break;
                    case PARSER_CODE_MEDITATION:
                        int meditation_count = 0;
                        byte meditation_orderByte;
                        while(meditation_count < valueBytesLength){
                            meditation_orderByte = payload[i + meditation_count];
                            meditation_count++;
                            meditationDataPack.meditation = meditation_orderByte;
                            if(!dataParserResult.meditation_put(meditationDataPack)){
                                Log.d("DataParser", "data parser put error!!!!");
                                return;
                            }
                        }
                        i += valueBytesLength;
                        break;
                    case PARSER_CODE_POOR_SIGNAL:
                        int signal_count = 0;
                        byte signal_orderByte;
                        while(signal_count < valueBytesLength){
                            signal_orderByte = payload[i+signal_count];
                            signal_count++;
                            signalQualityDataPack.signal_quality = signal_orderByte;
                            if(!dataParserResult.signal_quality_put(signalQualityDataPack)){
                                Log.d("DataParser", "data parser put error!!!!");
                                return;
                            }
                        }
                        i += valueBytesLength;
                        break;
                    default: break;
                }
            }
        }
        parserStatus = PARSER_STATE_SYNC;
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

    public class EEGPowerDataPack{
        public int delta;
        public int theta;
        public int lowalpha;
        public int highalpha;
        public int lowbeta;
        public int highbeta;
        public int lowgamma;
        public int midgamma;
    }
    public class AttentionDataPack{
        public int attention;
    }
    public class MeditationDataPack{ ;
        public int meditation;
    }
    public class SignalQualityDataPack{
        public int signal_quality;
    }
    public class EEGRawDataPack{
        public int rawData;
    }
    public class OtherSensorDataPack{
        public float mpu6050_pitch;
        public float mpu6050_roll;
        public float mpu6050_yaw;
        public float sht11_temp;
        public float sht11_humi;
        public float mlx90615_temp;
    }
}