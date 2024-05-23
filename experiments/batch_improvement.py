import argparse
import sys
import time
from pathlib import Path
import logging

sys.path.append(str(Path(__file__).absolute().parent.parent))

from core.circuit_improvement import *
from datetime import datetime
from os import listdir
from concurrent.futures import ProcessPoolExecutor, as_completed, Future
from multiprocessing import Process, Queue
import curses
import tempfile

log_dir = Path(tempfile.gettempdir())


def get_log_file(log_id):
    return log_dir / f"log_{log_id}.log"


home_log = []
home_log_queue = Queue()


def print_home(s):
    home_log_queue.put(s)


def process_circuit(file_number, total_files, file_name, basis, speed, forward_output=False):
    ckt = Circuit()
    ckt.load_from_file(file_name[:-6], extension='bench')
    ckt.normalize(basis)
    text = f'[{file_number}/{total_files}] Processing {file_name[:-6]} of size {ckt.get_nof_true_binary_gates()} ({datetime.now()})'
    print_home(text)
    if forward_output:
        set_output(file_number)
        print(text)
    improve_circuit_iteratively(ckt, file_name[:-6], basis=basis, speed=speed)
    print_home(f"Done [{file_number}] {file_name}")


def improve_batch(basis, speed, threads):
    if threads > 1:
        clear_output("home")
        set_output("home")
    print_home(f'Start batch improvement ({datetime.now()}). basis: {basis}, speed: {speed}, threads: {threads}')
    files = sorted(listdir('./circuits/'))
    with ProcessPoolExecutor(max_workers=threads) as pool:
        tasks = []
        for file_number, file_name in enumerate(files):
            if file_name == '.images':
                continue
            clear_output(file_number)
            if threads == 1:
                process_circuit(file_number, len(files), file_name, basis, speed, False)
            else:
                task = pool.submit(process_circuit, file_number, len(files), file_name, basis, speed, True)
                tasks.append(task)

        for task in as_completed(tasks):
            exception = task.exception()
            assert exception is None, f"{exception}"
            assert task.done()
    print(f'Done! ({datetime.now()}). Enter quit to exit')


def set_output(log_id):
    log_filepath = get_log_file(log_id)
    log_file = log_filepath.open("a")
    sys.stderr = log_file
    sys.stdout = log_file


def clear_output(log_id):
    log_filepath = get_log_file(log_id)
    if log_filepath.is_file():
        log_filepath.unlink()


def print_lines(lines, stdscr):
    max_y, max_x = stdscr.getmaxyx()

    def safe_add(s):
        stdscr.addstr(f"{s[:max_x - 1]}\n")

    lines = lines[-(max_y - 2):]
    for line in lines:
        safe_add(line)


def print_screen(screen, stdscr):
    if screen == "home":
        while not home_log_queue.empty():
            home_log.append(home_log_queue.get())
        print_lines(home_log, stdscr)
        return

    file = get_log_file(screen)

    if file.is_file():
        with file.open("rb") as file:
            lines = []
            text = file.read().decode('utf-8')
            for line in text.split('\n'):
                lines.append(line.split('\r')[-1])
            print_lines(lines, stdscr)
    else:
        print_lines(["Log file does not exist."], stdscr)


def run_tui(stdscr):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    current_screen = "home"
    next_screen_name = []

    try:
        while True:
            time.sleep(0.05)
            stdscr.clear()
            stdscr.addstr(f"\"{current_screen}\" log:\n")
            max_y, max_x = stdscr.getmaxyx()
            print_screen(current_screen, stdscr)

            stdscr.addstr(max_y - 1, 0,
                          f"Enter \"run id\" or \"quit\" or \"home\" and press Enter: {''.join(next_screen_name)}"[
                          -(max_x - 1):])
            stdscr.refresh()

            key = stdscr.getch()
            if key == -1:
                continue
            elif key == curses.KEY_BACKSPACE or key == 127:
                if next_screen_name:
                    next_screen_name.pop()  # Remove last digit
            elif key == 10:  # Enter key
                if next_screen_name:
                    next_screen_name = "".join(next_screen_name)
                    if next_screen_name == "quit":
                        break
                    current_screen = next_screen_name
                    next_screen_name = []
            elif ord('0') <= key <= ord('9') or ord('a') <= key <= ord('z') or ord("A") <= key <= ord("Z"):
                next_screen_name.append(chr(key))
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(2, 0, f"An error occurred: {str(e)}")
        stdscr.refresh()
        stdscr.getch()

    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


def start(stdscr, basis, speed, threads):
    improve_process = Process(target=improve_batch, args=[basis, speed, threads])
    improve_process.start()
    run_tui(stdscr)
    print("TUI exited.")
    if improve_process.is_alive():
        print("Improving is still running. Try to kill it")
        improve_process.kill()
    improve_process.join()


def main():
    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument('--basis', type=str, choices=['xaig', 'aig'], required=True,
                        help="The basis for operation, can be either 'xaig' or 'aig'")
    parser.add_argument('--speed', type=int, choices=list(range(2, 18)), required=True,
                        help="The speed level, must be between 2 and 17")
    parser.add_argument('--threads', type=int, default=1,
                        help="The number of threads, must be greater than 1")

    args = parser.parse_args()

    basis = args.basis
    speed = args.speed
    threads = args.threads
    assert basis is not None
    assert speed is not None
    assert threads is not None

    if threads == 1:
        improve_batch(basis, speed, threads)
    else:
        try:
            curses.wrapper(start, basis, speed, threads)
        except BaseException as e:
            print(f"Curses error: {e}")


if __name__ == "__main__":
    main()
