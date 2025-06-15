package com.example.qrcodedecode;

import android.os.AsyncTask;
import android.util.Log;
import java.io.IOException;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class NetworkUtil {
    public interface NetworkCallback {
        void onSuccess();
        void onFailure(String error);
    }

    public static void sendData(String serverUrl, String data, NetworkCallback callback) {
        new AsyncTask<String, Void, Boolean>() {
            @Override
            protected Boolean doInBackground(String... params) {
                OkHttpClient client = new OkHttpClient();
                String url = params[0] + "?data=" + params[1];
                Request request = new Request.Builder().url(url).build();
                
                try (Response response = client.newCall(request).execute()) {
                    return response.isSuccessful();
                } catch (IOException e) {
                    Log.e("NetworkUtil", "Error: " + e.getMessage());
                    return false;
                }
            }

            @Override
            protected void onPostExecute(Boolean success) {
                if (success) {
                    callback.onSuccess();
                } else {
                    callback.onFailure("Network error");
                }
            }
        }.execute(serverUrl, data);
    }
}