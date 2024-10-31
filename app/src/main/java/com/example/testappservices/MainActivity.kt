package com.example.testappservices

import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import androidx.activity.ComponentActivity
import android.content.Intent
import android.content.pm.PackageManager
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import android.Manifest
import android.annotation.SuppressLint
import android.graphics.BitmapFactory
import android.os.Build
import android.util.Log
import java.io.File


@Suppress("DEPRECATION")
class MainActivity : ComponentActivity() {

    private lateinit var imageView: ImageView
    private lateinit var startButton: Button
    private lateinit var stopButton: Button
    private lateinit var viewResult: Button

    private val STORAGE_PERMISSION_CODE = 100

    @SuppressLint("SdCardPath")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.layout)

        imageView = findViewById(R.id.image_view) // ImageView hiển thị hình ảnh
        startButton = findViewById(R.id.start_service) // Nút để bắt đầu phát hiện khuôn mặt
        stopButton = findViewById(R.id.stop_service)
        viewResult = findViewById(R.id.view_result)

        startButton.setOnClickListener {
            if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                // android >= 13
                if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_MEDIA_IMAGES)
                    != PackageManager.PERMISSION_GRANTED) {

                    ActivityCompat.requestPermissions(
                        this,
                        arrayOf(Manifest.permission.READ_MEDIA_IMAGES),
                        1001
                    )
                }else {
                    val serviceIntent = Intent(this, DetectionService::class.java)
                    startForegroundService(serviceIntent)
                }
            } else {
                // android < 13
                if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE)
                    != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(this,
                        arrayOf(Manifest.permission.READ_EXTERNAL_STORAGE),
                        STORAGE_PERMISSION_CODE)
                } else {
                    val serviceIntent = Intent(this, DetectionService::class.java)
                    startForegroundService(serviceIntent)
                }
            }
        }

        stopButton.setOnClickListener {
            Log.d("Activity", "Service is being destroyed")
            val serviceIntent = Intent(this, DetectionService::class.java)
            stopService(serviceIntent)
            finishAffinity()
            android.os.Process.killProcess(android.os.Process.myPid())
        }

        viewResult.setOnClickListener {
            val resultFile = File("/sdcard/Pictures/detected_Image.png")
            if(resultFile.exists()) {
                val bitmapResult = BitmapFactory.decodeFile(resultFile.absolutePath)
                imageView.setImageBitmap(bitmapResult)
            }
        }
    }

    @Deprecated("This method has been deprecated in favor of using the Activity Result API\n      which brings increased type safety via an {@link ActivityResultContract} and the prebuilt\n      contracts for common intents available in\n      {@link androidx.activity.result.contract.ActivityResultContracts}, provides hooks for\n      testing, and allow receiving results in separate, testable classes independent from your\n      activity. Use\n      {@link #registerForActivityResult(ActivityResultContract, ActivityResultCallback)} passing\n      in a {@link RequestMultiplePermissions} object for the {@link ActivityResultContract} and\n      handling the result in the {@link ActivityResultCallback#onActivityResult(Object) callback}.")
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == STORAGE_PERMISSION_CODE) {
            // Kiểm tra xem quyền có được cấp hay không
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                val serviceIntent = Intent(this, DetectionService::class.java)
                startForegroundService(serviceIntent)
            }
        } else if(requestCode == 1001) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                val serviceIntent = Intent(this, DetectionService::class.java)
                startForegroundService(serviceIntent)
            }
        }
    }
}
