

```dial

title: Foo Bar Baz

foo.title: Lorem ipsum
foo.type: actor

foo -> bar
  bar -> baz: int func(a, b)
  bar -> baz: (a, b) func(a, b)
  bar -> qux: func(a)
    # This is comment
    @over:
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
      tempor incididunt ut labore et dolore.
    @over bar: note
    @over bar~qux: note
    @over bar~: note
    @over ~bar: note
    @left of bar: note
    @right of qux: note

    qux -> quux: func(a)
    
  for i in list
    qux -> quux: func(a)

  if condition
    qux -> quux: int func(a)
  elif condition
    qux -> quux
  else
    qux -> bar
  
```


## Tokenizer
- Semicolon
- Loop

## Sequence Diagram
- call
- loop
- if
- note: right left over
- comment
- actor
- parallel
- Include

## Class Diagram
## State Diagram
