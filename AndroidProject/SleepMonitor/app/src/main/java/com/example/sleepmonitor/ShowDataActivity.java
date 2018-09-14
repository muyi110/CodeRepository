package com.example.sleepmonitor;

import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.widget.TextView;

import com.example.bluetooth.Bluetooth;
import com.example.data.DataParser;

import java.lang.ref.WeakReference;

public class ShowDataActivity extends AppCompatActivity {

    private static final int UPDATE_DATA = 1;
    private static final String TAG = "ShowDataActivity";
    private Boolean parser_complete_flag = false;
    public TextView mTextView;
    private MyHandle mMyHandle = new MyHandle(this);
    private DataParser dataParser = new DataParser();
    private Boolean getDataThreadStopFlag = false;
    private Boolean getParserDataThreadStopFlag = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_data);

        mTextView = findViewById(R.id.textViewReceiveDataShow);
        mTextView.setMovementMethod(ScrollingMovementMethod.getInstance());

        GetDataThread getdataThread = new GetDataThread();
        getdataThread.start();
        GetParserDataThread getParserDataThread = new GetParserDataThread();
        getParserDataThread.start();
    }

    private class GetDataThread extends Thread{
        @Override
        public void run() {
            while(!getDataThreadStopFlag) {
                try {
                    //get received data
                    byte[] result = Bluetooth.mDataReceive.get();
                    for (byte byte_element:result) {
                        if(dataParser.parserByte(byte_element) < 0)
                            Log.d(TAG, "Data Parser error!!");
                    }
                    parser_complete_flag = true;
                    //StringBuilder mStringBuilder = Bluetooth.bytesToHexString(result);
                    //mMyHandle.obtainMessage(UPDATE_DATA, result.length, -1,
                            //mStringBuilder).sendToTarget();
                    Thread.sleep(100);
                } catch (Exception e) {
                    Log.e(TAG, "Data get error !");
                    break;
                }
            }
        }
    }

    private class GetParserDataThread extends Thread{
        @Override
        public void run() {
            StringBuilder stringBuilder = new StringBuilder();
            while(!getParserDataThreadStopFlag) {
                if(parser_complete_flag) {
                    try {
                        DataParser.OtherSensorDataPack[] otherSensorDataPack =
                                DataParser.dataParserResult.other_sensor_get();
                        for (DataParser.OtherSensorDataPack element : otherSensorDataPack) {
                            stringBuilder.append("mpu6050 pitch: ");
                            stringBuilder.append(Float.toString(element.mpu6050_pitch));
                            stringBuilder.append('\n');
                            stringBuilder.append("mpu6050 roll: ");
                            stringBuilder.append(Float.toString(element.mpu6050_roll));
                            stringBuilder.append('\n');
                            stringBuilder.append("mpu6050 yaw: ");
                            stringBuilder.append(Float.toString(element.mpu6050_yaw));
                            stringBuilder.append('\n');
                            stringBuilder.append("sht11 temp: ");
                            stringBuilder.append(Float.toString(element.sht11_temp));
                            stringBuilder.append('\n');
                            stringBuilder.append("sht11 humi: ");
                            stringBuilder.append(Float.toString(element.sht11_humi));
                            stringBuilder.append('\n');
                            stringBuilder.append("mlx90615 temp: ");
                            stringBuilder.append(Float.toString(element.mlx90615_temp));
                            stringBuilder.append('\n');
                            stringBuilder.append('\n');
                        }
                        mMyHandle.obtainMessage(UPDATE_DATA, otherSensorDataPack.length, -1,
                                stringBuilder).sendToTarget();
                        parser_complete_flag = false;
                        Thread.sleep(100);
                    } catch (Exception e) {
                        Log.e(TAG, "Data parser result get error !");
                        break;
                    }
                }
            }
        }
    }

    private static class MyHandle extends Handler{
        private final WeakReference<ShowDataActivity> mActivity;
        MyHandle(ShowDataActivity activity){
            mActivity = new WeakReference<>(activity);
        }
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            switch (msg.what){
                case UPDATE_DATA:
                    int offset=mActivity.get().mTextView.getLineCount()*mActivity.get().mTextView.getLineHeight();
                    if (offset > mActivity.get().mTextView.getHeight()) {
                        mActivity.get().mTextView.scrollTo(0,offset - mActivity.get().mTextView.getHeight());
                    }
                    mActivity.get().mTextView.append(msg.obj.toString());
                    break;
                default:
                    break;
            }
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        getDataThreadStopFlag = true;
        getParserDataThreadStopFlag = true;
        finish();
    }
}