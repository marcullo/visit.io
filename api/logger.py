#!/usr/bin/env python3

_LOG_PREFIX_LEN = 10
_VERBOSE = False


def log(message, indent=1, verbose=False):
    message = str(message)

    if verbose and not _VERBOSE:
        return

    if indent == 0:
        print(message)
        return

    prefix_len = _LOG_PREFIX_LEN + 3 * indent
    prefix, content = message.split(':', 1)
    prefix = prefix.strip().rjust(prefix_len) + ':'
    content = content.strip()
    print(prefix, content)


if __name__ == '__main__':
    log('logger: Hello, World!')
    log('verbose: Verbose message', verbose=True)
    log('indent: 2', indent=2)
    log('indent: 3', indent=3)
    log('hello: again')
