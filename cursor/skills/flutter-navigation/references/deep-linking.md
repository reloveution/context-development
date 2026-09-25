# Deep Linking Setup

## Android

**`AndroidManifest.xml` — App Links (recommended):**
```xml
<activity android:name=".MainActivity">
  <intent-filter android:autoVerify="true">
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="https" android:host="yourapp.com" />
  </intent-filter>
</activity>
```

**Custom scheme:**
```xml
<intent-filter>
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="myapp" />
</intent-filter>
```

**Verify App Links** — host `https://yourapp.com/.well-known/assetlinks.json`:
```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.example.yourapp",
    "sha256_cert_fingerprints": ["YOUR_SHA256_FINGERPRINT"]
  }
}]
```

**Test:** `adb shell am start -W -a android.intent.action.VIEW -d "https://yourapp.com/path"`

## iOS

**Universal Links (recommended)** — add to Runner.entitlements or Xcode:
```xml
<key>com.apple.developer.associated-domains</key>
<array>
  <string>applinks:yourapp.com</string>
</array>
```

**Custom scheme** — `ios/Runner/Info.plist`:
```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLName</key>
    <string>com.example.yourapp</string>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>myapp</string>
    </array>
  </dict>
</array>
```

**Verify Universal Links** — host `https://yourapp.com/.well-known/apple-app-site-association`:
```json
{
  "applinks": {
    "apps": [],
    "details": [{
      "appIDs": ["TEAMID.com.example.yourapp"],
      "components": [{ "/": "/path/to/*" }]
    }]
  }
}
```

**Test:** `xcrun simctl openurl booted "https://yourapp.com/path"`

## go_router Config

```dart
final router = GoRouter(routes: [
  GoRoute(path: '/', builder: (context, state) => HomeScreen()),
  GoRoute(path: '/details/:id', builder: (context, state) {
    return DetailsScreen(id: state.pathParameters['id']!);
  }),
]);
```

go_router handles deep links automatically when platform is configured.

## Troubleshooting

- **Link not opening app:** check intent filters / Info.plist, verify scheme match
- **Web 404:** configure SPA rewrite (see web-navigation.md) or use hash strategy
- **Route not found:** check GoRouter path matches link, watch trailing slashes
- **Security:** prefer App Links / Universal Links over custom schemes, validate link data
