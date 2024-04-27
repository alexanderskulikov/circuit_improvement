import sys
from pathlib import Path
project_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(project_dir))

import asyncio
import queue
import sys

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from multiprocessing import Process, Queue
from pathlib import Path
from core.circuit_improvement import *


def get_file_name(basis, id):
    folder = Path(__file__).absolute().parent / 'circuits'
    print(folder, file=sys.stderr)
    matching_files = [file for file in folder.glob(f"{basis}_ex{id}*.bench") if file.is_file()]
    assert len(matching_files) == 1, f"Found {len(matching_files)} files, expected 1: {matching_files}"
    return str(matching_files[0].name)[:-6]


log_queue = Queue()


async def log_queue_listener():
    while True:
        if not log_queue.empty():
            chat_id, bot, message = log_queue.get()
            await bot.send_message(chat_id=chat_id, text=message)
        await asyncio.sleep(1)


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
            log(f'Processing {file_name} of size {ckt.get_nof_true_binary_gates()} ({datetime.now()})')
            improve_circuit_iteratively(ckt, file_name, basis=basis, speed=speed)
            log(f'Done improving {file_name}! ({datetime.now()})')
    except Exception as e:
        log(f'Error: {e}')
    log("Finished :-)")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Hi, this bot can improve circuits. '
                                        f'Send /improve basis circuit_number speed to start.')


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
                                       text=f'Usage: /improve basis circuit_id')
        return
    basis = context.args[0]
    circuit_number = context.args[1]

    file_name = get_log_path(basis, circuit_number)

    text = "\n".join(get_lines(file_name)[-10:]) or "No log found"
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'{text}')


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
                                       text=f'Basis should be aig or xaig')
        return
    if speed not in ['fast', 'medium', 'slow']:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'Speed should be fast/medium/slow')
        return

    p = Process(target=improve_circuit,
                args=(basis, circuit_number, speed, get_log_path(basis, circuit_number), log_queue))
    p.start()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Started. Use /log {basis} {circuit_number} to get status')


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = []
    while True:
        try:
            msg = log_queue.get(timeout=0.1)
            text.append(msg)
        except queue.Empty:
            break
    text = "\n========\n".join(text)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Messages:\n\n{text}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: bot-token")
        sys.exit(1)
    token = sys.argv[1]

    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    improve_handler = CommandHandler("improve", improve)
    log_handler = CommandHandler("log", get_log)
    check_handler = CommandHandler("check", check)
    application.add_handlers([start_handler, improve_handler, log_handler, check_handler])

    application.run_polling()


if __name__ == '__main__':
    main()
