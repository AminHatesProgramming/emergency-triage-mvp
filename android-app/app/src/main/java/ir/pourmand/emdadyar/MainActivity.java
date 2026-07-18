package ir.pourmand.emdadyar;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.MimeTypeMap;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.io.ByteArrayInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.Collections;

public final class MainActivity extends Activity {
    private static final String APP_HOST = "appassets.androidplatform.net";
    private static final String APP_PREFIX = "/assets/www/";
    private static final String START_URL = "https://" + APP_HOST + APP_PREFIX + "index.html";

    private WebView webView;

    @Override
    @SuppressLint("SetJavaScriptEnabled")
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.rgb(6, 78, 95));
        getWindow().setNavigationBarColor(Color.rgb(244, 247, 246));

        webView = new WebView(this);
        webView.setBackgroundColor(Color.rgb(244, 247, 246));
        webView.setOnApplyWindowInsetsListener((view, insets) -> {
            view.setPadding(
                    insets.getSystemWindowInsetLeft(),
                    insets.getSystemWindowInsetTop(),
                    insets.getSystemWindowInsetRight(),
                    0
            );
            return insets;
        });
        setContentView(webView);
        webView.requestApplyInsets();

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);
        settings.setSupportZoom(true);
        settings.setMediaPlaybackRequiresUserGesture(true);
        settings.setUserAgentString(settings.getUserAgentString() + " EmdadyarAndroid/1.0");

        boolean debuggable = (getApplicationInfo().flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0;
        WebView.setWebContentsDebuggingEnabled(debuggable);
        webView.setWebChromeClient(new WebChromeClient());
        webView.setWebViewClient(new LocalAppClient());

        if (savedInstanceState == null) {
            webView.loadUrl(START_URL);
        } else {
            webView.restoreState(savedInstanceState);
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        webView.saveState(outState);
        super.onSaveInstanceState(outState);
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.stopLoading();
            webView.destroy();
        }
        super.onDestroy();
    }

    private final class LocalAppClient extends WebViewClient {
        @Override
        public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
            Uri url = request.getUrl();
            if (!"https".equals(url.getScheme()) || !APP_HOST.equals(url.getHost())) {
                return null;
            }

            String path = Uri.decode(url.getPath());
            if (path == null || path.equals("/assets/www") || path.equals("/assets/www/")) {
                path = APP_PREFIX + "index.html";
            }
            if (!path.startsWith(APP_PREFIX) || path.contains("..")) {
                return errorResponse(403, "Forbidden");
            }

            String assetPath = path.substring("/assets/".length());
            try {
                InputStream stream = getAssets().open(assetPath);
                String mimeType = mimeType(assetPath);
                return new WebResourceResponse(mimeType, encodingFor(mimeType), stream);
            } catch (FileNotFoundException missing) {
                return errorResponse(404, "Not Found");
            } catch (IOException error) {
                return errorResponse(500, "Unable to read bundled asset");
            }
        }

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            Uri uri = request.getUrl();
            if ("https".equals(uri.getScheme()) && APP_HOST.equals(uri.getHost())) {
                return false;
            }
            String scheme = uri.getScheme();
            if ("tel".equals(scheme)) {
                openExternal(new Intent(Intent.ACTION_DIAL, uri));
                return true;
            }
            if ("mailto".equals(scheme) || "https".equals(scheme)) {
                openExternal(new Intent(Intent.ACTION_VIEW, uri));
                return true;
            }
            return true;
        }

    }

    private void openExternal(Intent intent) {
        try {
            startActivity(intent);
        } catch (ActivityNotFoundException ignored) {
            // The app remains open when no external handler is installed.
        }
    }

    private static WebResourceResponse errorResponse(int statusCode, String message) {
        InputStream body = new ByteArrayInputStream(message.getBytes(StandardCharsets.UTF_8));
        return new WebResourceResponse(
                "text/plain",
                "UTF-8",
                statusCode,
                message,
                Collections.emptyMap(),
                body
        );
    }

    private static String mimeType(String path) {
        String extension = MimeTypeMap.getFileExtensionFromUrl(path);
        String type = MimeTypeMap.getSingleton().getMimeTypeFromExtension(extension);
        if (type != null) {
            return type;
        }
        if (path.endsWith(".webmanifest")) {
            return "application/manifest+json";
        }
        if (path.endsWith(".json")) {
            return "application/json";
        }
        if (path.endsWith(".js")) {
            return "application/javascript";
        }
        return "application/octet-stream";
    }

    private static String encodingFor(String mimeType) {
        if (mimeType.startsWith("text/")
                || "application/json".equals(mimeType)
                || "application/javascript".equals(mimeType)
                || "application/manifest+json".equals(mimeType)) {
            return "UTF-8";
        }
        return null;
    }
}
