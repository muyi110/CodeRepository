package com.example.data;

import java.util.concurrent.locks.ReentrantLock;

public class DataParserResult {
    private DataParser.EEGRawDataPack[] eeg_raw_buffer;
    private DataParser.EEGRawDataPack[] eeg_raw_buffer0;
    private DataParser.EEGRawDataPack[] eeg_raw_buffer1;
    private int eeg_raw_bufferLen;

    private DataParser.EEGPowerDataPack[] eeg_power_buffer;
    private DataParser.EEGPowerDataPack[] eeg_power_buffer0;
    private DataParser.EEGPowerDataPack[] eeg_power_buffer1;
    private int eeg_power_bufferLen;

    private DataParser.AttentionDataPack[] attention_buffer;
    private DataParser.AttentionDataPack[] attention_buffer0;
    private DataParser.AttentionDataPack[] attention_buffer1;
    private int attention_bufferLen;

    private DataParser.MeditationDataPack[] meditation_buffer;
    private DataParser.MeditationDataPack[] meditation_buffer0;
    private DataParser.MeditationDataPack[] meditation_buffer1;
    private int meditation_bufferLen;

    private DataParser.SignalQualityDataPack[] signal_quality_buffer;
    private DataParser.SignalQualityDataPack[] signal_quality_buffer0;
    private DataParser.SignalQualityDataPack[] signal_quality_buffer1;
    private int signal_quality_bufferLen;

    private DataParser.OtherSensorDataPack[] other_sensor_buffer;
    private DataParser.OtherSensorDataPack[] other_sensor_buffer0;
    private DataParser.OtherSensorDataPack[] other_sensor_buffer1;
    private int other_sensor_bufferLen;

    private ReentrantLock lock = new ReentrantLock();

    public DataParserResult(){
        eeg_raw_buffer0 = eeg_raw_buffer = new DataParser.EEGRawDataPack[10000];
        eeg_raw_buffer1 = new DataParser.EEGRawDataPack[10000];

        eeg_power_buffer0 = eeg_power_buffer = new DataParser.EEGPowerDataPack[512];
        eeg_power_buffer1 = new DataParser.EEGPowerDataPack[512];

        attention_buffer0 = attention_buffer = new DataParser.AttentionDataPack[512];
        attention_buffer1 = new DataParser.AttentionDataPack[512];

        meditation_buffer0 = meditation_buffer = new DataParser.MeditationDataPack[512];
        meditation_buffer1 = new DataParser.MeditationDataPack[512];

        signal_quality_buffer0 = signal_quality_buffer = new DataParser.SignalQualityDataPack[512];
        signal_quality_buffer1 = new DataParser.SignalQualityDataPack[512];

        other_sensor_buffer0 = other_sensor_buffer = new DataParser.OtherSensorDataPack[512];
        other_sensor_buffer1 = new DataParser.OtherSensorDataPack[512];
    }

    public Boolean eeg_raw_put(DataParser.EEGRawDataPack datum){
        Boolean canWrite;
        lock.lock();
        try{
            canWrite = eeg_raw_bufferLen < eeg_raw_buffer.length;
            if (canWrite){
                eeg_raw_buffer[eeg_raw_bufferLen++] = datum;
            }
        }
        finally {
            lock.unlock();
        }
        return canWrite;
    }

    public Boolean eeg_power_put(DataParser.EEGPowerDataPack datum){
        Boolean canWrite;
        lock.lock();
        try{
            canWrite = eeg_power_bufferLen < eeg_power_buffer.length;
            if(canWrite){
                eeg_power_buffer[eeg_power_bufferLen++] = datum;
            }
        }
        finally {
            lock.unlock();
        }
        return canWrite;
    }

    public Boolean attention_put(DataParser.AttentionDataPack datum){
        Boolean canWrite;
        lock.lock();
        try{
            canWrite = attention_bufferLen < attention_buffer.length;
            if(canWrite){
                attention_buffer[attention_bufferLen++] = datum;
            }
        }
        finally {
            lock.unlock();
        }
        return canWrite;
    }

    public Boolean meditation_put(DataParser.MeditationDataPack datum){
        Boolean canWrite;
        lock.lock();
        try{
            canWrite = meditation_bufferLen < meditation_buffer.length;
            if(canWrite){
                meditation_buffer[meditation_bufferLen++] = datum;
            }
        }
        finally {
            lock.unlock();
        }
        return canWrite;
    }

    public Boolean signal_quality_put(DataParser.SignalQualityDataPack datum){
        Boolean canWrite;
        lock.lock();
        try{
            canWrite = signal_quality_bufferLen < signal_quality_buffer.length;
            if(canWrite){
                signal_quality_buffer[signal_quality_bufferLen++] = datum;
            }
        }
        finally {
            lock.unlock();
        }
        return canWrite;
    }

    public Boolean other_sensor_put(DataParser.OtherSensorDataPack datum){
        Boolean canWrite;
        lock.lock();
        try{
            canWrite = other_sensor_bufferLen < other_sensor_buffer.length;
            if(canWrite)
                other_sensor_buffer[other_sensor_bufferLen++] = datum;
        }
        finally {
            lock.unlock();
        }
        return canWrite;
    }

    public DataParser.EEGRawDataPack[] eeg_raw_get(){
        DataParser.EEGRawDataPack[] ret;
        lock.lock();
        try{
            ret = new DataParser.EEGRawDataPack[eeg_raw_bufferLen];
            System.arraycopy(eeg_raw_buffer, 0, ret, 0, eeg_raw_bufferLen);
            eeg_raw_buffer = (eeg_raw_buffer == eeg_raw_buffer0) ? eeg_raw_buffer1 : eeg_raw_buffer0;
            eeg_raw_bufferLen = 0;
        }
        finally {
            lock.unlock();
        }
        return ret;
    }

    public DataParser.EEGPowerDataPack[] eeg_power_get(){
        DataParser.EEGPowerDataPack[] ret;
        lock.lock();
        try{
            ret = new DataParser.EEGPowerDataPack[eeg_power_bufferLen];
            System.arraycopy(eeg_power_buffer, 0, ret, 0, eeg_power_bufferLen);
            eeg_power_buffer = (eeg_power_buffer == eeg_power_buffer0) ? eeg_power_buffer1 : eeg_power_buffer0;
            eeg_power_bufferLen = 0;
        }
        finally {
            lock.unlock();
        }
        return ret;
    }

    public DataParser.AttentionDataPack[] attention_get(){
        DataParser.AttentionDataPack[] ret;
        lock.lock();
        try{
            ret = new DataParser.AttentionDataPack[attention_bufferLen];
            System.arraycopy(attention_buffer, 0, ret, 0, attention_bufferLen);
            attention_buffer = (attention_buffer == attention_buffer0) ? attention_buffer1 : attention_buffer0;
            attention_bufferLen = 0;
        }
        finally {
            lock.unlock();
        }
        return ret;
    }

    public DataParser.MeditationDataPack[] meditation_get(){
        DataParser.MeditationDataPack[] ret;
        lock.lock();
        try{
            ret = new DataParser.MeditationDataPack[meditation_bufferLen];
            System.arraycopy(meditation_buffer, 0, ret, 0, meditation_bufferLen);
            meditation_buffer = (meditation_buffer == meditation_buffer0) ? meditation_buffer1 : meditation_buffer0;
            meditation_bufferLen = 0;
        }
        finally {
            lock.unlock();
        }
        return ret;
    }

    public DataParser.SignalQualityDataPack[] signal_quality_get(){
        DataParser.SignalQualityDataPack[] ret;
        lock.lock();
        try{
            ret = new DataParser.SignalQualityDataPack[signal_quality_bufferLen];
            System.arraycopy(signal_quality_buffer, 0, ret, 0, signal_quality_bufferLen);
            signal_quality_buffer = (signal_quality_buffer == signal_quality_buffer0) ? signal_quality_buffer1 : signal_quality_buffer0;
        }
        finally {
            lock.unlock();
        }
        return ret;
    }

    public DataParser.OtherSensorDataPack[] other_sensor_get(){
        DataParser.OtherSensorDataPack[] ret;
        lock.lock();
        try{
            ret = new DataParser.OtherSensorDataPack[other_sensor_bufferLen];
            System.arraycopy(other_sensor_buffer,0,ret,0,other_sensor_bufferLen);
            other_sensor_buffer = (other_sensor_buffer == other_sensor_buffer0) ? other_sensor_buffer1 : other_sensor_buffer0;
            other_sensor_bufferLen = 0;
        }
        finally {
            lock.unlock();
        }
        return ret;
    }
}
