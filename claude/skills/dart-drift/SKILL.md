---
name: dart-drift
description: Complete guide for using drift database library in Dart applications (CLI, server-side, non-Flutter). Use when building Dart apps that need local SQLite database storage or PostgreSQL connection with type-safe queries, reactive streams, migrations, and efficient CRUD operations.
---

# Dart Drift

Reactive persistence library for Dart built on SQLite, with optional PostgreSQL support. Type-safe queries, auto-updating streams, schema migrations.

## Setup

### SQLite

```yaml
dependencies:
  drift: ^2.30.0
  sqlite3: ^3.1.3
dev_dependencies:
  drift_dev: ^2.30.0
  build_runner: ^2.10.4
```

```dart
@DriftDatabase(tables: [TodoItems])
class AppDatabase extends _$AppDatabase {
  AppDatabase(QueryExecutor e) : super(e);
  @override
  int get schemaVersion => 1;
}

AppDatabase openConnection() {
  final file = File('db.sqlite');
  return AppDatabase(LazyDatabase(() async {
    final db = sqlite3.open(file.path);
    return NativeDatabase.createInBackground(db);
  }));
}
```

### PostgreSQL

```yaml
dependencies:
  drift: ^2.30.0
  postgres: ^3.5.9
  drift_postgres: ^1.3.1
dev_dependencies:
  drift_dev: ^2.30.0
  build_runner: ^2.10.4
```

Configure dialect in `build.yaml`:

```yaml
targets:
  $default:
    builders:
      drift_dev:
        options:
          sql:
            dialects:
              - postgres
```

```dart
AppDatabase openPostgresConnection() {
  final endpoint = HostEndpoint(
    host: 'localhost', port: 5432,
    database: 'mydb', username: 'user', password: 'password',
  );
  return AppDatabase(PgDatabase(endpoint: endpoint));
}

// Connection pool (use in production)
AppDatabase openPooledConnection() {
  final pool = PgPool(
    PgEndpoint(host: 'localhost', port: 5432, database: 'mydb',
      username: 'user', password: 'password'),
    settings: PoolSettings(maxSize: 10),
  );
  return AppDatabase(PgDatabase.opened(pool));
}

// Existing session
AppDatabase fromSession(Session session) =>
    AppDatabase(PgDatabase.opened(session));
```

Connection settings:

```dart
PgDatabase(
  endpoint: endpoint,
  settings: ConnectionSettings(
    connectTimeout: Duration(seconds: 10),
    queryTimeout: Duration(seconds: 30),
    applicationName: 'My Drift App',
  ),
)
```

### Code Generation

```bash
dart run build_runner build
dart run build_runner watch  # during development
```

### Testing

```dart
AppDatabase createTestDatabase() => AppDatabase(NativeDatabase.memory());

// PostgreSQL integration tests
AppDatabase createPostgresTestDatabase() => AppDatabase(
  PgDatabase(endpoint: HostEndpoint(
    host: 'localhost', port: 5432,
    database: 'test_db', username: 'test_user', password: 'test_pass',
  )),
);
```

## Tables

### Column Types

| Dart Type | Drift Column | SQL Type |
|-----------|-------------|----------|
| `int` | `integer()` | INTEGER |
| `BigInt` | `int64()` | INTEGER |
| `String` | `text()` | TEXT |
| `bool` | `boolean()` | INTEGER (1/0) |
| `double` | `real()` | REAL |
| `Uint8List` | `blob()` | BLOB |
| `DateTime` | `dateTime()` | INTEGER or TEXT |

### Column Modifiers

```dart
integer().nullable()()                          // allow NULL
dateTime().withDefault(currentDateAndTime)()     // server default (SQL)
boolean().clientDefault(() => true)()            // client default (Dart)
text().withLength(min: 1, max: 50)()             // length constraint
integer().check(age.isBiggerOrEqualValue(0))()   // check constraint
text().unique()()                                // unique constraint
text().named('admin')()                          // custom column name
integer().references(Artists, #id)()             // foreign key
```

### Primary Keys

```dart
// Auto-increment (default)
IntColumn get id => integer().autoIncrement()();

// Custom primary key
@override
Set<Column<Object>> get primaryKey => {email};
```

### Composite Unique

```dart
@override
List<Set<Column>> get uniqueKeys => [{room, onDay}];
```

### Indexes

```dart
@TableIndex(name: 'user_name', columns: {#name})
// With ordering:
@TableIndex(name: 'log_at', columns: {IndexedColumn(#loggedAt, orderBy: OrderingMode.desc)})
// Custom SQL:
@TableIndex.sql('CREATE INDEX pending ON orders (creation_time) WHERE status == \'pending\';')
```

### Generated Columns

```dart
late final area = integer().generatedAs(length * width)();              // virtual
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

### Custom Table Name

```dart
@override
String get tableName => 'product_table';
```

### Strict Tables

```dart
@override
bool get isStrict => true;
```

### Custom Table Constraints

```dart
@override
List<String> get customConstraints => [
  'FOREIGN KEY (foo, bar) REFERENCES group_memberships ("group", user)',
];
```

### Enable Foreign Keys (SQLite)

```dart
@override
MigrationStrategy get migration => MigrationStrategy(
  beforeOpen: (details) async {
    await customStatement('PRAGMA foreign_keys = ON');
  },
);
```

## Queries

### Where Operators

- `equals(value)`, `isBiggerThan(value)`, `isSmallerThan(value)`
- `isBiggerOrEqualValue(value)`, `isSmallerOrEqualValue(value)`
- `like(pattern)`, `contains(value)`
- `isNull()`, `isNotNull()`
- Combine: `&` (AND), `|` (OR)

```dart
final results = await (select(todoItems)
  ..where((t) => t.isCompleted.equals(true) & t.priority.isBiggerThanValue(3))
  ..orderBy([(t) => OrderingTerm(expression: t.createdAt, mode: OrderingMode.desc)])
  ..limit(20, offset: 40)
).get();
```

### Single Row

```dart
await (...).getSingle();        // exactly one, throws if none
await (...).getSingleOrNull();  // one or null
```

### Mapping

```dart
select(todoItems).map((row) => row.title).get();
```

### Joins

```dart
final results = await (select(todoItems)
  .join([
    innerJoin(categories, categories.id.equalsExp(todoItems.category)),
    leftOuterJoin(users, users.id.equalsExp(todoItems.userId)),
  ])
  .map((row) => (
    entry: row.readTable(todoItems),
    category: row.readTableOrNull(categories),
  ))
).get();

// Self join
final otherTodos = alias(todoItems, 'other');
```

### Aggregations

```dart
// Count
selectOnly(todoItems).addColumns([countAll()]).map((r) => r.read(countAll())).getSingle();

// Group by
select(categories)
  .join([innerJoin(todoItems, todoItems.category.equalsExp(categories.id), useColumns: false)])
  ..addColumns([todoItems.id.count()])
  ..groupBy([categories.id]);

// Average
selectOnly(todoItems).addColumns([todoItems.title.length.avg()]);
```

### Subqueries

```dart
// In WHERE
..where((t) => t.createdAt.isBiggerThan(
  subqueryExpression(selectOnly(todoItems).addColumns([max(todoItems.createdAt)])),
))

// From subquery
final sub = Subquery(select(todoItems)..orderBy(...)..limit(10), 's');
await select(sub).get();
```

### Custom Columns & Exists & Union

```dart
final isImportant = todoItems.content.like('%important%');
select(todoItems).addColumns([isImportant]).map((r) => r.read(isImportant)!);

existsQuery(select(todoItems));

query1.unionAll(query2).get();
```

## Write Operations

### Insert

```dart
final id = await into(todoItems).insert(
  TodoItemsCompanion.insert(title: 'First todo', content: 'Description'),
);

// Insert returning (SQLite 3.35+)
final row = await into(todos).insertReturning(TodosCompanion.insert(...));

// Upsert (SQLite 3.24+)
await into(users).insertOnConflictUpdate(UsersCompanion.insert(...));

// Custom conflict target
await into(products).insert(companion, onConflict: DoUpdate(target: [sku]));
```

### Update

```dart
await (update(todoItems)
  ..where((t) => t.id.equals(1))
).write(TodoItemsCompanion(title: const Value('Updated')));

// Replace entire row
await update(todoItems).replace(TodoItem(id: 1, title: 'Updated', content: 'New'));

// SQL expression update
await update(users).write(UsersCompanion.custom(name: users.name.lower()));
```

### Delete

```dart
await (delete(todoItems)..where((t) => t.id.equals(1))).go();
await delete(todoItems).go();  // WARNING: deletes ALL rows
```

### Companion vs Data Class

- **Data class** (`TodoItem`) — full row, all fields required
- **Companion** (`TodoItemsCompanion`) — partial data for inserts/updates

```dart
Value(value)       // set to this value
Value.absent()     // don't update this column
Value(null)        // SET column = NULL (different from absent!)
```

### Transactions

```dart
final result = await transaction(() async {
  final id = await into(todoItems).insert(...);
  await into(categories).insert(...);
  return id;  // auto-rollback on exception
});
```

### Batch Operations

```dart
await batch((batch) {
  batch.insertAll(todoItems, [companion1, companion2]);
  batch.update(todoItems, TodoItemsCompanion(id: 1, title: const Value('Updated')));
  batch.delete(todoItems, 2);
});
```

## Streams

```dart
select(todoItems).watch();              // all rows, auto-updates
(select(todoItems)..where(...)).watchSingle();     // single row
(select(todoItems)..where(...)).watchSingleOrNull();
```

### With Joins

```dart
select(todoItems).join([leftOuterJoin(...)]).map(...).watch();
```

### Transformations

```dart
select(todoItems).watch().map((todos) => todos.map((t) => t.title).toList());
```

### Cancellation

```dart
StreamSubscription? subscription;
subscription = select(todoItems).watch().listen((todos) { ... });
subscription?.cancel();
subscription = null;
```

### Manual Update Trigger

```dart
notifyTableUpdates(todoItems);
```

### Limitations

- External changes (outside drift API) don't trigger stream updates
- Streams update for any table change, not just relevant rows
- Keep stream queries efficient (limit rows, use indexes)

## Migrations

### Configuration

```yaml
# build.yaml
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

```bash
dart run drift_dev make-migrations
```

### Step-by-Step Migrations

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
      await into(categories).insert(CategoriesCompanion.insert(name: 'Work'));
    }
  },
);
```

### Migration Operations

| Operation | Code |
|-----------|------|
| Add column | `m.addColumn(schema.users, schema.users.birthDate)` |
| Drop column | `m.dropColumn(schema.users, schema.users.oldField)` |
| Rename column | `m.renameColumn(schema.users, schema.users.name, schema.users.fullName)` |
| Create table | `m.createTable(schema.categories)` |
| Drop table | `m.deleteTable('users')` |
| Alter table | `m.alterTable(TableMigration(schema.todoItems))` |
| Create index | `m.create(schema.usersByNameIndex)` |
| Drop index | `m.dropIndex('users_name_idx')` |
| Custom SQL | `m.customStatement('ALTER TABLE ...')` |

### Manual Migrations (without make-migrations)

```dart
onUpgrade: (Migrator m, int from, int to) async {
  if (from == 1 && to == 2) {
    await m.addColumn(todoItems, todoItems.dueDate);
  }
},
```

### Data Migration

```dart
from1To2: (m, schema) async {
  await m.addColumn(schema.users, schema.users.fullName);
  final users = await (select(users)).get();
  await batch((batch) {
    for (final user in users) {
      batch.update(users, UsersCompanion(
        id: Value(user.id),
        fullName: Value('${user.firstName} ${user.lastName}'),
      ));
    }
  });
}
```

### Testing Migrations

```bash
dart test test/drift/schema_test.dart
```

## PostgreSQL-Specific

### Types

```dart
late final id = postgresUuid().autoGenerate()();
late final config = postgresJson()();
late final metadata = postgresJsonb()();
late final tags = postgresArray(PostgresTypes.text)();
late final createdAt = dateTime().withDefault(FunctionCallExpression.currentTimestamp());
```

### Queries

```dart
// JSON
..where((u) => u.jsonData.containsString('key', 'value'))

// Array contains
..where((p) => p.tags.contains('tag1'))

// Full-text search
customSelect('SELECT * FROM posts WHERE to_tsvector(content) @@ plainto_tsquery(?)', ['term']).get();
```

### Indexes

```dart
// Simple
@TableIndex(name: 'users_email_idx', columns: {#email})

// JSON index
@TableIndex.sql('CREATE INDEX data_key_idx ON data ((config->>\'key\'))')

// GIN for arrays
@TableIndex.sql('CREATE INDEX posts_tags_gin ON posts USING GIN (tags)')
```

### PostgreSQL Migrations

```dart
from1To2: (m, schema) async {
  await m.customStatement('ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT NOW()');
}
```

External tools for complex migrations: pgmigrate, sqitch, Flyway.

## Common Patterns

### Soft Deletes

```dart
late final deletedAt = dateTime().nullable()();
// Query: ..where((t) => t.deletedAt.isNull())
```

### Updated At

```dart
late final updatedAt = dateTime().withDefault(FunctionCallExpression.currentTimestamp());
```

## Troubleshooting

```bash
# Build fails
dart run build_runner clean && dart run build_runner build --delete-conflicting-outputs

# Migration errors
dart run drift_dev schema validate
dart run drift_dev make-migrations
```

- **Connection pool exhausted**: increase `PoolSettings(maxSize: 20, maxLifetime: Duration(minutes: 5))`
- **PostgreSQL type errors**: verify dialect configured in `build.yaml`

## Best Practices

- Always use connection pools in production (PostgreSQL)
- Index frequently queried columns
- Use `watch()` over repeated `get()` for reactive UI
- Cancel stream subscriptions when not needed
- Use `stepByStep` for maintainable migrations
- Test migrations with generated test files
- Wrap data migrations in transactions
- Bump `schemaVersion` only on schema changes
- Set connection/query timeouts; enable SSL in production
- Use in-memory SQLite for unit tests, real Postgres for integration tests
