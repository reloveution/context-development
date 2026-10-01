---
title: Images, Database, Files
description: Caching, connections, handles
---

# Images

- Implement proper image caching and disposal.
- Use appropriate eviction policies; don't hold unlimited image data.

# Database

- Use proper database connection management and closing.
- Close connections when no longer needed.
- Don't leave connections open across lifecycle boundaries.

# Files

- Use proper file handle management and closing.
- Close `IOSink`, `RandomAccessFile`, and other file streams.
- Use try-finally or ensure cleanup on error paths.
