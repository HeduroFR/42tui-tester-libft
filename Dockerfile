FROM debian:bookworm-slim@sha256:99c0b25c46d0214d5a2091092e7908907dcaecd6a962cde0ac700acee222b6f3 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev pkg-config valac meson ninja-build libglib2.0-dev libbsd-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /source
COPY . .
RUN meson setup /build --prefix=/opt/tester --buildtype=release && meson compile -C /build && meson install -C /build
FROM debian:bookworm-slim@sha256:99c0b25c46d0214d5a2091092e7908907dcaecd6a962cde0ac700acee222b6f3
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev make binutils libglib2.0-0 libbsd0 && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/tester /opt/tester
COPY LICENSE /opt/tester/share/LICENSE
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 HOME=/tmp
WORKDIR /project
ENTRYPOINT ["timeout", "--signal=TERM", "--kill-after=5s", "600s", "/opt/tester/bin/libft_tester"]
