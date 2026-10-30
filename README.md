The SupraTester for the 42 school libft (Linux ~~Mac Os~~)

# INSTALLATION

	clone the repo inside your libft or at its root.
	run './install.sh' to compile and install the libft_tester
	the `libft_tester` file has been created
	run it with `./libft_tester`

# REQUIREMENTS
	``vala``
	``a C compiler (clang or gcc)``
	``meson and ninja``

# VERSUS MODE

Benchmark your libft against the libc or against another libft:

	./libft_tester --versus libc               # your libft vs the glibc (+ libbsd for strlcpy/strlcat/strnstr)
	./libft_tester --versus ../other_libft     # a folder with a Makefile, it gets compiled
	./libft_tester --versus other/libft.a      # a static archive
	./libft_tester --versus other/libft.so     # a shared library

15 rounds are played: `strlen`, `memcpy`, `memset`, `bzero`, `memmove`, `memchr`, `memcmp`,
`strchr`, `strrchr`, `strncmp`, `strlcpy`, `strlcat`, `strnstr`, `strdup` and `atoi`.

Each round runs on 4 sizes: `light` (32 bytes), `medium` (4 KB), `max` (1 MB) and `max+1`
(1 MB on an unaligned address). `atoi` uses `short`, `int_min` and `spaces` inputs instead.

- The best of 5 runs is kept for each side, and the fork cost is removed from the time.
- A size is won when one side is more than 5% faster; the round goes to whoever wins the most sizes.
- A missing function means a **FORFEIT**: the opponent wins the round.
- A **K.O.** means you lost a round by a huge gap (x50 against the libc, x5 against another libft).

The recap shows the ratio for every function (`×N` = N times slower, `▲×N` = N times faster),
the final score and the mean gap. Against the libc you also get a level, from `beginner` to `GLIBC KILLER`.

# NOTES

If you see some 'EEEEEEE', it's because the libft_tester fills the stack and the heap with 'E' before running your tests.

`[🛡️ ]` means your function survives NULL arguments, `[  ]` means it crashes on them.
NULL is undefined for the non-libc functions (part 2 and 3), so both are fine.

# SupraTester

It loads your functions and tests them
asynchronously and fast on several processors.

It checks the memory with SupraLeak to stay fast :)

An idea? Something else? Open an issue!

# 42TUI fork

This fork is based on [nda-cunh/libft_tester](https://github.com/nda-cunh/libft_tester) commit `fa0062fe805ff55179ad4bfd5ccd8d19d3c330fd` and retains its GPL license. It does not update itself automatically.

Build and run the container against a **disposable copy** of a libft project (the tester runs its Makefile and creates build artifacts):

```sh
docker build -t 42tui-tester-libft .
docker run --rm --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges --pids-limit 512 \
  --tmpfs /tmp:rw,exec,nosuid,nodev,size=256m \
  --mount "type=bind,source=/absolute/path/to/disposable-copy,target=/project" \
  42tui-tester-libft --report /project/result.json
```

The optional `--report PATH` writes a version 1 JSON summary with `version`, `total`, `passed`, `failed`, `errors`, and `skipped`. It counts displayed checks, missing functions and forbidden symbols; warnings count as skipped. The destination must not exist. Normal execution includes the linked-list tests. `--report` cannot be combined with `--versus`. Exit status is 0 for success, 1 for failed checks or inspection errors, and 2 for setup or report errors; the container watchdog returns 124 on timeout. A failed build does not create a report.

Run `python3 tests/check_container.py 42tui-tester-libft` to check the container report and failure paths.
