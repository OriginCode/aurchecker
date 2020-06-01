# AUR Checker

The tool will automatically check updates for AUR packages in `pkgs.conf (default path: ${HOME}/.config/aurchk/pkgs.conf)` and clone the repo from AUR to a specific location `(default path: ${HOME}/.cache/aurchk/)`.

Default directory structure:

    $HOME/
        .config/
            aurchk/
                config.json
                pkgs.json
        .cache/
            aurchk/
