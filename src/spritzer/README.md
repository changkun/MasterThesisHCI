# spritzer

`spritzer` is the actual website Action Path crawler for learning task.

## Usage

1. Setup `MongoDB` on your local machine
2. Modify your personal settings for `spritzer` in `settings/settings.go`, such as `staring point` and `database endpoint`
3. Run:

```go
go run spritzer.go
```

Ater running your data will be located in the database.

## Link Processing Strategy

Consider a page `url` and one of its pointing link `href`.

- Only cares response status code is 200

Different case for `url`:

- `url` with suffix `/`
- `url` without subffix `/`

Different case for `href`:

- `href` start with `http`
- `href` start with `/`:
- `href` start with `.`
- `href` start with `#`
- `href` leads to a file
- otherwise

## Licenses

 [CC-BY-NC 4.0](http://creativecommons.org/licenses/by-nc/4.0/) | [MIT](../LICENSE) | &copy; 2018 Changkun Ou
