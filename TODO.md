# Current release

- ASCII Canvas
- Test self calls

## Sequence Diagram

- ascii
  - call hierarchy
  - note
  - loop
  - condition

# Next release

- Gallery

## SVG
## Syntaxt highlight
  Github Syntaxt highlight
  VIM Syntaxt highlight

## Sequence Diagram
- Parallel
- Include

## Class Diagram
## State Diagram

``` 

   test             pcap         main            httpd
    .                .            .               .
    .                .            .               .
  START              .            .               .
    |                .            .               .
    |________________             .               .
                     |            .               .
                    fork          .               .
     ________________|\___________                .
    |                             |               .
   test                           |               .
    |                             |               .
   stop                          fork             .
    |________________             |\______________ 
                     |            |               |
                    kill ------> kill ---------> loop 
                     |            | ______________|    
                    wait          |/                   
                     |           join
                     | ___________|
                     |/
                    join
     ________________|
    |
   EXIT
```

```

                           +---------------+           +------------------+
                           | struct peer   |   +------>| enum peer_state  |
                           +---------------+   |       +------------------+
                           |  fd           |   |       |  PS_READ         |
                           |  state        >---+       |  PS_WRITE        |
                           |  writebuff[]  |           +------------------+
                           |  writerb      |
                           | *handler      |           +------------------+
                           +---------------+       +-->| struct ev_epoll  |
                                                   |   +------------------+
  +-----------------+      +---------------+       |   |  epollfd         |
  | struct ev       |  +-->| union ev_priv |       |   +------------------+
  +-----------------+  |   +---------------+       |
  |  id             |  |   |  ev_epoll     >-------+   +------------------+
  |  forks          |  |   |  ev_select    >---------->| struct ev_select |
  |  children[]     |  |   |  ev_mock      >-------+   +------------------+
  |  private_data   >--+   +---------------+       |   | ?                |
  +-----------------+                              |   +----------------- +
  | *on_recvd       |                              |
  | *on_writefinish |                              |   +------------------+
  +-----------------+                              +-->| struct ev_mock   |
      ^         ^                                      +------------------+
      |         |                                      | ?                |
      |         +--------------+                       +------------------+
      |                        |
  +---^-----------+        +---^------------+
  | struct ev_srv |        | struct ev_clnt |
  +---------------+        +----------------+
  | +struct ev    |        | +struct ev     |
  |  listenfd     |        |  hostname      |
  |  bind         |        |  port          |
  +---------------+        +----------------+
  | *on_connect   |        |  ?             |
  +---------------+        +----------------+

```
