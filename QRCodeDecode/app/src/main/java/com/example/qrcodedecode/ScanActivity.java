package com.example.qrcodedecode;

import android.os.Bundle;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.journeyapps.barcodescanner.BarcodeCallback;
import com.journeyapps.barcodescanner.BarcodeResult;
import com.journeyapps.barcodescanner.DecoratedBarcodeView;

public class ScanActivity extends AppCompatActivity {
    private DecoratedBarcodeView barcodeView;
    private String serverIp;
    private int serverPort;
    private long lastScanTime = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scan);

        serverIp = getIntent().getStringExtra("SERVER_IP");
        serverPort = getIntent().getIntExtra("SERVER_PORT", 5000);
        barcodeView = findViewById(R.id.barcode_scanner);

        barcodeView.decodeContinuous(new BarcodeCallback() {
            @Override
            public void barcodeResult(BarcodeResult result) {
                // 防抖动处理 (1秒内不重复扫描)
                if (System.currentTimeMillis() - lastScanTime < 1000) return;
                lastScanTime = System.currentTimeMillis();
                
                String qrContent = result.getText();
                String serverUrl = "http://" + serverIp + ":" + serverPort;
                
                NetworkUtil.sendData(serverUrl, qrContent, new NetworkUtil.NetworkCallback() {
                    @Override
                    public void onSuccess() {
                        runOnUiThread(() -> Toast.makeText(
                            ScanActivity.this, 
                            "发送成功: " + qrContent, 
                            Toast.LENGTH_SHORT).show());
                    }

                    @Override
                    public void onFailure(String error) {
                        runOnUiThread(() -> Toast.makeText(
                            ScanActivity.this, 
                            "发送失败: " + error, 
                            Toast.LENGTH_SHORT).show());
                    }
                });
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        barcodeView.resume();
    }

    @Override
    protected void onPause() {
        super.onPause();
        barcodeView.pause();
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        finish();
    }
}