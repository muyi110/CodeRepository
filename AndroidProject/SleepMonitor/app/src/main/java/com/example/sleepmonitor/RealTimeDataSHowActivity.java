package com.example.sleepmonitor;

import android.graphics.Color;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.WindowManager;
import android.widget.TextView;

import com.example.bluetooth.Bluetooth;
import com.example.data.DataParser;
import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.interfaces.datasets.ILineDataSet;

import java.lang.ref.WeakReference;

public class RealTimeDataSHowActivity extends AppCompatActivity {

    private static final int UPDATE_DATA = 1;
    private static final String TAG = "RealTimeShowActivity";
    private static final int UPDATE_SHT11_TEMP = 2;
    private static final int UPDATE_SHT11_HUMI = 3;
    private static final int UPDATE_BODY_TEMP = 4;
    private static final int UPDATE_HEAD_MOVE = 5;
    private Boolean parser_complete_flag = false;
    private MyHandle mMyHandle = new MyHandle(this);
    private DataParser dataParser = new DataParser();
    private Boolean getDataThreadStopFlag = false;
    private Boolean getParserDataThreadStopFlag = false;
    private int t = 0;

    private TextView sht11_temp_textView;
    private TextView sht11_humi_textView;
    private TextView body_temp_textView;
    private TextView head_move_textView;
    private LineChart mChart;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_real_time_data_show);
        sht11_temp_textView = findViewById(R.id.sht11_temp_textView);
        sht11_humi_textView = findViewById(R.id.sht11_humi_textView);
        body_temp_textView = findViewById(R.id.body_temp_textView);
        head_move_textView = findViewById(R.id.head_move_textView);
        mChart = findViewById(R.id.chart);
        mChart.setDrawGridBackground(false);
        mChart.getDescription().setEnabled(false);
        mChart.setData(new LineData());

        GetDataThread getdataThread = new GetDataThread();
        getdataThread.start();
        GetParserDataThread getParserDataThread = new GetParserDataThread();
        getParserDataThread.start();

        mChart.invalidate();
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
            float sht11_temp = 0;
            float sht11_humi = 0;
            float body_temp = 0;
            float pitch = 0, roll = 0, yaw = 0;
            while(!getParserDataThreadStopFlag) {
                if(parser_complete_flag) {
                    try {
                        StringBuilder stringBuilder_sht11_temp = new StringBuilder();
                        StringBuilder stringBuilder_sht11_humi = new StringBuilder();
                        StringBuilder stringBuilder_body_temp = new StringBuilder();
                        StringBuilder stringBuilder_head_move = new StringBuilder();

                        DataParser.OtherSensorDataPack[] otherSensorDataPack = DataParser.dataParserResult.other_sensor_get();
                        DataParser.EEGRawDataPack[] eegRawDataPacks = DataParser.dataParserResult.eeg_raw_get();
                        for (DataParser.OtherSensorDataPack element : otherSensorDataPack) {
                            sht11_temp = element.sht11_temp;
                            sht11_humi = element.sht11_humi;
                            body_temp = element.mlx90615_temp;
                            pitch = element.mpu6050_pitch;
                            roll = element.mpu6050_roll;
                            yaw = element.mpu6050_yaw;
                        }
                        stringBuilder_sht11_temp.append(Float.toString(sht11_temp));
                        stringBuilder_sht11_temp.append("℃");
                        stringBuilder_sht11_humi.append(Float.toString(sht11_humi));
                        stringBuilder_sht11_humi.append("%");
                        stringBuilder_body_temp.append(Float.toString(body_temp));
                        stringBuilder_body_temp.append("℃");
                        stringBuilder_head_move.append("pitch: ");
                        stringBuilder_head_move.append(Float.toString(pitch));
                        stringBuilder_head_move.append("°");
                        stringBuilder_head_move.append("   ");
                        stringBuilder_head_move.append("roll: ");
                        stringBuilder_head_move.append(Float.toString(roll));
                        stringBuilder_head_move.append("°");
                        stringBuilder_head_move.append("   ");
                        stringBuilder_head_move.append("yaw: ");
                        stringBuilder_head_move.append(Float.toString(yaw));
                        stringBuilder_head_move.append("°");
                        stringBuilder_head_move.append("   ");


                        mMyHandle.obtainMessage(UPDATE_DATA, eegRawDataPacks.length, -1,
                                eegRawDataPacks).sendToTarget();
                        mMyHandle.obtainMessage(UPDATE_SHT11_TEMP, -1, -1, stringBuilder_sht11_temp).sendToTarget();
                        mMyHandle.obtainMessage(UPDATE_SHT11_HUMI, -1, -1, stringBuilder_sht11_humi).sendToTarget();
                        mMyHandle.obtainMessage(UPDATE_BODY_TEMP, -1, -1, stringBuilder_body_temp).sendToTarget();
                        mMyHandle.obtainMessage(UPDATE_HEAD_MOVE, -1, -1, stringBuilder_head_move).sendToTarget();
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

    private static class MyHandle extends Handler {
        private final WeakReference<RealTimeDataSHowActivity> mActivity;
        MyHandle(RealTimeDataSHowActivity activity){
            mActivity = new WeakReference<>(activity);
        }
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            switch (msg.what){
                case UPDATE_DATA:
                    LineData data = mActivity.get().mChart.getData();
                    ILineDataSet set = data.getDataSetByIndex(0);
                    if(set == null){
                        LineDataSet sets = new LineDataSet(null, "eeg");
                        sets.setLineWidth(2.5f);
                        //sets.setCircleRadius(4.5f);
                        sets.setColor(Color.rgb(240, 99, 99));
                        //sets.setCircleColor(Color.rgb(240, 99, 99));
                        //sets.setHighLightColor(Color.rgb(190, 190, 190));
                        sets.setAxisDependency(YAxis.AxisDependency.LEFT);
                        sets.setHighlightEnabled(false);
                        sets.setDrawCircles(false);
                        sets.setDrawValues(false);
                        //sets.setValueTextSize(10f);
                        data.addDataSet(sets);
                    }
                    if(((DataParser.EEGRawDataPack[])msg.obj).length > 0) {
                        for (DataParser.EEGRawDataPack element : (DataParser.EEGRawDataPack[]) msg.obj) {
                            data.addEntry(new Entry((float) mActivity.get().t++ / 1000, (float) element.rawData / 6), 0);
                        }
                    }
                    else {
                        data.addEntry(new Entry((float) mActivity.get().t++ / 1000, 0f), 0);
                    }
                    data.notifyDataChanged();
                    mActivity.get().mChart.notifyDataSetChanged();
                    mActivity.get().mChart.setVisibleXRangeMaximum(10);
                    mActivity.get().mChart.moveViewTo(data.getEntryCount() - 11, 0f, YAxis.AxisDependency.LEFT);
                    break;
                case UPDATE_SHT11_TEMP:
                    mActivity.get().sht11_temp_textView.setText(msg.obj.toString());
                    break;
                case UPDATE_SHT11_HUMI:
                    mActivity.get().sht11_humi_textView.setText(msg.obj.toString());
                    break;
                case UPDATE_BODY_TEMP:
                    mActivity.get().body_temp_textView.setText(msg.obj.toString());
                    break;
                case UPDATE_HEAD_MOVE:
                    mActivity.get().head_move_textView.setText(msg.obj.toString());
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
