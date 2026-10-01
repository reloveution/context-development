---
name: flutter-networking
description: Flutter networking — HTTP CRUD, WebSocket, authentication, error handling, performance. Use when implementing HTTP requests, WebSocket connections, authenticated requests, background parsing, or REST API integration.
---

# Flutter Networking

## HTTP

### Dependencies

```yaml
dependencies:
  http: ^1.6.0
```

### CRUD Operations

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

// GET
final response = await http.get(Uri.parse('https://api.example.com/albums/1'));

// GET with query parameters
final response = await http.get(
  Uri.parse('https://api.example.com/albums')
      .replace(queryParameters: {'userId': '1', '_limit': '10'}),
);

// POST
final response = await http.post(
  Uri.parse('https://api.example.com/albums'),
  headers: {'Content-Type': 'application/json; charset=UTF-8'},
  body: jsonEncode({'title': title}),
);

// PUT
final response = await http.put(
  Uri.parse('https://api.example.com/albums/1'),
  headers: {'Content-Type': 'application/json; charset=UTF-8'},
  body: jsonEncode({'title': title}),
);

// DELETE
final response = await http.delete(
  Uri.parse('https://api.example.com/albums/1'),
  headers: {'Content-Type': 'application/json; charset=UTF-8'},
);
```

### Response Handling

```dart
if (response.statusCode == 200) {
  return Album.fromJson(jsonDecode(response.body));
} else {
  throw Exception('Failed: ${response.statusCode}');
}
```

### Model Pattern (Dart 3)

```dart
class Album {
  final int id;
  final String title;

  const Album({required this.id, required this.title});

  factory Album.fromJson(Map<String, dynamic> json) => switch (json) {
    {'id': int id, 'title': String title} => Album(id: id, title: title),
    _ => throw const FormatException('Failed to parse album'),
  };

  Map<String, dynamic> toJson() => {'id': id, 'title': title};
}
```

### Timeout

```dart
final response = await http.get(uri).timeout(
  const Duration(seconds: 10),
  onTimeout: () => throw TimeoutException('Request timeout'),
);
```

## WebSocket

### Dependencies

```yaml
dependencies:
  web_socket_channel: ^3.0.3
```

### Basic Usage

```dart
import 'package:web_socket_channel/web_socket_channel.dart';

final channel = WebSocketChannel.connect(Uri.parse('wss://example.com/ws'));

// Send
channel.sink.add(jsonEncode({'type': 'chat', 'message': 'Hello'}));

// Receive (StreamBuilder or listen)
channel.stream.listen(
  (data) { /* handle message */ },
  onError: (error) { /* handle error */ },
  onDone: () { /* connection closed */ },
  cancelOnError: false,
);

// Close in dispose()
channel.sink.close();
```

### Reconnection with Backoff

```dart
WebSocketChannel? _channel;
Timer? _reconnectTimer;
int _reconnectAttempts = 0;
static const int _maxReconnectAttempts = 5;

void _connect() {
  try {
    _channel = WebSocketChannel.connect(Uri.parse('wss://example.com/ws'));
    _channel!.stream.listen(
      (data) { _reconnectAttempts = 0; },
      onError: (_) => _scheduleReconnect(),
      onDone: () => _scheduleReconnect(),
    );
  } catch (_) {
    _scheduleReconnect();
  }
}

void _scheduleReconnect() {
  if (_reconnectAttempts >= _maxReconnectAttempts) return;
  _reconnectAttempts++;
  _reconnectTimer?.cancel();
  _reconnectTimer = Timer(Duration(seconds: _reconnectAttempts * 2), _connect);
}
```

### WebSocket Auth

```dart
// Query parameter
final uri = Uri.parse('wss://example.com/ws').replace(
  queryParameters: {'token': token},
);

// Headers (IOWebSocketChannel)
import 'package:web_socket_channel/io.dart';
final channel = IOWebSocketChannel.connect(
  'wss://example.com/ws',
  headers: {'Authorization': 'Bearer $token'},
);
```

## Authentication

### Auth Header Patterns

```dart
import 'dart:io';

// Bearer Token (JWT)
headers: {HttpHeaders.authorizationHeader: 'Bearer $token'}

// Basic Auth
String basicAuth(String user, String pass) =>
    'Basic ${base64Encode(utf8.encode('$user:$pass'))}';

// API Key
headers: {'X-API-Key': apiKey}
```

### Token Storage (flutter_secure_storage)

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureTokenStorage {
  final _storage = const FlutterSecureStorage();

  Future<void> saveToken(String token) async =>
      await _storage.write(key: 'auth_token', value: token);

  Future<String?> getToken() async =>
      await _storage.read(key: 'auth_token');

  Future<void> clearToken() async =>
      await _storage.delete(key: 'auth_token');
}
```

### Interceptor Pattern (BaseClient)

```dart
class AuthenticatedClient extends http.BaseClient {
  final http.Client _inner;
  final AuthManager _authManager;

  AuthenticatedClient(this._inner, this._authManager);

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final token = await _authManager.getAccessToken();
    request.headers['Authorization'] = 'Bearer $token';

    final response = await _inner.send(request);

    if (response.statusCode == 401) {
      await _authManager.refreshAccessToken();
      final newToken = await _authManager.getAccessToken();
      request.headers['Authorization'] = 'Bearer $newToken';
      return await _inner.send(request);
    }

    return response;
  }
}
```

### Token Refresh

```dart
class AuthManager {
  final SecureTokenStorage _tokenStorage;
  final http.Client _client;
  String? _accessToken;
  String? _refreshToken;

  Future<String> getAccessToken() async {
    if (_accessToken != null && !_isTokenExpired(_accessToken!)) {
      return _accessToken!;
    }
    return await _refreshAccessToken();
  }

  Future<String> _refreshAccessToken() async {
    final response = await _client.post(
      Uri.parse('https://api.example.com/auth/refresh'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'refreshToken': _refreshToken}),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      _accessToken = data['accessToken'] as String;
      _refreshToken = data['refreshToken'] as String;
      await _tokenStorage.saveToken(_accessToken!);
      return _accessToken!;
    }
    throw Exception('Failed to refresh token');
  }
}
```

## Error Handling

### Status Code Mapping

```dart
switch (response.statusCode) {
  case 200 || 201 || 204:
    return Data.fromJson(jsonDecode(response.body));
  case 400: throw BadRequestException('Invalid request');
  case 401: throw UnauthorizedException('Not authenticated');
  case 403: throw ForbiddenException('Access denied');
  case 404: throw NotFoundException('Not found');
  case 429: throw TooManyRequestsException('Rate limit exceeded');
  case >= 500: throw ServerException('Server error');
  default: throw HttpException('HTTP ${response.statusCode}');
}
```

### Custom Exception Hierarchy

```dart
abstract class ApiException implements Exception {
  final String message;
  final int? statusCode;
  ApiException(this.message, [this.statusCode]);
  @override
  String toString() => message;
}

class BadRequestException extends ApiException {
  BadRequestException(super.message) : super(400);
}
class UnauthorizedException extends ApiException {
  UnauthorizedException(super.message) : super(401);
}
class ForbiddenException extends ApiException {
  ForbiddenException(super.message) : super(403);
}
class NotFoundException extends ApiException {
  NotFoundException(super.message) : super(404);
}
class TooManyRequestsException extends ApiException {
  TooManyRequestsException(super.message) : super(429);
}
class ServerException extends ApiException {
  ServerException(super.message) : super(500);
}
class NetworkException extends ApiException {
  NetworkException(super.message);
}
```

### Connection Error Handling

```dart
try {
  return await future;
} on SocketException catch (e) {
  throw NetworkException('No internet: ${e.message}');
} on HttpException catch (e) {
  throw NetworkException('HTTP error: ${e.message}');
} on FormatException catch (e) {
  throw NetworkException('Invalid format: ${e.message}');
}
```

### Retry with Exponential Backoff

```dart
Future<T> fetchWithRetry<T>(
  Future<T> Function() fetch, {
  int maxRetries = 3,
  Duration initialDelay = const Duration(seconds: 1),
}) async {
  for (int i = 0; i < maxRetries; i++) {
    try {
      return await fetch();
    } catch (e) {
      if (i == maxRetries - 1) rethrow;
      if (e is! NetworkException && e is! ServerException && e is! TooManyRequestsException) rethrow;
      await Future.delayed(initialDelay * (i + 1));
    }
  }
  throw StateError('Unreachable');
}
```

## Performance

### Background Parsing (Isolates)

For large JSON responses (>10KB), parse in background isolate:

```dart
import 'package:flutter/foundation.dart';

Future<List<Photo>> fetchPhotos(http.Client client) async {
  final response = await client.get(Uri.parse('https://api.example.com/photos'));
  if (response.statusCode == 200) {
    return compute(parsePhotos, response.body);
  }
  throw Exception('Failed to load');
}

List<Photo> parsePhotos(String body) =>
    (jsonDecode(body) as List).cast<Map<String, dynamic>>()
        .map((json) => Photo.fromJson(json)).toList();
```

### In-Memory Cache with TTL

```dart
class CacheService<T> {
  final Map<String, ({T value, DateTime expiry})> _cache = {};
  final Duration defaultTtl;

  CacheService({this.defaultTtl = const Duration(minutes: 5)});

  T? get(String key) {
    final entry = _cache[key];
    if (entry == null || DateTime.now().isAfter(entry.expiry)) {
      _cache.remove(key);
      return null;
    }
    return entry.value;
  }

  void set(String key, T value, {Duration? ttl}) {
    _cache[key] = (value: value, expiry: DateTime.now().add(ttl ?? defaultTtl));
  }
}
```

### Request Deduplication

```dart
class RequestDeduplicator<T> {
  final Map<String, Future<T>> _pending = {};

  Future<T> fetch(String key, Future<T> Function() fetchFn) async {
    if (_pending.containsKey(key)) return await _pending[key]!;
    final future = fetchFn();
    _pending[key] = future;
    try { return await future; } finally { _pending.remove(key); }
  }
}
```

### Pagination

```dart
// Offset-based
final response = await http.get(
  uri.replace(queryParameters: {'offset': '$offset', 'limit': '$limit'}),
);

// Cursor-based
class PageResult<T> {
  final List<T> items;
  final String? nextCursor;
  PageResult({required this.items, required this.nextCursor});
}
```

### Connection Pooling

Reuse a single `http.Client` instance app-wide — inject via DI. Close on app dispose.

### Request Batching

```dart
final results = await Future.wait(ids.map((id) => fetchItem(id)));
```

Prefer one bulk endpoint over `Future.wait` of single-id calls (parallel ≠ not-N+1 from server view). Preserve auth/tenancy/soft-delete/ordering — bulk applies the same filters per-item.

`Future.wait` reports only the **first** error: default `eagerError: false` waits for all then propagates first; `eagerError: true` fires immediately. Remaining errors drop to the Zone in both modes. For partial-success, wrap each future in `.catchError(...)` (or `Result<T>`) **before** passing to `Future.wait`.

Chunk ids and await between chunks for rate limits. See `dart-data-patterns`.

### Optimistic Updates

Update cache immediately, rollback on error:

```dart
Future<Album> updateAlbum(int id, String title) async {
  final cached = _cache.get('album-$id');
  _cache.set('album-$id', cached!.copyWith(title: title));
  try {
    final result = await _updateOnServer(id, title);
    _cache.set('album-$id', result);
    return result;
  } catch (e) {
    _cache.set('album-$id', cached); // rollback
    rethrow;
  }
}
```
