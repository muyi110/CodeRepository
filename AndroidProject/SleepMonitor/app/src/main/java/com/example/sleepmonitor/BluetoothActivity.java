package com.example.sleepmonitor;

import android.content.Intent;
import android.content.IntentFilter;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import com.example.bluetooth.Bluetooth;


public class BluetoothActivity extends AppCompatActivity {

    final Bluetooth mBluetooth = new Bluetooth();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bluetooth);
        //Create an Bluetooth instance
        ListView mListView = findViewById(R.id.listView_devices);

        mBluetooth.bluetoothInitialization();
        //Get pair bluetooth
        mBluetooth.getPairBluetoothDevice();
        mBluetooth.mArrayAdapter = new ArrayAdapter<>(BluetoothActivity.this,
                android.R.layout.simple_list_item_1, mBluetooth.mArrayList);

        mListView.setAdapter(mBluetooth.mArrayAdapter);
        mListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                //Connect bluetooth
                mBluetooth.connectBluetooth(position);
                //Open data show UI
                Intent mIntent = new Intent(BluetoothActivity.this, RealTimeDataSHowActivity.class);
                startActivity(mIntent);
            }
        });
        //Open bluetooth
        mBluetooth.startBluetooth();
        //Search bluetooth devices
        mBluetooth.searchBluetoothDevices();
        //Create a broadcastReceiver for ACTION_FOUND
        IntentFilter mIntentFilter = mBluetooth.createBroadcastReceiver();
        registerReceiver(mBluetooth.mReceiver, mIntentFilter);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        new Thread(new Runnable() {
            @Override
            public void run() {
               mBluetooth.stop();
            }
        }).start();
        //unregister broadcastReceiver
        unregisterReceiver(mBluetooth.mReceiver);
        //Close bluetooth
        mBluetooth.mBluetoothAdapter.disable();
        android.os.Process.killProcess(android.os.Process.myPid());
    }
}
