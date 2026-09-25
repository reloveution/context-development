---
name: flutter-drift
description: Guide for drift database in Flutter. Use when building apps with local SQLite storage — type-safe queries, reactive streams, migrations, CRUD. Includes drift_flutter setup, StreamBuilder integration, and cross-platform support.
---

# Flutter Drift

## Setup

### Dependencies

```yaml
dependencies:
  drift: ^2.30.0
  drift_flutter: ^0.2.8
  path_provider: ^2.1.5

dev_dependencies:
  drift_dev: ^2.30.0
  build_runner: ^2.10.4
```

### Database Class

```dart
import 'package:drift/drift.dart';
import 'package:drift_flutter/drift_flutter.dart';

part 'database.g.dart';

class TodoItems extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get title => text()();
  DateTimeColumn get createdAt => dateTime().nullable()();
}

@DriftDatabase(tables: [TodoItems])
class AppDatabase extends _$AppDatabase {
  AppDatabase([QueryExecutor? e])
      : super(
          e ??
              driftDatabase(
                name: 'app_db',
                native: const DriftNativeOptions(
                  databaseDirectory: getApplicationSupportDirectory,
                ),
                web: DriftWebOptions(
                  sqlite3Wasm: Uri.parse('sqlite3.wasm'),
                  driftWorker: Uri.parse('drift_worker.js'),
                ),
              ),
        );

  @override
  int get schemaVersion => 1;
}
```

Generate: `dart run build_runner build` (or `watch` during dev).

### Web

Place `sqlite3.wasm` and `drift_worker.js` in `web/` folder.

### Isolate Sharing

```dart
AppDatabase.defaults(): super(
  driftDatabase(
    name: 'app_db',
    native: DriftNativeOptions(shareAcrossIsolates: true),
  ),
);
```

### Testing

```dart
AppDatabase createTestDatabase() => AppDatabase(NativeDatabase.memory());
```

## Tables

### Column Types

| Dart Type | Drift Column | SQL Type |
|-----------|-------------|----------|
| `int` | `integer()` | `INTEGER` |
| `BigInt` | `int64()` | `INTEGER` |
| `String` | `text()` | `TEXT` |
| `bool` | `boolean()` | `INTEGER` (0/1) |
| `double` | `real()` | `REAL` |
| `Uint8List` | `blob()` | `BLOB` |
| `DateTime` | `dateTime()` | `INTEGER` or `TEXT` |

### Column Modifiers

```dart
integer().nullable()()                           // nullable
dateTime().withDefault(currentDateAndTime)()      // SQL default
boolean().clientDefault(() => true)()             // Dart default
boolean().named('admin')()                        // custom column name
text().withLength(min: 1, max: 50)()              // length constraint
integer().check(age.isBiggerOrEqualValue(0))()    // check constraint
text().unique()()                                 // unique
integer().references(Artists, #id)()              // foreign key
```

### Primary Keys

```dart
// Auto increment (default)
IntColumn get id => integer().autoIncrement()();

// Custom primary key
@override
Set<Column<Object>> get primaryKey => {email};
```

### Unique Keys (Multi-Column)

```dart
@override
List<Set<Column>> get uniqueKeys => [{room, onDay}];
```

### Indexes

```dart
@TableIndex(name: 'user_name', columns: {#name})
class Users extends Table { ... }

// With ordering
@TableIndex(
  name: 'log_at',
  columns: {IndexedColumn(#loggedAt, orderBy: OrderingMode.desc)},
)

// Custom SQL
@TableIndex.sql('CREATE INDEX pending ON orders (creation_time) WHERE status == \'pending\';')
```

### Generated Columns

```dart
late final area = integer().generatedAs(length * width)();               // virtual
late final area = integer().generatedAs(length * width, stored: true)(); // stored
```

### Table Mixins

```dart
mixin TableMixin on Table {
  late final id = integer().autoIncrement()();
  late final createdAt = dateTime().withDefault(currentDateAndTime)();
}

class Posts extends Table with TableMixin {
  late final content = text()();
}
```

### Custom Table Name / Strict Tables

```dart
@override
String get tableName => 'product_table';

@override
bool get isStrict => true;
```

### Enable Foreign Keys

```dart
MigrationStrategy get migration => MigrationStrategy(
  beforeOpen: (details) async {
    await customStatement('PRAGMA foreign_keys = ON');
  },
);
```

## Queries

### Select

```dart
final all = await select(todoItems).get();
final stream = select(todoItems).watch();
```

### Where

```dart
final result = await (select(todoItems)
  ..where((t) => t.isCompleted.equals(true) & t.priority.isBiggerThanValue(3))
).get();
```

Operators: `equals`, `isBiggerThan`, `isSmallerThan`, `isBiggerOrEqualValue`, `isSmallerOrEqualValue`, `like`, `contains`, `isNull`, `isNotNull`

### Order By, Limit, Single Row

```dart
..orderBy([(t) => OrderingTerm(expression: t.createdAt, mode: OrderingMode.desc)])
..limit(20, offset: 40)

// Single row
.getSingle()        // throws if not found
.getSingleOrNull()  // returns null
.watchSingle()      // stream single row
.watchSingleOrNull()
```

### Map Results

```dart
final titles = await select(todoItems)
  .map((row) => row.title)
  .get();
```

### Joins

```dart
// Inner join
final results = await (select(todoItems)
  .join([innerJoin(categories, categories.id.equalsExp(todoItems.category))])
  .map((row) => (
    entry: row.readTable(todoItems),
    category: row.readTableOrNull(categories),
  ))
  .get();

// Left outer join
leftOuterJoin(categories, categories.id.equalsExp(todoItems.category))

// Self join
final other = alias(todoItems, 'other');
```

### Aggregations

```dart
// Count all
final count = await (selectOnly(todoItems)
  .addColumns([countAll()])
  .map((row) => row.read(countAll()))
  .getSingle();

// Group by
(select(categories).join([
  innerJoin(todoItems, todoItems.category.equalsExp(categories.id), useColumns: false),
])
  ..addColumns([todoItems.id.count()])
  ..groupBy([categories.id]))
```

### Subqueries

```dart
// In WHERE
..where((t) => t.createdAt.isBiggerThan(
  subqueryExpression(selectOnly(todoItems).addColumns([max(todoItems.createdAt)])),
))

// From subquery
final sub = Subquery(select(todoItems)..orderBy(...)..limit(10), 's');
final results = await select(sub).get();
```

### Custom Columns, Exists, Union

```dart
final isImportant = todoItems.content.like('%important%');
select(todoItems).addColumns([isImportant]).map((row) => row.read(isImportant)!);

existsQuery(select(todoItems))

query1.unionAll(query2).get()
```

## Writes

### Insert

```dart
final id = await into(todoItems).insert(
  TodoItemsCompanion.insert(title: 'First todo'),
);

// Bulk
await batch((b) {
  b.insertAll(todoItems, [
    TodoItemsCompanion.insert(title: 'First'),
    TodoItemsCompanion.insert(title: 'Second'),
  ]);
});

// Upsert (SQLite 3.24+)
await into(users).insertOnConflictUpdate(companion);

// Custom conflict target
await into(products).insert(companion, onConflict: DoUpdate(target: [sku]));

// Insert returning (SQLite 3.35+)
final row = await into(todos).insertReturning(companion);
```

### Update

```dart
// Partial update
await (update(todoItems)..where((t) => t.id.equals(1)))
  .write(TodoItemsCompanion(title: const Value('Updated')));

// Full replace
await update(todoItems).replace(TodoItem(id: 1, title: 'Updated', ...));

// SQL expression
await update(users).write(UsersCompanion.custom(name: users.name.lower()));
```

### Delete

```dart
await (delete(todoItems)..where((t) => t.id.equals(1))).go();
await delete(todoItems).go();  // WARNING: deletes ALL rows
```

### Companions vs Data Classes

- **Data class** (`TodoItem`) — full row, all fields required
- **Companion** (`TodoItemsCompanion`) — partial data for inserts/updates

```dart
Value('text')      // set to this value
Value(null)        // SET column = NULL
Value.absent()     // don't change this column
```

### Transactions

```dart
await transaction(() async {
  await into(todoItems).insert(...);
  await into(categories).insert(...);
});
// Automatically rolls back on exception
```

### Batch Operations

```dart
await batch((b) {
  b.insertAll(todoItems, [...]);
  b.update(todoItems, companion);
  b.delete(todoItems, id);
});
```

## Streams

All queries support `.watch()` / `.watchSingle()` / `.watchSingleOrNull()` for reactive updates.

### Limitations

1. External changes (outside drift APIs) don't trigger updates
2. Coarse updates — any table change triggers all watchers on that table
3. Keep stream queries efficient (use indexes, limit rows)

## Migrations

### Configure build.yaml

```yaml
targets:
  $default:
    builders:
      drift_dev:
        options:
          databases:
            my_database: lib/database.dart
          schema_dir: drift_schemas/
          test_dir: test/drift/
```

Generate: `dart run drift_dev make-migrations`

### Step-by-Step

```dart
@override
int get schemaVersion => 3;

@override
MigrationStrategy get migration => MigrationStrategy(
  onUpgrade: stepByStep(
    from1To2: (m, schema) async {
      await m.addColumn(schema.users, schema.users.birthDate);
    },
    from2To3: (m, schema) async {
      await m.create(schema.todosDelete);
      await m.alterTable(TableMigration(schema.todoItems));
    },
  ),
  beforeOpen: (details) async {
    await customStatement('PRAGMA foreign_keys = ON');
    if (details.wasCreated) {
      // Seed default data
    }
  },
);
```

### Migration Operations

```dart
m.addColumn(schema.users, schema.users.birthDate)
m.dropColumn(schema.users, schema.users.oldField)
m.renameColumn(schema.users, schema.users.name, schema.users.fullName)
m.createTable(schema.categories)
m.deleteTable('users')
m.alterTable(TableMigration(schema.todoItems))
m.create(schema.usersByNameIndex)     // create index
m.dropIndex('users_name_idx')
m.customStatement('UPDATE users SET status = ...')
```

### Manual Migrations (without make-migrations)

```dart
onUpgrade: (Migrator m, int from, int to) async {
  if (from == 1 && to == 2) {
    await m.addColumn(todoItems, todoItems.dueDate);
  }
}
```

### Test Migrations

```bash
dart test test/drift/schema_test.dart
dart run drift_dev schema validate
```

## Flutter UI Integration

Use StreamBuilder with `.watch()` for reactive UI. Handle loading/error/empty states.

Search with debounce:
```dart
stream: (select(db.todoItems)
  ..where((t) => t.title.contains(searchText))
).watch()
```

## Troubleshooting

```bash
dart run build_runner clean && dart run build_runner build --delete-conflicting-outputs
dart run drift_dev schema validate
```

Stream not updating — ensure operations go through drift APIs, not raw SQLite.
