# gink

`gink` is the Action Path crowdsourcing data labeling tool.

## Usage

1. Setup `MongoDB` on your local machine
2. Run [`spritzer`](https://github.com/changkun/spritzer) for some unsupervised dataset
3. Run:

```go
go run gink.go
```

Then you can access the labeling tool on `localhost:12346/tool`.

## Interfaces

- GET: `/tool`
- GET: `/api/v1/ping`
- GET: `/api/v1/path`
- POST: `/api/v1/path`
- POST: `/api/v1/node`

## Architecture

```
  (external)   store to collection `node`
  spritzer ------------------------------> Database <--+
                                              |       | write to collection
                  fetch Action Path algorithm |       | `supervised` and `node` 
                                              v       | if participant provided
   user <---------------------------------> gink -----+
              Labeling an Action Path     (daemon)
```

## Challenges

- `gink` find action path randomly start from a staring point;
- sometimes the path finally points to somewhere can be represented by a short path (Shortest path problem);
    - Solution: After find the action path, should apply shortest path check, if it is not a shortest path, then retry
- Will all path be labeled eventually? --> Hamiltonian path problem (NP-complete)
- How long should a path be presented;

Supervised path structure:

```json
{
    "path": [
        "http://xxxxx",
        "http://xxxxx/sdd",
        "http://xxxxx/ewfe",
        "http://xxxxx/ewth",
        "http://xxxxx/qwerfwb/sgfddh"
    ],
    "manual_desc": "labeled description"
}
```

- A Path contains a list of links, which satisfy the order of visiting by a user.
- A link is an unique id for a page, detail information can be found in another collection of the mongodb database

```json
{
    "url": "http://www.medien.ifi.lmu.de",
    "value": "entry page",
    "meta": [],
    "keywords": [],
    "manual_desc": "",
    "source_code": "source code of the page",
    "is_end": false,
    "next": [
        {
            "url": "http://www.medien.ifi.lmu.de/mt/",
            "value": "Medientechnik"
        },
        {
            "url": "http://www.medien.ifi.lmu.de/mmp/",
            "value": "Multimedia-Programmierung"
        }
    ]
}
```

Thus, participants can also change the data of a node, such as describe the node.


## Licenses

 [CC-BY-NC 4.0](http://creativecommons.org/licenses/by-nc/4.0/) | [MIT](../LICENSE) | &copy; 2018 Changkun Ou
