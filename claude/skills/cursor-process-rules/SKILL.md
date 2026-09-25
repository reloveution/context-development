---
name: cursor-process-rules
description: Development process rules. Use when planning complex tasks, implementing incrementally, managing packages, or following communication guidelines.
---

# Process Rules

## Incremental Development

For complex tasks (multiple files, architectural changes):
1. Analyze → create step-by-step plan → present for review
2. Implement one step at a time with complete, ready-to-use code
3. Wait for user confirmation before next step
4. Answer clarifying questions before continuing

## Clarification

- Ask clarifying questions for ambiguous requirements — don't assume
- Clarify: intended functionality, target platform, edge cases, constraints

## Communication

- Terminate immediately after delivering information
- No "Let me know if...", "Feel free to..." closures
- Cognitive efficiency over conversational flow
- When suggesting new dependencies, explain their benefits

## Code Generation

- Dynamic code generators, not hard-coded static examples
- Always specify exact file name
- Be thorough; provide complete code per step

## Package Management

- Use `mcp_dart_pub` if available; otherwise `flutter pub add <package>`
- Dev deps: `pub add dev:<package>` or `flutter pub add dev:<package>`
- Override: `override:<package>:1.0.0`
- Remove: `dart pub remove <package>`
- Discovery: `pub_dev_search` first

## User Persona

- User is familiar with programming but may be new to Dart
- Explain Dart-specific features (null safety, futures, streams) when relevant
