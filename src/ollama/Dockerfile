FROM ollama/ollama

WORKDIR /

RUN ollama serve & sleep 15 && ollama pull gemma3

EXPOSE 11434

CMD ["serve"]