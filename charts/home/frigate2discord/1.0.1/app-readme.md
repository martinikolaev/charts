# Frigate2Discord

[Frigate2Discord] is a PVR for Usenet and BitTorrent users. It can monitor multiple RSS feeds for new episodes of your favorite shows and will grab, sort and rename them.

> When application is installed, a container will be launched with **root** privileges.
> This is required in order to apply the correct permissions to the `Frigate2Discord` directories.
> Afterward, the `Frigate2Discord` container will run as a **non**-root user (Default: `568`).
> All mounted storage(s) will be `chown`ed only if the parent directory does not match the configured user.
