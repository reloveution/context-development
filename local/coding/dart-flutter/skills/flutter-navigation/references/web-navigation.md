# Web Navigation

## Path URL Strategy Setup

```dart
import 'package:flutter_web_plugins/url_strategy.dart';

void main() {
  usePathUrlStrategy();
  runApp(MyApp());
}
```

Requires `flutter_web_plugins` SDK dependency in `pubspec.yaml`.

## SPA Server Rewrite Configs

Path strategy requires all routes to rewrite to `index.html`.

**Nginx:**
```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

**Apache (.htaccess):**
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

**Firebase:**
```json
{
  "hosting": {
    "public": "build/web",
    "rewrites": [{ "source": "**", "destination": "/index.html" }],
    "cleanUrls": true
  }
}
```

**Vercel:**
```json
{ "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }] }
```

**Netlify (_redirects):**
```
/* /index.html 200
```

## Non-Root Path Hosting

For `https://example.com/myapp/`:

1. Set `<base href="/myapp/">` in `web/index.html`
2. Configure GoRouter:
```dart
GoRouter(
  initialLocation: '/myapp/',
  routes: [
    GoRoute(path: '/myapp/', builder: (context, state) => HomeScreen()),
    GoRoute(path: '/myapp/details', builder: (context, state) => DetailsScreen()),
  ],
);
```
