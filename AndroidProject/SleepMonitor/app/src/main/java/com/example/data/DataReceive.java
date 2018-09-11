package com.example.data;

import java.util.concurrent.locks.ReentrantLock;

public class DataReceive {

    private byte[] buffer;
    private byte[] buffer0;
    private byte[] buffer1;
    private int bufferLen;
    private ReentrantLock lock = new ReentrantLock();

    public DataReceive(){
        buffer0 = buffer = new byte[10000];
        buffer1 = new byte[10000];
    }

    public Boolean put(byte datum){
        Boolean canWrite;
        lock.lock();
        try{
            canWrite = bufferLen < buffer.length;
            if (canWrite){
                buffer[bufferLen++] = datum;
            }
        }
        finally {
            lock.unlock();
        }
        return canWrite;
    }

    public byte[] get(){
        byte[] ret;
        lock.lock();
        try{
            ret = new byte[bufferLen];
            System.arraycopy(buffer, 0, ret, 0, bufferLen);
            buffer = (buffer == buffer0) ? buffer1 : buffer0;
            bufferLen = 0;
        }
        finally {
            lock.unlock();
        }
        return ret;
    }
}
