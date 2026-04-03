# Development Coded By Benxx!
import asyncio
import os
import random
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.account import ReportPeerRequest
from telethon.tl.types import (
    InputReportReasonViolence,
    InputReportReasonChildAbuse,
    InputReportReasonFake,        # Penipuan/Akun Palsu
    InputReportReasonPornography, # Tindakan Seksual
)
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn

console = Console()

# API ID & Hash milikmu
API_ID = 39013074         
API_HASH = "f855b33fdd2797a6c8d1fa621b195011"

DEFAULT_DELAY = 12.0 # Delay agak lama agar akun pribadi tetap aman

# Daftar alasan berat yang kamu minta
REASONS_LIST = [
    InputReportReasonViolence(),
    InputReportReasonChildAbuse(),
    InputReportReasonFake(),
    InputReportReasonPornography()
]
REASON_NAMES = ['Kekerasan', 'Pelecehan Anak', 'Penipuan', 'Tindakan Seksual']

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

    name_idx = REASONS_LIST.index(reason)
    msg = f"Laporan Otomatis - {REASON_NAMES[name_idx]}"
    try:
        # Eksekusi laporan ke server
        await client(ReportPeerRequest(peer=entity, reason=reason, message=msg))
        console.print(f"[green]✓ Report [{REASON_NAMES[name_idx]}] Sent To {target} Using {client.session.filename}[/green]")
        await asyncio.sleep(random.uniform(delay, delay + 3))
        return True
    except Exception as e:
        console.print(f"[red] ! Error Report {target} using {client.session.filename}: {e}[/red]")
        return False

async def rotate_reports(clients, targets, max_reports_per_target=100, delay=DEFAULT_DELAY):
    total_reports = len(targets) * max_reports_per_target * len(clients)
    with Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Proses Laporan...", total=total_reports)

        for _ in range(max_reports_per_target):
            for target in targets:
                # Membersihkan username target
                clean_target = target.lower().replace("@", "").replace("https://t.me/", "").split('/')[-1]
                
                for client in clients:
                    try:
                        # Proteksi lapor diri sendiri
                        me = await client.get_me()
                        me_username = me.username.lower() if me.username else ""
                        
                        if clean_target == me_username or clean_target == str(me.id):
                            progress.update(task, advance=1)
                            continue
                        
                        # Pilih alasan dari daftar berat
                        reason = random.choice(REASONS_LIST)
                        await report_target(client, target, reason, delay)
                        progress.update(task, advance=1)
                    except Exception:
                        progress.update(task, advance=1)
                        continue

async def main():
    console.print("[bold cyan] TELEGRAM BANEND BY Bͯͯeͯͯnͯͯxͯͯxͯ [/bold cyan]\n")
     
    choice_mode = console.input("1 Single Target\n2 Multi Target File\nPilih 1/2 : ").strip()
    if choice_mode == "1":  
        targets = [console.input("Target username / link: ").strip()]
    elif choice_mode == "2":  
        path = console.input("Path File targets (.txt): ").strip()
        targets = load_targets_file(path)
        if not targets:
            console.print("[red][!] File Target Kosong[/red]")
            return
    else:
        console.print("[red]Pilihan Tidak Valid[/red]")
        return

    max_reports = int(console.input("Jumlah Report (Default 100): ").strip() or 100)
    delay_sec = float(console.input(f"Delay Detik (Default {DEFAULT_DELAY}): ").strip() or DEFAULT_DELAY)

    session_paths = get_sessions()
    if not session_paths:
        console.print("[red]! Folder sessions kosong![/red]")
        return

    clients = []
    for sess in session_paths:
        client = TelegramClient(sess, API_ID, API_HASH)
        try:
            await client.start()
            clients.append(client)
        except SessionPasswordNeededError:
            console.print(f"[yellow][!] {sess} butuh Password 2FA[/yellow]")
        except Exception as e:
            console.print(f"[red][!] Gagal login {sess}: {e}[/red]")

    if not clients:
        console.print("[red]! Tidak ada akun aktif[/red]")
        return

    table = Table(title="LOG DATA")
    table.add_column("Akun Aktif", justify="center")
    table.add_column("Target", justify="center")
    table.add_row(str(len(clients)), str(len(targets)))
    console.print(table)

    console.print("[bold green]! Memulai Laporan Berat...[/bold green]\n")
    await rotate_reports(clients, targets, max_reports, delay_sec)
     
    for client in clients:
        await client.disconnect()

    console.print("\n[bold green]✓ Selesai Beraksi![/bold green]")

async def add_number():
    phone = console.input("Nomor (+62xxx): ").strip()
    sessions = get_sessions()
    next_id = len(sessions) + 1
    sess = f"sessions/acc{next_id}"
    client = TelegramClient(sess, API_ID, API_HASH)
    try:
        await client.start(phone)
        console.print(f"[green]✓ Berhasil! Akun disimpan di {sess}.session[/green]")
    except Exception as e:
        console.print(f"[red]! Gagal: {e}[/red]")

if __name__ == "__main__":
    console.print("[bold cyan] TELEGRAM BANEND BY Bͯͯeͯͯnͯͯxͯͯxͯ [/bold cyan]")
    console.print("1 Jalankan Report")
    console.print("2 Tambah Akun Baru")
    pilih = console.input("Pilih 1/2 : ").strip()

    if pilih == "1":  
        asyncio.run(main())
    elif pilih == "2":  
        asyncio.run(add_number())
    else:  
        console.print("[red]Pilihan Salah[/red]")
