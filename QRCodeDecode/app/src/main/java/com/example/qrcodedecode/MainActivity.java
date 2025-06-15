package com.example.qrcodedecode;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        EditText etIp = findViewById(R.id.etIp);
        EditText etPort = findViewById(R.id.etPort);
        Button btnStartScan = findViewById(R.id.btnStartScan);

        btnStartScan.setOnClickListener(v -> {
            String ip = etIp.getText().toString().trim();
            String port = etPort.getText().toString().trim();
            
            if (ip.isEmpty() || port.isEmpty()) {
                return;
            }

            Intent intent = new Intent(MainActivity.this, ScanActivity.class);
            intent.putExtra("SERVER_IP", ip);
            intent.putExtra("SERVER_PORT", port);
            startActivity(intent);
        });
    }
}