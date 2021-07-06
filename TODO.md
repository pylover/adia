## Dial roadmap

### Current release

- A complete example in readme.
- Remove SVG support and just support ASCII.

### Next release

- Personalize & configrations
- Gallery
- How to use inside javascript

#### Syntaxt highlight

- Github Syntaxt highlight
- VIM Syntaxt highlight
- VIM plugin to auto-render commented blocks


#### Sequence Diagram

- Parallel
- Include


#### Class Diagram

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

#### Fork Diagram

- Example of Git branching
- Example of Unix fork

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

#### State Diagram

- Need help for design


