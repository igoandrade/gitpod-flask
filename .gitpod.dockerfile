FROM gitpod/workspace-full-vnc

RUN sudo apt-get update  && sudo apt-get install -y nano  && sudo rm -rf /var/lib/apt/lists/*
