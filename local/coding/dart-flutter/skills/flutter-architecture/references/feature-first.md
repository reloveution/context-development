# Feature-First Architecture

## Structure

```
lib/
├── features/
│   ├── auth/
│   │   ├── data/          # impl/repo/
│   │   ├── domain/        # entities/, usecases/, repo/, services/
│   │   └── presentation/  # controllers/, pages/, widgets/
│   ├── todos/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   └── settings/
│       ├── data/
│       └── presentation/  # skip domain/ if simple
├── shared/
│   ├── core/              # constants/, theme/, utils/
│   ├── data/              # shared models/, services/ (network, storage)
│   └── ui/                # reusable widgets/, components/
└── main.dart
```

## Feature-First vs Layer-First

| | Feature-First | Layer-First |
|---|---|---|
| When | 10+ features, 2+ devs, complex logic | <10 features, solo/small team |
| Pros | Self-contained features, easy add/remove, fewer merge conflicts | Clear layer separation, less nesting |
| Cons | More nesting, shared code needs organization | Harder to delete features, cross-folder changes |

## Naming

- Feature folders: plural, snake_case — `auth/`, `todos/`, `user_profile/`
- Files: `snake_case.dart` → `PascalCase` class
- Component folders: plural — `controllers/`, `pages/`, `widgets/`, `usecases/`, `entities/`

## Dependency Rules

- `presentation/ → domain/ → data/` within a feature
- All layers can use `shared/`
- **Features must NOT depend on each other** — move common logic to `shared/` or use DI with interfaces

## Adding a New Feature

1. Create `features/new_feature/` with `data/`, `presentation/`, optionally `domain/`
2. Implement bottom-up: entities → datasources → repositories → usecases → controllers → pages
3. Add barrel file: `features/new_feature/new_feature.dart` exporting public API
4. Register in DI container

## Migration from Layer-First

Gradual: new features use feature-first; migrate existing one at a time; extract shared code to `shared/`.
