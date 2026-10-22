import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path

ARQUIVO = Path("tarefas.json")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minhas Tarefas")
        self.geometry("400x500")
        self.tarefas = []
        self.criar_widgets()
        self.carregar()

    # ---------- interface ----------
    def criar_widgets(self):
        topo = ttk.Frame(self, padding=10)
        topo.pack(fill="x")

        self.entrada = ttk.Entry(topo)
        self.entrada.pack(side="left", fill="x", expand=True)
        self.entrada.bind("<Return>", lambda e: self.adicionar())
        self.entrada.focus()

        ttk.Button(topo, text="Adicionar", command=self.adicionar).pack(
            side="left", padx=(5, 0)
        )

        self.lista = tk.Listbox(self, activestyle="none", font=("Segoe UI", 11))
        self.lista.pack(fill="both", expand=True, padx=10)
        self.lista.bind("<Double-Button-1>", lambda e: self.alternar())

        baixo = ttk.Frame(self, padding=10)
        baixo.pack(fill="x")
        ttk.Button(baixo, text="Concluir / Desfazer", command=self.alternar).pack(side="left")
        ttk.Button(baixo, text="Remover", command=self.remover).pack(side="right")

    # ---------- lógica ----------
    def indice_selecionado(self):
        sel = self.lista.curselection()
        return sel[0] if sel else None

    def adicionar(self):
        texto = self.entrada.get().strip()
        if not texto:
            return
        self.tarefas.append({"texto": texto, "feita": False})
        self.entrada.delete(0, "end")
        self.salvar()
        self.atualizar_lista()

    def alternar(self):
        i = self.indice_selecionado()
        if i is None:
            return
        self.tarefas[i]["feita"] = not self.tarefas[i]["feita"]
        self.salvar()
        self.atualizar_lista()
        self.lista.selection_set(i)

    def remover(self):
        i = self.indice_selecionado()
        if i is None:
            return
        del self.tarefas[i]
        self.salvar()
        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista.delete(0, "end")
        for i, t in enumerate(self.tarefas):
            marca = "✔" if t["feita"] else "☐"
            self.lista.insert("end", f"{marca}  {t['texto']}")
            if t["feita"]:
                self.lista.itemconfig(i, fg="gray")

    # ---------- persistência ----------
    def salvar(self):
        ARQUIVO.write_text(
            json.dumps(self.tarefas, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def carregar(self):
        if ARQUIVO.exists():
            self.tarefas = json.loads(ARQUIVO.read_text(encoding="utf-8"))
            self.atualizar_lista()


if __name__ == "__main__":
    App().mainloop()