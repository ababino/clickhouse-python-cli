# ClickHouse Python CLI

A personal workaround for using ClickHouse over SSH tunnels. This script exists because the native ClickHouse client has issues when used over SSH tunnels, particularly with hostname resolution and certificate verification.

## What it does

This is a Python-based CLI that mimics the basic behavior of the `clickhouse client` command but:

1. Always uses `localhost` as the actual connection host
2. Uses the `--host` parameter value as the `server_host_name` for SNI
3. Supports both interactive and non-interactive modes

## Why?

This is probably not useful to anyone else but me. I created it because I frequently need to connect to ClickHouse through SSH tunnels, and the native client doesn't handle this scenario well, especially with cloud instances and certificate verification.

## Usage

```bash
./main.py client --host your.actual.host --user youruser --secure -q "SELECT 1"
```

Or in interactive mode:

```bash
./main.py client --host your.actual.host --user youruser --secure
```

## Requirements

- Python 3.x
- clickhouse-connect
