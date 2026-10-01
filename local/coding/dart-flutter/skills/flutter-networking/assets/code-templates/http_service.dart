import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

class ApiService {
  final http.Client _client;
  final String _baseUrl;
  final String? _authToken;

  ApiService({required String baseUrl, String? authToken, http.Client? client})
    : _baseUrl = baseUrl,
      _authToken = authToken,
      _client = client ?? http.Client();

  Map<String, String> get _headers {
    final headers = <String, String>{'Content-Type': 'application/json'};

    if (_authToken != null) {
      headers['Authorization'] = 'Bearer $_authToken';
    }

    return headers;
  }

  Future<T> _get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
  }) async {
    final uri = Uri.parse(
      '$_baseUrl$path',
    ).replace(queryParameters: queryParameters);

    final response = await _client.get(uri, headers: _headers);
    return _handleResponse<T>(response);
  }

  Future<T> _post<T>(String path, {Map<String, dynamic>? body}) async {
    final uri = Uri.parse('$_baseUrl$path');

    final response = await _client.post(
      uri,
      headers: _headers,
      body: body != null ? jsonEncode(body) : null,
    );
    return _handleResponse<T>(response);
  }

  Future<T> _put<T>(String path, {Map<String, dynamic>? body}) async {
    final uri = Uri.parse('$_baseUrl$path');

    final response = await _client.put(
      uri,
      headers: _headers,
      body: body != null ? jsonEncode(body) : null,
    );
    return _handleResponse<T>(response);
  }

  Future<T> _delete<T>(String path) async {
    final uri = Uri.parse('$_baseUrl$path');

    final response = await _client.delete(uri, headers: _headers);
    return _handleResponse<T>(response);
  }

  T _handleResponse<T>(http.Response response) {
    switch (response.statusCode) {
      case 200:
      case 201:
      case 204:
        if (response.body.isEmpty) {
          return null as T;
        }
        return jsonDecode(response.body) as T;

      case 400:
        throw BadRequestException('Invalid request');

      case 401:
        throw UnauthorizedException('Not authenticated');

      case 403:
        throw ForbiddenException('Access denied');

      case 404:
        throw NotFoundException('Resource not found');

      case 429:
        throw TooManyRequestsException('Rate limit exceeded');

      case 500:
      case 502:
      case 503:
        throw ServerException('Server error');

      default:
        throw HttpException(
          'HTTP ${response.statusCode}: ${response.reasonPhrase}',
        );
    }
  }

  void dispose() {
    _client.close();
  }
}

class BadRequestException implements Exception {
  final String message;
  BadRequestException(this.message);
}

class UnauthorizedException implements Exception {
  final String message;
  UnauthorizedException(this.message);
}

class ForbiddenException implements Exception {
  final String message;
  ForbiddenException(this.message);
}

class NotFoundException implements Exception {
  final String message;
  NotFoundException(this.message);
}

class TooManyRequestsException implements Exception {
  final String message;
  TooManyRequestsException(this.message);
}

class ServerException implements Exception {
  final String message;
  ServerException(this.message);
}

class HttpException implements Exception {
  final String message;
  HttpException(this.message);
}
