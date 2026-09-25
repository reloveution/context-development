---
name: dart-naming-conventions
description: Project naming conventions for Dart/Flutter. Use when naming interfaces (I prefix), implementations (Impl), use cases (Usc), datasources (Dts), extensions (X), mixins (Mxn), or organizing feature/datasource folders.
---

# Dart Naming Conventions

## Suffixes and Prefixes

| Pattern | Convention | Example |
|---|---|---|
| Interface | `I` prefix | `IExportRepo`, `IApiMagDecDts` |
| Implementation | `Impl` suffix | `MagDecRepoImpl`, `NoaaApiMagDecDtsImpl` |
| Use case | `Usc` suffix | `GetMagDecUsc`, `ExecuteProjectExportUsc` |
| Datasource | `Dts` suffix | `IApiMagDecDts`, `IExcellExportDts` |
| Extension | `X` suffix | `DateTimeX`, `DurationX` |
| Mixin | `Mxn` suffix | `MxnExcelFormatting`, `MxnRepoCharsXlsxDisc` |
| Rare function | `$` prefix (hides from autocomplete) | `$helper` |

## Folder and Variable Abbreviations

- Use `repo` not `repository` in class/folder/variable names.
- Use `dts` not `datasource` in class/folder/variable names.
- Multiple extensions in a feature: organize in `X/` folder.

## Datasource Implementation Naming

- Interface: `I{FeatureMarking}Dts` -- `IDocumentDts`, `IApiMagDecDts`.
- Implementation with external package: `{PackageName}{FeatureMarking}DtsImpl` -- `ExcelExportDtsImpl`, `NoaaApiMagDecDtsImpl`.
- Multiple datasources per repository: separate folders per source -- `api/`, `excell/`, `csv/`.

## Abbreviations

- Avoid abbreviations unless context is unambiguous.
- Bad: `idx` (index of what?). Good: `fs` for fracture systems when context is clear.

## Acronyms

- Acronyms >2 letters capitalize as words: `HttpClient`, `SqlRepository` (not `HTTPClient`).
