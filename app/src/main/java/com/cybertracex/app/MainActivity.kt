package com.cybertracex.app

import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.FileProvider
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : ComponentActivity() {
    private val isDownloading = mutableStateOf(false)
    private val downloadProgress = mutableFloatStateOf(0f)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            Scaffold(
                modifier = Modifier.fillMaxSize(),
                containerColor = Color(0xFF04070a)
            ) { innerPadding ->
                Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {
                    WebViewScreen(
                        modifier = Modifier.fillMaxSize(),
                        onUpdateRequested = { url ->
                            startDownload(url)
                        }
                    )
                    
                    if (isDownloading.value) {
                        UpdateProgressOverlay(progress = downloadProgress.value)
                    }
                }
            }
        }
    }

    private fun startDownload(urlString: String) {
        isDownloading.value = true
        downloadProgress.value = 0f
        
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // If it's github releases page, downloading it directly will download the html page.
                // We assume urlString points directly to .apk, or we follow redirects.
                val url = URL(urlString)
                var connection = url.openConnection() as HttpURLConnection
                connection.instanceFollowRedirects = true
                connection.connect()

                // handle redirect if any
                if (connection.responseCode in 300..399) {
                    val redirectUrl = connection.getHeaderField("Location")
                    connection = URL(redirectUrl).openConnection() as HttpURLConnection
                    connection.connect()
                }

                val fileLength = connection.contentLength
                val apkFile = File(cacheDir, "update.apk")
                if (apkFile.exists()) {
                    apkFile.delete()
                }
                
                val input = connection.inputStream
                val output = FileOutputStream(apkFile)
                
                val data = ByteArray(4096)
                var total: Long = 0
                var count: Int
                
                while (input.read(data).also { count = it } != -1) {
                    total += count
                    if (fileLength > 0) {
                        downloadProgress.value = total.toFloat() / fileLength
                    }
                    output.write(data, 0, count)
                }
                output.flush()
                output.close()
                input.close()
                
                withContext(Dispatchers.Main) {
                    isDownloading.value = false
                    installApk(apkFile)
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    isDownloading.value = false
                    Toast.makeText(this@MainActivity, "Download failed: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }
        }
    }

    private fun installApk(apkFile: File) {
        try {
            val intent = Intent(Intent.ACTION_VIEW)
            val uri = FileProvider.getUriForFile(this, "${packageName}.fileprovider", apkFile)
            intent.setDataAndType(uri, "application/vnd.android.package-archive")
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_GRANT_READ_URI_PERMISSION
            startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(this, "Failed to install: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }
}

class AndroidUpdater(private val onUpdateRequested: (String) -> Unit) {
    @JavascriptInterface
    fun startUpdate(url: String) {
        onUpdateRequested(url)
    }
}

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun WebViewScreen(modifier: Modifier = Modifier, onUpdateRequested: (String) -> Unit) {
    AndroidView(
        modifier = modifier.fillMaxSize(),
        factory = { context ->
            WebView(context).apply {
                settings.javaScriptEnabled = true
                settings.domStorageEnabled = true
                settings.mediaPlaybackRequiresUserGesture = false
                settings.allowFileAccess = true
                settings.allowContentAccess = true
                settings.allowFileAccessFromFileURLs = true
                settings.allowUniversalAccessFromFileURLs = true
                setBackgroundColor(android.graphics.Color.TRANSPARENT)
                webViewClient = WebViewClient()
                webChromeClient = WebChromeClient()
                
                addJavascriptInterface(AndroidUpdater(onUpdateRequested), "AndroidUpdater")
                
                loadUrl("file:///android_asset/index.html")
            }
        },
        update = {}
    )
}

@Composable
fun UpdateProgressOverlay(progress: Float) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xCC04070A)),
        contentAlignment = Alignment.Center
    ) {
        Card(
            colors = CardDefaults.cardColors(containerColor = Color(0xFF070d10)),
            modifier = Modifier.padding(32.dp)
        ) {
            Column(
                modifier = Modifier.padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    text = "DOWNLOADING UPDATE...",
                    color = Color(0xFF22FF9C),
                    style = MaterialTheme.typography.titleMedium
                )
                Spacer(modifier = Modifier.height(16.dp))
                LinearProgressIndicator(
                    progress = { progress },
                    modifier = Modifier.fillMaxWidth(),
                    color = Color(0xFF38E8FF),
                    trackColor = Color(0xFF38E8FF).copy(alpha = 0.2f),
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "${(progress * 100).toInt()}%",
                    color = Color.White,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}
