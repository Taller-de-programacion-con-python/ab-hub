import argparse
import sys
import time


def notify_windows(title: str, message: str):
    try:
        from win10toast import ToastNotifier
        ToastNotifier().show_toast(title, message, duration=10, threaded=False)
        return True
    except Exception:
        pass
    try:
        import ctypes
        MB_ICONINFORMATION = 0x40
        ctypes.windll.user32.MessageBoxW(0, message, title, MB_ICONINFORMATION)
        return True
    except Exception:
        return False


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', default='Recordatorio')
    parser.add_argument('--message', required=True)
    args = parser.parse_args(argv)
    notify_windows(args.title, args.message)


if __name__ == '__main__':
    main()
