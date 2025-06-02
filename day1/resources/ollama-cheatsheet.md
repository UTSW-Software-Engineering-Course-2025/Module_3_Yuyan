# Ollama cheatsheet

> Quick reference for running, managing, and integrating LLMs with [Ollama](https://ollama.com/).

---

## Managing the Ollama server

### Start the server in background
```bash
ollama serve &
```
### Storing downloaded models somewhere custom
```bash
export OLLAMA_MODELS=/your/path/to/models
```

### To stop the server:
```bash
pkill -f "ollama serve"
```

---

## Running Interactive Chat

```bash
ollama run qwen3:4b
```
- This will download the model weights if you don't have it already.
- Starts a chat session with the `qwen3:4b` model.
- Use `Ctrl+C` to quit.

---

## Managing Models

### Pull a model

```shell
ollama pull qwen3:4b
```

This command can also be used to update a local model. Only the diff will be pulled.

### Remove a model

```shell
ollama rm qwen3:4b
```

### Copy a model

```shell
ollama cp qwen3:4b my-model
```

### Multiline input

For multiline input, you can wrap text with `"""`:

```
>>> """Hello,
... world!
... """
I'm a basic program that prints the famous "Hello, world!" message to the console.
```

### Multimodal models

```
ollama run llava "What's in this image? /Users/jmorgan/Desktop/smile.png"
```

> **Output**: The image features a yellow smiley face, which is likely the central focus of the picture.

### Pass the prompt as an argument

```shell
ollama run qwen3:4b "Summarize this file: $(cat README.md)"
```

> **Output**: Ollama is a lightweight, extensible framework for building and running language models on the local machine. It provides a simple API for creating, running, and managing models, as well as a library of pre-built models that can be easily used in a variety of applications.

### Show model information

```shell
ollama show qwen3:4b
```

### List models on your computer

```shell
ollama list
```

### List which models are currently loaded

```shell
ollama ps
```

### Stop a model which is currently running

```shell
ollama stop qwen3:4b
```


## Environment Variables

| Variable              | Purpose                               |
|-----------------------|----------------------------------------|
| `OLLAMA_MODELS`       | Path to store models                   |
| `OLLAMA_HOST`         | Change bind address (e.g. for remote)  |
| `OLLAMA_DEBUG=1`      | Enable debug logs                      |

For example, to change the bind address to `127.0.0.1:11400` (default is `0.0.0.0:11434`)
```
export OLLAMA_HOST=127.0.0.1:11400
```