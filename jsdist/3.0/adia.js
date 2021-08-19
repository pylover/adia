class ADia {
  delay = 0; // ms
  loadingProbeInterval = 300; // ms
  input;

  // inititializing, processing, idle
  #_status = 'initializing';

  /* Private Fields */
  #_delayTimer;
  #_source;

  constructor() {
    this.hooks = {
      result: [],
      success: [],
      error: [],
      status: [],
      init: [],
    }
    this.ensureADiaAPI();
  }
  
  addHook(name, func) {
    let handlers = this.hooks[name]
    if (!handlers.includes(func)) {
      handlers.push(func)
    }
  }
  
  hook(name, data) {
    let handlers = this.hooks[name]
    if (handlers == undefined) {
      throw `Invalid hook name: ${name}`;
    }
    
    for (var i = 0; i < handlers.length; i++) {
      handlers[i](this, data);
    }
  }

  get status() {
    return this.#_status;
  }

  set status(newValue) {
    this.#_status = newValue;
    this.hook('status', newValue);
  }

  ensureADiaAPI() {
    if (window.__adia__ == undefined) {
      setTimeout(this.ensureADiaAPI.bind(this), this.loadingProbeInterval);
      return;
    }
    
    window.__adia__.callback = this.onResult.bind(this);
    window.__adia__.send('?version');
  }
  
  send() {
    if (this.input == undefined) {
      return;
    }
    let newSource = this.input();
    if (this.#_source == newSource) {
      /* Do Nothing */
      return;
    }
    
    this.status = 'processing';
    this.#_source = newSource;
    window.__adia__.send(this.#_source);
  }

  go() {
    switch (this.status) {
      case 'idle':
        if (this.delay > 0) {
          clearTimeout(this.#_delayTimer);
          this.#_delayTimer = setTimeout(this.send.bind(this), this.delay);
        }
        else {
          this.send();
        }
      case 'initializing':
      case 'processing':
        /* Do nothing, initializer and fee will call me again. */
        break;
    }
  }
  
  onResult(result) {
    if (result.version != undefined) {
      this.__version__ = result.version
      this.hook('init')
    }
    else {
      this.hook('result', result)
      if (result.error) {
        this.hook('error', result.error)
      }
      else {
        this.hook('success', result.diagram)
      }
    }
    this.status = 'idle';
    this.go();
  }
}

window.aDia = new ADia();
