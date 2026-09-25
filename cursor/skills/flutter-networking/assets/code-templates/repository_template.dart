import 'dart:async';

abstract class Repository<T> {
  Future<T?> get(String id);
  Future<List<T>> getAll();
  Future<T> create(T entity);
  Future<T> update(T entity);
  Future<void> delete(String id);
}

class CacheRepository<T> implements Repository<T> {
  final Map<String, T> _cache = {};
  final Duration _cacheTtl;

  final Map<String, DateTime> _cacheExpiry = {};

  CacheRepository({Duration cacheTtl = const Duration(minutes: 5)})
    : _cacheTtl = cacheTtl;

  @override
  Future<T?> get(String id) async {
    if (!_cache.containsKey(id)) {
      return null;
    }

    if (DateTime.now().isAfter(_cacheExpiry[id]!)) {
      _cache.remove(id);
      _cacheExpiry.remove(id);
      return null;
    }

    return _cache[id];
  }

  @override
  Future<List<T>> getAll() async {
    return _cache.values.toList();
  }

  @override
  Future<T> create(T entity) async {
    final id = _getId(entity);
    _cache[id] = entity;
    _cacheExpiry[id] = DateTime.now().add(_cacheTtl);
    return entity;
  }

  @override
  Future<T> update(T entity) async {
    final id = _getId(entity);
    _cache[id] = entity;
    _cacheExpiry[id] = DateTime.now().add(_cacheTtl);
    return entity;
  }

  @override
  Future<void> delete(String id) async {
    _cache.remove(id);
    _cacheExpiry.remove(id);
  }

  String _getId(T entity) {
    if (entity is Identifiable) {
      return (entity as Identifiable).id;
    }
    throw ArgumentError('Entity must implement Identifiable');
  }

  void clearCache() {
    _cache.clear();
    _cacheExpiry.clear();
  }
}

abstract class Identifiable {
  String get id;
}

class NetworkRepository<T> implements Repository<T> {
  final Future<T?> Function(String id) _fetchFn;
  final Future<List<T>> Function() _fetchAllFn;
  final Future<T> Function(T entity) _createFn;
  final Future<T> Function(T entity) _updateFn;
  final Future<void> Function(String id) _deleteFn;

  NetworkRepository({
    required Future<T?> Function(String id) fetchFn,
    required Future<List<T>> Function() fetchAllFn,
    required Future<T> Function(T entity) createFn,
    required Future<T> Function(T entity) updateFn,
    required Future<void> Function(String id) deleteFn,
  }) : _fetchFn = fetchFn,
       _fetchAllFn = fetchAllFn,
       _createFn = createFn,
       _updateFn = updateFn,
       _deleteFn = deleteFn;

  @override
  Future<T?> get(String id) async {
    return await _fetchFn(id);
  }

  @override
  Future<List<T>> getAll() async {
    return await _fetchAllFn();
  }

  @override
  Future<T> create(T entity) async {
    return await _createFn(entity);
  }

  @override
  Future<T> update(T entity) async {
    return await _updateFn(entity);
  }

  @override
  Future<void> delete(String id) async {
    return await _deleteFn(id);
  }
}

class HybridRepository<T> implements Repository<T> {
  final CacheRepository<T> _cacheRepo;
  final NetworkRepository<T> _networkRepo;

  HybridRepository({
    required Future<T?> Function(String id) fetchFn,
    required Future<List<T>> Function() fetchAllFn,
    required Future<T> Function(T entity) createFn,
    required Future<T> Function(T entity) updateFn,
    required Future<void> Function(String id) deleteFn,
    Duration cacheTtl = const Duration(minutes: 5),
  }) : _cacheRepo = CacheRepository(cacheTtl: cacheTtl),
       _networkRepo = NetworkRepository(
         fetchFn: fetchFn,
         fetchAllFn: fetchAllFn,
         createFn: createFn,
         updateFn: updateFn,
         deleteFn: deleteFn,
       );

  @override
  Future<T?> get(String id) async {
    final cached = await _cacheRepo.get(id);
    if (cached != null) {
      return cached;
    }

    final fetched = await _networkRepo.get(id);
    if (fetched != null) {
      await _cacheRepo.create(fetched);
    }
    return fetched;
  }

  @override
  Future<List<T>> getAll() async {
    final cached = await _cacheRepo.getAll();
    if (cached.isNotEmpty) {
      return cached;
    }

    final fetched = await _networkRepo.getAll();
    for (final entity in fetched) {
      await _cacheRepo.create(entity);
    }
    return fetched;
  }

  @override
  Future<T> create(T entity) async {
    final created = await _networkRepo.create(entity);
    await _cacheRepo.create(created);
    return created;
  }

  @override
  Future<T> update(T entity) async {
    final updated = await _networkRepo.update(entity);
    await _cacheRepo.update(updated);
    return updated;
  }

  @override
  Future<void> delete(String id) async {
    await _networkRepo.delete(id);
    await _cacheRepo.delete(id);
  }

  void clearCache() {
    _cacheRepo.clearCache();
  }
}
