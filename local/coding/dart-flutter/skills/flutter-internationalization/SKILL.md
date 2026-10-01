---
name: flutter-internationalization
description: Guide for internationalizing Flutter apps using gen-l10n and intl packages. Use when adding localization, translating UI text, formatting numbers/dates for locales, or configuring multi-language support.
---

# Flutter Internationalization

## Setup gen-l10n

### 1. Dependencies

```yaml
dependencies:
  flutter_localizations:
    sdk: flutter
  intl: any
```

### 2. Enable in pubspec.yaml

```yaml
flutter:
  generate: true
```

### 3. l10n.yaml

```yaml
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
```

### 4. Create ARB Files

Template `lib/l10n/app_en.arb`:
```json
{
  "helloWorld": "Hello World!",
  "@helloWorld": { "description": "Greeting message" }
}
```

Translation `lib/l10n/app_es.arb`:
```json
{ "helloWorld": "¡Hola Mundo!" }
```

### 5. Generate & Configure

```bash
flutter gen-l10n
```

```dart
import 'package:flutter_localizations/flutter_localizations.dart';
import 'l10n/app_localizations.dart';

MaterialApp(
  localizationsDelegates: [
    AppLocalizations.delegate,
    GlobalMaterialLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
  ],
  supportedLocales: [Locale('en'), Locale('es')],
)
```

### 6. Use

```dart
Text(AppLocalizations.of(context)!.helloWorld)
```

## ARB Message Types

### Placeholders

```json
{
  "greeting": "Hello {userName}!",
  "@greeting": {
    "description": "Personalized greeting",
    "placeholders": {
      "userName": { "type": "String", "example": "Alice" }
    }
  }
}
```

### Plurals

```json
{
  "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
  "@itemCount": {
    "placeholders": { "count": { "type": "int" } }
  }
}
```

Plural forms: `=0`, `=1`, `=2`, `zero`, `one`, `two`, `few`, `many`, `other`

### Selects

```json
{
  "pronoun": "{gender, select, male{he} female{she} other{they}}",
  "@pronoun": {
    "placeholders": { "gender": { "type": "String" } }
  }
}
```

## Number Formats

Placeholder types: `int`, `double`, `num`

| Format | Example (en_US) | Description |
|--------|----------------|-------------|
| `compact` | 1.2M | Short form |
| `compactCurrency` | $1.2M | Short + currency |
| `compactSimpleCurrency` | $1.2M | Short + locale currency |
| `compactLong` | 1.2 million | Long form |
| `currency` | USD1,200,000.00 | Full currency code |
| `simpleCurrency` | $1,200,000 | Locale currency symbol |
| `decimalPattern` | 1,200,000 | Grouped digits |
| `decimalPercentPattern` | 120% | Decimal as percent |
| `percentPattern` | 120% | Percent |
| `scientificPattern` | 1E6 | Scientific notation |

### Currency with optionalParameters

```json
{
  "price": "Price: {value}",
  "@price": {
    "placeholders": {
      "value": {
        "type": "double",
        "format": "compactCurrency",
        "optionalParameters": { "decimalDigits": 2, "symbol": "€" }
      }
    }
  }
}
```

## Date Formats

Placeholder type: `DateTime`

| Format | Example (en_US) | Description |
|--------|----------------|-------------|
| `y` | 2024 | Year |
| `yMd` | 1/15/2024 | Short date |
| `yMMMd` | Jan 15, 2024 | Month abbr |
| `yMMMMd` | January 15, 2024 | Full month |
| `yMMMMEEEEd` | Monday, January 15, 2024 | Full with day name |
| `MMMMd` | January 15 | Month + day |
| `Hm` | 14:30 | 24h time |
| `Hms` | 14:30:45 | 24h + seconds |
| `j` | 2:30 PM | Locale-aware time |
| `jm` | 2:30 PM | Locale-aware h:m |

### Date ARB Example

```json
{
  "eventDate": "Event on {date}",
  "@eventDate": {
    "placeholders": {
      "date": { "type": "DateTime", "format": "yMMMd" }
    }
  }
}
```

## l10n.yaml Options

### Output

| Option | Description | Default |
|--------|-------------|---------|
| `output-dir` | Directory for generated files | (synthetic package) |
| `output-class` | Generated class name | `AppLocalizations` |
| `header` | String header for generated files | — |
| `header-file` | File with header text | — |
| `synthetic-package` | Generate as synthetic package | `true` |

### Code Generation

| Option | Description | Default |
|--------|-------------|---------|
| `nullable-getter` | Nullable localizations getter | `true` |
| `use-named-parameters` | Named parameters for methods | `false` |
| `use-escaping` | Single-quote escaping syntax | `false` |
| `use-deferred-loading` | Lazy-load locale files (web) | `false` |
| `format` | Run dart format after gen | `true` |

### Tracking

| Option | Description |
|--------|-------------|
| `preferred-supported-locales` | Default locale priority list |
| `untranslated-messages-file` | File listing untranslated keys |
| `required-resource-attributes` | Require `@` metadata entries |

## ARB Escaping

Enable in l10n.yaml: `use-escaping: true`

```json
{ "escaped": "Hello! '{Isn''t}' this a wonderful day?" }
```

Result: `Hello! {Isn't} this a wonderful day?`

## Advanced

### Locale Override

```dart
Localizations.override(
  context: context,
  locale: const Locale('es'),
  child: CalendarDatePicker(...),
)
```

### Complex Locale Definitions

```dart
supportedLocales: [
  Locale.fromSubtags(languageCode: 'zh'),
  Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hans'),
  Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hant', countryCode: 'TW'),
]
```

### Deferred Loading (Web)

Reduces initial bundle size — loads locale files on demand.

```yaml
use-deferred-loading: true
```

```dart
Future<AppLocalizations> loadLocale(String localeCode) async =>
    await AppLocalizations.delegate.load(Locale(localeCode));
```

## Best Practices

1. Use gen-l10n for new projects
2. Add `description` to ARB entries — translator context
3. Use `format` for numbers/dates — automatic locale handling
4. Use placeholders — never concatenate strings
5. Enable `nullable-getter: false` to avoid null checks
6. Use descriptive keys: `userProfileTitle` not `title1`
7. Specify `type` in placeholders — improves generated code type safety
