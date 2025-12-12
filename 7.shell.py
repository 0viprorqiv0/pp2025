import os
import shlex
import subprocess


def run_command(cmd):
    if "|" in cmd:
        parts = [p.strip() for p in cmd.split("|")]
        prev_process = None

        for part in parts:
            args = shlex.split(part)
            p = subprocess.Popen(
                args,
                stdin=prev_process.stdout if prev_process else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if prev_process:
                prev_process.stdout.close()
            prev_process = p

        out, err = prev_process.communicate()
        if out:
            print(out, end="")
        if err:
            print(err, end="")
        return

    tokens = shlex.split(cmd)
    stdin = None
    stdout = None

    if "<" in tokens:
        idx = tokens.index("<")
        try:
            stdin = open(tokens[idx + 1], "r")
        except FileNotFoundError:
            print(f"{tokens[idx + 1]}: No such file or directory")
        return
        tokens = tokens[:idx]

    if ">" in tokens:
        idx = tokens.index(">")
        stdout = open(tokens[idx + 1], "w")
        tokens = tokens[:idx]

    try:
        subprocess.run(tokens, stdin=stdin, stdout=stdout)
    except FileNotFoundError:
        print("Command not found")

    if stdin:
        stdin.close()
    if stdout:
        stdout.close()


def shell():
    while True:
        try:
            cmd = input("pysh> ").strip()
        except EOFError:
            break

        if not cmd:
            continue

        if cmd in ("exit", "quit"):
            break

        run_command(cmd)


if __name__ == "__main__":
    shell()
