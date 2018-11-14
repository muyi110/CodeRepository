package com.example.bluetooth;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.util.Log;
import android.widget.ArrayAdapter;

import com.example.data.DataReceive;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Set;
import java.util.UUID;

public class Bluetooth {
    private static final String TAG = "BluetoothModel";
    private UUID uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    public BluetoothAdapter mBluetoothAdapter = null;
    public BroadcastReceiver mReceiver;
    public ArrayAdapter<String> mArrayAdapter = null;

    private ConnectThread mConnectThread;
    private ConnectedThread mConnectedThread;
    public ArrayList<String> mArrayList;

    private BluetoothSocket mmSocket = null;
    public static final DataReceive mDataReceive = new DataReceive();

    /********************************************************************
     * Bluetooth initialization method
     *******************************************************************/
    public void bluetoothInitialization(){
        mArrayList = new ArrayList<>();
        //get bluetoothAdapter
        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    }
    /********************************************************************
     * create a broadcastReceiver for ACTION_FOUND
     *******************************************************************/
    public IntentFilter createBroadcastReceiver() {
        mReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                String action = intent.getAction();
                // When discovery finds a device
                if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                    // Get the BluetoothDevice object from the Intent
                    BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                    // Add the name and address to an array adapter to show in a ListView
                    mArrayAdapter.add(device.getName() + "\n" + device.getAddress());
                    String dev = device.getName() + "\n" + device.getAddress();
                    if (!mArrayList.contains(dev)) {
                        mArrayList.add(dev);
                    }
                    mArrayAdapter.notifyDataSetChanged();
                }
                else if (BluetoothAdapter.ACTION_DISCOVERY_FINISHED.equals(action)){
                    Log.d(TAG, "Search over!");
                }
            }
        };
        //register the broadcastReceiver
        IntentFilter filter = new IntentFilter();
        filter.addAction(BluetoothDevice.ACTION_FOUND);
        filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED);
        return filter;
    }
    /********************************************************************
     * Connect bluetooth device method
     *******************************************************************/
    public void connectBluetooth(int position){
        if(mmSocket != null){
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try{
                        if(mmSocket.isConnected()){
                            mmSocket.close();
                        }
                    }
                    catch (IOException e){
                        e.printStackTrace();
                    }
                }
            }).start();
        }
        if(mBluetoothAdapter.isDiscovering()){
            mBluetoothAdapter.cancelDiscovery();
        }
        try {
            String devices = mArrayAdapter.getItem(position);
            String address = devices.substring(devices.indexOf("\n") + 1).trim();
            BluetoothDevice mBluetoothDevice = mBluetoothAdapter.getRemoteDevice(address);
            mConnectThread = new ConnectThread(mBluetoothDevice);
            mConnectThread.start();
        }
        catch (NullPointerException e){
            e.printStackTrace();
        }
    }
    /********************************************************************
     * Get pair bluetooth device method
     *******************************************************************/
    public void getPairBluetoothDevice(){
        Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();
        // If there are paired devices
        if (pairedDevices.size() > 0) {
            // Loop through paired devices
            for (BluetoothDevice device : pairedDevices) {
                // Add the name and address to an array adapter to show in a ListView
                mArrayList.add(device.getName() + "\n" + device.getAddress());
            }
        }
    }
    /********************************************************************
     * Open phone's bluetooth method
     *******************************************************************/
    public void startBluetooth(){
        if (mBluetoothAdapter != null) {
            if (!mBluetoothAdapter.isEnabled()) {
                mBluetoothAdapter.enable();
                mBluetoothAdapter.cancelDiscovery();
            }
        }
    }
    /********************************************************************
     * Open phone's bluetooth method
     *******************************************************************/
    public void searchBluetoothDevices(){
        while (!mBluetoothAdapter.startDiscovery()) {
            Log.d(TAG, "No found devices");
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
    /********************************************************************
     * Bluetooth stop method
     *******************************************************************/
    public void stop(){
        mConnectThread.cancel();
        mConnectedThread.cancel();
    }
    /********************************************************************
     * Connect as server class
     *******************************************************************/
    private class AcceptThread extends Thread {
        private final BluetoothServerSocket mmServerSocket;

        public AcceptThread() {
            BluetoothServerSocket tmp = null;
            try {
                tmp = mBluetoothAdapter.listenUsingRfcommWithServiceRecord("SleepMonitor", uuid);
            } catch (IOException e) {
                e.printStackTrace();
            }
            mmServerSocket = tmp;
        }
        public void run() {
            BluetoothSocket socket;
            // Keep listening until exception occurs or a socket is returned
            while (true) {
                try {
                    socket = mmServerSocket.accept();
                } catch (IOException e) {
                    break;
                }
                // If a connection was accepted
                if (socket != null) {
                    // Do work to manage the connection (in a separate thread)
                    mConnectedThread = new ConnectedThread(socket);
                    mConnectedThread.start();
                    try {
                        mmServerSocket.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    break;
                }
            }
        }
        public void cancel() {
            try {
                mmServerSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    /********************************************************************
     * Connect as client class
     *******************************************************************/
    private class ConnectThread extends Thread {
        private final BluetoothDevice mmDevice;

        private ConnectThread(BluetoothDevice device) {
            // Use a temporary object that is later assigned to mmSocket,
            // because mmSocket is final
            BluetoothSocket tmp = null;
            mmDevice = device;
            // Get a BluetoothSocket to connect with the given BluetoothDevice
            try {
                // uuid is the app's UUID string, also used by the server code
                tmp = mmDevice.createRfcommSocketToServiceRecord(uuid);
            } catch (IOException e) {
                e.printStackTrace();
            }
            mmSocket = tmp;
        }
        public void run() {
            // Cancel discovery because it will slow down the connection
            mBluetoothAdapter.cancelDiscovery();
            try {
                // Connect the device through the socket. This will block
                // until it succeeds or throws an exception
                mmSocket.connect();
            } catch (IOException connectException) {
                // Unable to connect; close the socket and get out
                try {
                    mmSocket.close();
                } catch (IOException closeException) {
                    closeException.printStackTrace();
                }
                return;
            }
            // Do work to manage the connection (in a separate thread)
            mConnectedThread = new ConnectedThread(mmSocket);
            mConnectedThread.start();
        }
        private void cancel() {
            try {
                mmSocket.close();
            }
            catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    /********************************************************************
     * Management connection class
     *******************************************************************/
    private class ConnectedThread extends Thread {
        private final BluetoothSocket mmSocket;
        private final InputStream mmInStream;
        private final OutputStream mmOutStream;

        private ConnectedThread(BluetoothSocket socket) {
            mmSocket = socket;
            InputStream tmpIn = null;
            OutputStream tmpOut = null;

            // Get the input and output streams, using temp objects because
            // member streams are final
            try {
                tmpIn = socket.getInputStream();
                tmpOut = socket.getOutputStream();
            } catch (IOException e) {
                e.printStackTrace();
            }

            mmInStream = tmpIn;
            mmOutStream = tmpOut;
        }
        public void run() {
            byte[] buffer = new byte[1024];  // buffer store for the stream
            int bytes; // bytes returned from read()

            // Keep listening to the InputStream until an exception occurs
            while (true) {
                try {
                    // Read from the InputStream
                    bytes = mmInStream.read(buffer);
                    //Put received data to buffer
                    for(int i = 0; i < bytes; ++i) {
                        if (!mDataReceive.put(buffer[i])) {
                            Log.d(TAG, "data put error!!");
                            break;
                        }
                    }
                }
                catch (IOException e) {
                    break;
                }
            }
        }
        /* Call this from the main activity to send data to the remote device */
        public void write(byte[] bytes) {
            try {
                mmOutStream.write(bytes);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        /* Call this from the main activity to shutdown the connection */
        private void cancel() {
            try {
                mmInStream.close();
                mmOutStream.close();
                mmSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    /********************************************************************
     * Conversion bytes to hexString method
     *******************************************************************/
    public static StringBuilder bytesToHexString(byte[] bytes) {
        StringBuilder results = new StringBuilder();
        for (int i = 0; i < bytes.length; i++) {
            String hexString = Integer.toHexString(bytes[i] & 0xFF) + " ";
            if (hexString.length() == 2) {
                hexString = '0' + hexString + " ";
            }
            results.append(hexString.toUpperCase());
        }
        return results;
    }
}
