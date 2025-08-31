import time as tm
import os
import subprocess as sub
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.styles import Style
except ImportError:
    chiedi = input('Promt_toolkit is NOT installed, you want to install it?(Y/n): ')
    if chiedi == y or chiedi == Y:
        sub.check_call(["pip", "install", "prompt_toolkit", "--break-system-packages"])
        from prompt_toolkit import PromptSession
        from prompt_toolkit.styles import Style
    else:
        exit()

def rosso(testo):
    return f"\033[91m{testo}\033[0m"

def verde(testo):
    return f"\033[92m{testo}\033[0m"

def blu(testo):
    return f"\033[94m{testo}\033[0m"

def scrivi_programma(nome_programma):
    print("✍️ Tyoe in the Pitone script (write 'FINE' or 'fine' on a line to finish the script):\n")
    session = PromptSession()
    righe = []

    while True:
        try:
            riga = session.prompt()
            if riga.strip().upper() == "FINE":
                break
            righe.append(riga)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

    testo_completo = "\n".join(righe)
    compilatore(testo_completo, nome_programma)

def compilatore(testo_completo, nome_programma):
    #compilatore
    translated = [] 
    righe = testo_completo.splitlines()
    indentazione = 0

    for riga in righe:
        riga = riga.strip()

        def indenta():
            return "    " * indentazione

        if riga.startswith("scrivi "):
            contenuto = riga[7:].strip()
            translated.append(indenta() + f'print({contenuto})')

        elif "chiedi " in riga:
            if "→" in riga:
                parti = riga.split("chiedi")[1].split("→")
                domanda = parti[0].strip()
                variabile = parti[1].strip()
                translated.append(indenta() + f'{variabile} = input({domanda})')
            elif "=" in riga:
                sinistra, destra = riga.split("=", 1)
                variabile = sinistra.strip()
                if "chiedi" in destra:
                    domanda = destra.split("chiedi")[1].strip().strip('"')
                    translated.append(indenta() + f'{variabile} = input("{domanda}")')

        elif "=" in riga and "→" not in riga:
            translated.append(indenta() + riga)

        elif riga.startswith("se ") and "allora" in riga:
            condizione = riga[3:].split("allora")[0].strip()
            translated.append(indenta() + f"if {condizione}:")
            indentazione += 1

        elif riga == "altrimenti":
            indentazione -= 1
            translated.append(indenta() + "else:")
            indentazione += 1

        elif riga == "fine":
            indentazione = max(indentazione - 1, 0)

        elif riga.startswith("ripeti ") and "volte" in riga:
            numero = riga[7:].split("volte")[0].strip()
            translated.append(indenta() + f"for _ in range({numero}):")
            indentazione += 1

        elif riga.startswith("mentre "):
            condizione = riga[7:].strip()
            translated.append(indenta() + f"while {condizione}:")
            indentazione += 1

        elif riga.startswith("def "):
            nome_funzione = riga[4:].strip()
            translated.append(indenta() + f"def {nome_funzione}:")
            indentazione += 1

        elif riga.startswith("ritorna "):
            valore = riga[8:].strip()
            translated.append(indenta() + f"return {valore}")

        elif riga.startswith("usa "):
            modulo = riga[4:].strip()
            translated.append(indenta() + f"import {modulo}")

        elif riga.startswith("#") or riga.startswith("commento"):
            translated.append(indenta() + f"{riga}")

        elif "(" in riga and ")" in riga:
            translated.append(indenta() + riga)

        elif riga == "inizio":
            translated.append("# Inizio programma Pitone")

        else:
            translated.append(indenta() + f"# Comando non riconosciuto: {riga}")

    avviatore(translated, nome_programma)

def avviatore(translated, nome_programma):
    sub.run('cls')
    with open(nome_programma + '.py', 'w', encoding='utf-8') as f:
        f.write("\n".join(translated))

    sub.run(['python', nome_programma + '.py'])

def main():
    sub.run('clear')
    print(rosso(r"""
██████╗ ██╗████████╗ ██████╗ ███╗   ██╗███████╗
██╔══██╗██║╚══██╔══╝██╔═══██╗████╗  ██║██╔════╝
██████╔╝██║   ██║   ██║   ██║██╔██╗ ██║█████╗  
██╔═══╝ ██║   ██║   ██║   ██║██║╚██╗██║██╔══╝  
██║     ██║   ██║   ╚██████╔╝██║ ╚████║███████╗
╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚══════╝
"""))
    print(rosso(r"""
        Made by flawx
    """))
    tm.sleep(1)
    nome_programma = input('What name do you want the script to have?: ')
    scrivi_programma(nome_programma)

main()
