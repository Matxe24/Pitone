import sys
import os
import subprocess as sub

def compilatore(testo_completo, nome_programma):
    #compilatore
    translated = [] 
    righe = testo_completo.splitlines()
    indentazione = 0

    for riga in righe:
        riga = riga.strip()
        if riga == "":
            continue  # ignora righe vuote

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
                    domanda = destra.split("chiedi", 1)[1].strip()
                    # Rimuove eventuali virgolette esterne
                    if domanda.startswith('"') and domanda.endswith('"'):
                        domanda = domanda[1:-1]
                    translated.append(indenta() + f'{variabile} = input("{domanda}")')


        elif "=" in riga and "→" not in riga and not riga.startswith("se "):
            translated.append(indenta() + riga)


        elif riga.startswith("se ") and "allora" in riga:
            condizione = riga[3:].split("allora")[0].strip()

        # Se c'è un singolo = e non è già un ==
            if "=" in condizione and "==" not in condizione:
                condizione = condizione.replace("=", "==")

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
            print("Invalid command\n exiting...")
            exit()

    return "\n".join(translated)

def main():
    if len(sys.argv) != 2:
        print("❌ Uso corretto: python3 pitonec.py nomefile.pi")
        sys.exit(1)

    file_pi = sys.argv[1]
    if not file_pi.endswith(".pi"):
        print("❌ Errore: il file deve avere estensione .pi")
        sys.exit(1)

    try:
        with open(file_pi, "r", encoding="utf-8") as f:
            contenuto = f.read()
    except FileNotFoundError:
        print(f"❌ Errore: file '{file_pi}' non trovato.")
        sys.exit(1)

    nome_output = os.path.splitext(file_pi)[0] + ".py"
    codice_python = compilatore(contenuto, nome_output)

    with open(nome_output, "w", encoding="utf-8") as f_out:
        f_out.write(codice_python)

    print(f"✅ Compilazione completata: '{nome_output}' generato.")
    avvia = input("Avviare?(Y/n): ")
    if avvia == "Y" or avvia == "y" or avvia == "":
        sub.run(['python3', nome_output])
    else:
        exit()

if __name__ == "__main__":
    main()
