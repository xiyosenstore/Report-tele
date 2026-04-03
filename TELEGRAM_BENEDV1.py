# Development Coded By Benxx!
"""
"""

import asyncio
import os
import random
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.account import ReportPeerRequest
from telethon.tl.types import (
    InputReportReasonSpam,
    InputReportReasonFake,
    InputReportReasonViolence,
    InputReportReasonPornography,
    InputReportReasonChildAbuse,
)
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn

console = Console()

API_ID = 39013074         
API_HASH = "f855b33fdd2797a6c8d1fa621b195011"

DEFAULT_DELAY = 3.5
REASONS_LIST = [
    InputReportReasonSpam(),
    InputReportReasonFake(),
    InputReportReasonViolence(),
    InputReportReasonPornography(),
    InputReportReasonChildAbuse()
]
REASON_NAMES = ['spam', 'fake', 'violence', 'porn', 'child']





def get_sessions():
    if not os.path.exists("sessions"):
        os.mkdir("sessions")
    return [f"sessions/{x.replace('.session','')}" for x in os.listdir("sessions") if x.endswith(".session")]

def load_targets_file(path):
    if not os.path.exists(path):
        console.print(f"[red]! File {path} Tidak Ditemukan[/red]")
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]





async def report_target(client: TelegramClient, target: str, reason, delay=DEFAULT_DELAY):
    try:
        entity = await client.get_entity(target)
    except Exception as e:
        console.print(f"[red]! Target '{target}' Tidak Ditemukan: {e}[/red]")
        return False

    msg = f"Laporan Otomatis - {REASON_NAMES[REASONS_LIST.index(reason)]}"
    try:
        await client(ReportPeerRequest(peer=entity, reason=reason, message=msg))
        console.print(f"[green]✓ Report Sent To {target} Using {client.session.filename}[/green]")
        await asyncio.sleep(random.uniform(delay, delay + 2))
        return True
    except Exception as e:
        console.print(f"[red] ! Error Report {target} using {client.session.filename}: {e}[/red]")
        return False





async def rotate_reports(clients, targets, max_reports_per_target=100, delay=DEFAULT_DELAY):
    """
    
    """
    total_reports = len(targets) * max_reports_per_target * len(clients)
    with Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Melaporkan Target...", total=total_reports)

        for _ in range(max_reports_per_target):
            for target in targets:
                for client in clients:
                    await report_target(client, target, random.choice(REASONS_LIST), delay)
                    progress.update(task, advance=1)





async def main():
    console.print("[bold cyan] [/bold cyan]\n")

     
    choice_mode = console.input("1 Single Target\n2 Multi Target File\nPilih 1/2 : ").strip()
    if choice_mode == "1":  
        targets = [console.input("Target username / link: ").strip()]
    elif choice_mode == "2":  
        path = console.input("Path File targets (.txt): ").strip()
        targets = load_targets_file(path)
        if not targets:
            console.print("[red][!] Tidak Ada Target Valid Di File[/red]")
            return
    else:
        console.print("[red]Pilihan Tidak Valid[/red]")
        return

    max_reports = int(console.input("Jumlah Report Per Target 100/200 : ").strip() or 100)
    max_reports = max(100, min(max_reports, 200))
    delay_sec = float(console.input(f"Delay Antar Laporan Detik, Default {DEFAULT_DELAY}: ").strip() or DEFAULT_DELAY)

    
    session_paths = get_sessions()
    if not session_paths:
        console.print("[red]! Tidak Ada Session, Tambah Dulu Pakai Menu Add-Number![/red]")
        return

    clients = []
    for sess in session_paths:
        client = TelegramClient(sess, API_ID, API_HASH)
        try:
            await client.start()
            clients.append(client)
        except SessionPasswordNeededError:
            console.print(f"[yellow][!] Session {sess} Butuh 2FA, Skip...[/yellow]")
        except Exception as e:
            console.print(f"[red][!] Gagal Start Session {sess}: {e}[/red]")

    if not clients:
        console.print("[red]! Tidak Ada Session Aktif[/red]")
        return

    table = Table(title="TABLE")
    table.add_column("Sessions", justify="center")
    table.add_column("Targets", justify="center")
    table.add_column("Max Reports", justify="center")
    table.add_row(str(len(clients)), str(len(targets)), str(max_reports))
    console.print(table)

    console.print("[bold green]! Memulai Report...[/bold green]\n")
    await rotate_reports(clients, targets, max_reports, delay_sec)

     
    for client in clients:
        await client.disconnect()

    console.print("\n[bold green]✓Semua Report Selesai[/bold green]")





async def add_number():
    phone = console.input("Nomor Baru (+628xxx): ").strip()
    sessions = get_sessions()
    next_id = len(sessions) + 1
    sess = f"sessions/acc{next_id}"
    client = TelegramClient(sess, API_ID, API_HASH)
    try:
        await client.start(phone)
        console.print(f"[green]✓ Berhasil Ditambahkan → {sess}.session[/green]")
    except Exception as e:
        console.print(f"[red]! Gagal Tambah Nomor: {e}[/red]")





if __name__ == "__main__":
    console.print("[bold cyan] TELEGRAM BANEND BY Bͯͯeͯͯnͯͯxͯͯxͯ [/bold cyan]")
    console.print("1 Jalankan Report")
    console.print("2 Tambah Nomor Session")
    pilih = console.input("Pilih 1/2 : ").strip()

    if pilih == "1":  
        asyncio.run(main())
    elif pilih == "2":  
        asyncio.run(add_number())
    else:  
        console.print("[red]Pilihan Tidak Valid[/red]")
