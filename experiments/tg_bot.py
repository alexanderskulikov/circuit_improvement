import signal
import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(project_dir))

import asyncio
import logging
import queue
import sys

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from multiprocessing import Process, Queue
import multiprocessing
from pathlib import Path
from core.circuit_improvement import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
log_queue = Queue()
processes = dict()
processes_lock = multiprocessing.Lock()
subscribed = set()
subscribed_lock = asyncio.Lock()


def kill_all_processes():
    with processes_lock:
        for p in processes.values():
            p.kill()
        for p in processes.values():
            p.join()


def get_file_name(basis, id):
    folder = Path(__file__).absolute().parent / 'circuits'
    print(folder, file=sys.stderr)
    matching_files = [file for file in folder.glob(f"{basis}_ex{id}*.bench") if file.is_file()]
    assert len(matching_files) == 1, f"Found {len(matching_files)} files, expected 1: {matching_files}"
    return str(matching_files[0].name)[:-6]


def improve_circuit(basis, circuit_number, speed, log_file, queue: Queue):
    def log(text):
        queue.put(f"{basis}_{circuit_number}: {text}")
        print(text)

    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    out = open(log_file, "w")
    sys.stderr = out
    sys.stdout = out

    try:
        file_name = get_file_name(basis, circuit_number)
        ckt = Circuit()
        ckt.load_from_file(file_name, extension='bench')
        ckt.normalize(basis)

        if len(ckt.gates) < ckt.get_nof_true_binary_gates():
            log(f'Skipping {file_name} as it still contains unary gates')
        else:
            log(f'Started Processing {file_name} of size {ckt.get_nof_true_binary_gates()} ({datetime.now()})')
            improve_circuit_iteratively(ckt, file_name, basis=basis, speed=speed)
            log(f'Done improving {file_name}! ({datetime.now()})')
    except Exception as e:
        log(f'Error: {e}')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Hi, this bot can improve circuits. '
                                        f'Send /improve basis circuit_number speed to start.')
    await subscribe(update, context)


def get_log_path(basis, id):
    return Path(__file__).parent / "log" / f"{basis}_{id}.log"


def get_lines(logfile_path):
    lines = []
    with open(logfile_path, 'rb') as file:
        for line in file.read().decode('utf-8').split('\n'):
            lines.append(line.split('\r')[-1])
    return lines


async def get_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'Usage: /log basis circuit_id')
        return
    basis = context.args[0]
    circuit_number = context.args[1]
    for i in range(3):
        try:
            file_name = get_log_path(basis, circuit_number)
            text = "\n".join(get_lines(file_name)[-10:]) or "No log found"
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'{text}')
            break
        except BaseException as e:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'Something wrong with log. I will try one more time: {e}')
            await asyncio.sleep(5)
            continue
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Didn't manage to get log")


async def clear_finished_processes(context: ContextTypes.DEFAULT_TYPE):
    with processes_lock:
        for key, p in list(processes.items()):
            if p.is_alive():
                continue
            p.join()
            if p.exitcode != 0:
                await context.bot.send_message(chat_id=context._chat_id,
                                               text=f'Process ({key}) is terminated with code: {p.exitcode}')
            processes.pop(key)


async def get_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await clear_finished_processes(context)
    text = []
    with processes_lock:
        for basis, circuit_number in processes.keys():
            text += [f"{basis} {circuit_number}"]
    text = '\n'.join(text) or "No running processes"
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text)


async def improve(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 3:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'Usage: /improve basis circuit_id speed')
        return
    basis = context.args[0]
    circuit_number = context.args[1]
    speed = context.args[2]
    if basis not in ['aig', 'xaig']:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'Error: Basis should be aig or xaig')
        return
    if len(circuit_number) != 2 or not circuit_number.isdigit():
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Warning: Circuit number should be two digit number, got: {circuit_number}. Example: 03")
    if not speed.isdigit() or not 2 <= int(speed) <= 17:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Warning: speed should be a number from [2, 17], got: {speed}")

    await clear_finished_processes(context)
    with processes_lock:
        if (basis, circuit_number) in processes.keys():
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"Such circuit is already in progress")
            return

    await subscribe(update, context)
    p = Process(target=improve_circuit,
                args=(basis, circuit_number, int(speed), get_log_path(basis, circuit_number), log_queue))
    p.start()

    with processes_lock:
        processes[(basis, circuit_number)] = p
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Started. Use /log {basis} {circuit_number} to get status')


async def manual_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.chat_id = update.effective_chat.id
    await check_messages(context)


async def check_messages(context: ContextTypes.DEFAULT_TYPE) -> None:
    text = []
    while True:
        try:
            msg = log_queue.get(timeout=0.1)
            text.append(msg)
        except queue.Empty:
            break
    if text:
        text = "\n========\n".join(text)
        await context.bot.send_message(chat_id=context._chat_id,
                                       text=f"{text}")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async with subscribed_lock:
        if update.effective_chat.id in subscribed:
            return
        subscribed.add(update.effective_chat.id)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Subscribed for updates")
    context.job_queue.run_repeating(check_messages, interval=10, first=0, chat_id=update.effective_chat.id)
    context.job_queue.run_repeating(clear_finished_processes, interval=10, first=0, chat_id=update.effective_chat.id)


async def kill_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 2:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'Usage: /kill basis circuit_id')
        return
    basis = context.args[0]
    circuit_number = context.args[1]
    await clear_finished_processes(context)
    key = (basis, circuit_number)
    with processes_lock:
        if key not in processes.keys() or not (p := processes[key]).is_alive():
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"{basis} {circuit_number} is not processing now")
        else:
            p.kill()
            p.join()
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"Killed {basis} {circuit_number}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: bot-token")
        sys.exit(1)
    token = sys.argv[1]

    application = ApplicationBuilder().token(token).build()

    application.add_handlers([CommandHandler('start', start),
                              CommandHandler("improve", improve),
                              CommandHandler("log", get_log),
                              CommandHandler("status", get_status),
                              CommandHandler("kill", kill_process)])
    try:
        application.run_polling()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Killing all the subprocesses...")
        kill_all_processes()


if __name__ == '__main__':
    main()
