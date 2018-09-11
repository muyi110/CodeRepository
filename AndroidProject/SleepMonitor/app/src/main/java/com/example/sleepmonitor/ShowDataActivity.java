package com.example.sleepmonitor;

import android.content.Intent;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.widget.TextView;

import com.example.bluetooth.Bluetooth;

import java.lang.ref.WeakReference;

public class ShowDataActivity extends AppCompatActivity {

    private static final int UPDATE_DATA = 1;
    private static final String TAG = "ShowDataActivity";
    public TextView mTextView;
    private MyHandle mMyHandle = new MyHandle(this);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_data);

        mTextView = findViewById(R.id.textViewReceiveDataShow);
        mTextView.setMovementMethod(ScrollingMovementMethod.getInstance());

        GetDataThread getdataThread = new GetDataThread();
        getdataThread.start();
    }

    private class GetDataThread extends Thread{
        @Override
        public void run() {
            while(true) {
                try {
                    //get received data
                    byte[] result = Bluetooth.mDataReceive.get();
                    StringBuilder mStringBuilder = Bluetooth.bytesToHexString(result);
                    mMyHandle.obtainMessage(UPDATE_DATA, result.length, -1,
                            mStringBuilder).sendToTarget();
                    Thread.sleep(100);
                } catch (Exception e) {
                    Log.e(TAG, "Data get error !");
                    break;
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
        finish();
    }
}