import json
import tkinter as tk
from pathlib import Path
from tkinter import ttk

ARQUIVO = Path("tarefas.json")

FUNDO = "#f3f5f9"
TEXTO = "#172033"
TEXTO_SECUNDARIO = "#687386"
AZUL = "#4263eb"
AZUL_ESCURO = "#3451c6"
BORDA = "#e4e8f0"
PRIORIDADES = ("Baixa", "Intermediária", "Alta")
PRIORIDADE_CORES = {
    "Baixa": ("#22c55e", "#166534"),
    "Intermediária": ("#facc15", "#854d0e"),
    "Alta": ("#ef4444", "#991b1b"),
}
PRIORIDADE_PADRAO = "Intermediária"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minhas tarefas")
        self.geometry("540x640")
        self.minsize(440, 540)
        self.configure(bg=FUNDO)

        self.tarefas = []
        self.selecao = None
        self.linhas_tarefas = []
        self.configurar_estilos()
        self.criar_widgets()
        self.carregar()

    def configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure(
            "TEntry",
            padding=(12, 10),
            fieldbackground="#ffffff",
            foreground=TEXTO,
            bordercolor=BORDA,
            lightcolor=BORDA,
            darkcolor=BORDA,
            insertcolor=TEXTO,
        )
        estilo.configure(
            "TCombobox",
            padding=(10, 8),
            fieldbackground="#ffffff",
            foreground=TEXTO,
            bordercolor=BORDA,
            lightcolor=BORDA,
            darkcolor=BORDA,
        )
        estilo.configure(
            "Adicionar.TButton",
            padding=(16, 10),
            background=AZUL,
            foreground="#ffffff",
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
        )
        estilo.map(
            "Adicionar.TButton",
            background=[("active", AZUL_ESCURO), ("pressed", AZUL_ESCURO)],
        )
        estilo.configure(
            "Secundario.TButton",
            padding=(12, 9),
            background="#edf0f6",
            foreground=TEXTO,
            borderwidth=0,
            font=("Segoe UI", 9, "bold"),
        )
        estilo.map(
            "Secundario.TButton",
            background=[("active", "#e1e6f0"), ("pressed", "#d8deea")],
        )
        estilo.configure(
            "Remover.TButton",
            padding=(12, 9),
            background="#fff0f0",
            foreground="#c03948",
            borderwidth=0,
            font=("Segoe UI", 9, "bold"),
        )
        estilo.map(
            "Remover.TButton",
            background=[("active", "#ffe2e3"), ("pressed", "#ffd5d7")],
        )

    def criar_widgets(self):
        principal = tk.Frame(self, bg=FUNDO, padx=28, pady=24)
        principal.pack(fill="both", expand=True)

        tk.Label(
            principal,
            text="Minhas tarefas",
            bg=FUNDO,
            fg=TEXTO,
            font=("Segoe UI", 23, "bold"),
        ).pack(anchor="w")
        tk.Label(
            principal,
            text="Organize seu dia, uma tarefa de cada vez.",
            bg=FUNDO,
            fg=TEXTO_SECUNDARIO,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(3, 20))

        tk.Label(
            principal,
            text="NOVA TAREFA",
            bg=FUNDO,
            fg=TEXTO_SECUNDARIO,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", pady=(0, 7))

        entrada_linha = tk.Frame(principal, bg=FUNDO)
        entrada_linha.pack(fill="x")
        self.entrada = ttk.Entry(entrada_linha, font=("Segoe UI", 10))
        self.entrada.pack(side="left", fill="x", expand=True)
        self.entrada.bind(
            "<Return>",
            lambda event: self.adicionar() if event.keysym == "Return" else None,
        )
        ttk.Button(
            entrada_linha,
            text="Adicionar",
            style="Adicionar.TButton",
            command=self.adicionar,
        ).pack(side="left", padx=(9, 0))
        self.entrada.focus_set()

        prioridade_linha = tk.Frame(principal, bg=FUNDO)
        prioridade_linha.pack(fill="x", pady=(9, 0))
        tk.Label(
            prioridade_linha,
            text="Prioridade",
            bg=FUNDO,
            fg=TEXTO_SECUNDARIO,
            font=("Segoe UI", 9),
        ).pack(side="left", padx=(1, 10))
        self.seletor_prioridade = ttk.Combobox(
            prioridade_linha,
            values=PRIORIDADES,
            state="readonly",
            width=15,
            font=("Segoe UI", 9),
        )
        self.seletor_prioridade.set(PRIORIDADE_PADRAO)
        self.seletor_prioridade.pack(side="left")

        resumo = tk.Frame(principal, bg=FUNDO)
        resumo.pack(fill="x", pady=(25, 10))
        tk.Label(
            resumo,
            text="Sua lista",
            bg=FUNDO,
            fg=TEXTO,
            font=("Segoe UI", 13, "bold"),
        ).pack(side="left")
        self.contador = tk.Label(
            resumo,
            text="",
            bg=FUNDO,
            fg=TEXTO_SECUNDARIO,
            font=("Segoe UI", 9),
        )
        self.contador.pack(side="right")

        legenda = tk.Frame(principal, bg=FUNDO)
        legenda.pack(fill="x", pady=(0, 9))
        for prioridade in PRIORIDADES:
            cor_prioridade, _ = PRIORIDADE_CORES[prioridade]
            item_legenda = tk.Frame(legenda, bg=FUNDO)
            item_legenda.pack(side="left", padx=(0, 12))
            tk.Frame(
                item_legenda,
                bg=cor_prioridade,
                width=13,
                height=13,
                highlightbackground="#000000",
                highlightthickness=1,
                bd=0,
            ).pack(side="left", padx=(0, 5))
            tk.Label(
                item_legenda,
                text=prioridade,
                bg=FUNDO,
                fg=TEXTO_SECUNDARIO,
                font=("Segoe UI", 8),
            ).pack(side="left")

        cartao = tk.Frame(
            principal,
            bg="#ffffff",
            highlightbackground=BORDA,
            highlightthickness=1,
        )
        cartao.pack(fill="both", expand=True)
        cartao.grid_rowconfigure(0, weight=1)
        cartao.grid_columnconfigure(0, weight=1)

        self.canvas_lista = tk.Canvas(
            cartao,
            bg="#ffffff",
            borderwidth=0,
            highlightthickness=0,
        )
        self.canvas_lista.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=8)
        self.conteudo_lista = tk.Frame(self.canvas_lista, bg="#ffffff")
        self.janela_lista = self.canvas_lista.create_window(
            (0, 0), window=self.conteudo_lista, anchor="nw"
        )
        self.conteudo_lista.bind("<Configure>", self._atualizar_area_rolagem)
        self.canvas_lista.bind("<Configure>", self._ajustar_largura_lista)
        self.canvas_lista.bind_all("<MouseWheel>", self._rolar_lista)

        rolagem = ttk.Scrollbar(
            cartao, orient="vertical", command=self.canvas_lista.yview
        )
        rolagem.grid(row=0, column=1, sticky="ns", pady=5, padx=(0, 5))
        self.canvas_lista.configure(yscrollcommand=rolagem.set)

        self.vazio = tk.Label(
            cartao,
            text="Tudo tranquilo por aqui.\nAdicione uma tarefa para começar!",
            bg="#ffffff",
            fg=TEXTO_SECUNDARIO,
            font=("Segoe UI", 10),
            justify="center",
        )
        self.vazio.place(relx=0.5, rely=0.5, anchor="center")

        acoes = tk.Frame(principal, bg=FUNDO)
        acoes.pack(fill="x", pady=(14, 0))
        ttk.Button(
            acoes,
            text="Concluir / desfazer",
            style="Secundario.TButton",
            command=self.alternar,
        ).pack(side="left")
        ttk.Button(
            acoes,
            text="Remover",
            style="Remover.TButton",
            command=self.remover,
        ).pack(side="right")

    def indice_selecionado(self):
        return self.selecao

    def _atualizar_area_rolagem(self, event):
        if event.widget is self.conteudo_lista:
            self.canvas_lista.configure(scrollregion=self.canvas_lista.bbox("all"))

    def _ajustar_largura_lista(self, event):
        self.canvas_lista.itemconfigure(self.janela_lista, width=event.width)

    def _rolar_lista(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        while widget is not None:
            if widget is self.canvas_lista:
                self.canvas_lista.yview_scroll(int(-event.delta / 120), "units")
                return
            widget = widget.master

    def alternar(self):
        indice = self.indice_selecionado()
        if indice is None:
            return
        self.tarefas[indice]["feita"] = not self.tarefas[indice]["feita"]
        self.salvar()
        self.atualizar_lista()
        if indice < len(self.linhas_tarefas):
            self.linhas_tarefas[indice].focus_set()

    def _selecionar_tarefa(self, indice, widget=None):
        self.selecao = indice
        for posicao, linha in enumerate(self.linhas_tarefas):
            cor_fundo = "#e9edff" if posicao == indice else "#ffffff"
            linha.configure(bg=cor_fundo)
            for widget in linha.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=cor_fundo)
        if widget is not None and widget in self.linhas_tarefas:
            widget.focus_set()
        else:
            self.linhas_tarefas[indice].focus_set()

    def _concluir_tarefa(self, indice, event):
        self._selecionar_tarefa(indice, event.widget.master)
        self.alternar()

    def _tecla_espaco(self, indice, event):
        if event.keysym == "space":
            self._selecionar_tarefa(indice)
            self.alternar()
        return "break"

    def adicionar(self):
        texto = self.entrada.get().strip()
        if not texto:
            self.entrada.focus_set()
            return
        self.tarefas.append(
            {
                "texto": texto,
                "feita": False,
                "prioridade": self.seletor_prioridade.get(),
            }
        )
        self.entrada.delete(0, "end")
        self.salvar()
        self.atualizar_lista()
        self.entrada.focus_set()

    def remover(self):
        indice = self.indice_selecionado()
        if indice is None:
            return
        del self.tarefas[indice]
        self.selecao = None
        self.salvar()
        self.atualizar_lista()

    def atualizar_lista(self):
        for linha in self.linhas_tarefas:
            linha.destroy()
        self.linhas_tarefas = []

        for indice, tarefa in enumerate(self.tarefas):
            cor_prioridade = PRIORIDADE_CORES.get(
                tarefa.get("prioridade", PRIORIDADE_PADRAO),
                PRIORIDADE_CORES[PRIORIDADE_PADRAO],
            )[0]
            fundo = "#e9edff" if indice == self.selecao else "#ffffff"
            linha = tk.Frame(
                self.conteudo_lista,
                bg=fundo,
                padx=12,
                pady=11,
                takefocus=True,
                highlightthickness=0,
            )
            linha.pack(fill="x", padx=(0, 5), pady=2)
            marca = "✔" if tarefa["feita"] else "○"
            cor_tarefa = "#8992a3" if tarefa["feita"] else TEXTO
            tk.Label(
                linha,
                text=marca,
                bg=fundo,
                fg="#8992a3" if tarefa["feita"] else AZUL,
                font=("Segoe UI", 11, "bold"),
            ).pack(side="left", padx=(0, 10))
            tk.Label(
                linha,
                text=tarefa["texto"],
                bg=fundo,
                fg=cor_tarefa,
                font=("Segoe UI", 10),
                anchor="w",
            ).pack(side="left", fill="x", expand=True)
            tk.Frame(
                linha,
                bg=cor_prioridade,
                width=13,
                height=13,
                takefocus=False,
                highlightbackground="#000000",
                highlightthickness=1,
                bd=0,
            ).pack(side="right", padx=(10, 2))
            linha.bind(
                "<Button-1>",
                lambda event, i=indice: self._selecionar_tarefa(i, event.widget),
            )
            linha.bind(
                "<Double-Button-1>",
                lambda event, i=indice: self._concluir_tarefa(i, event),
            )
            linha.bind(
                "<space>",
                lambda event, i=indice: self._tecla_espaco(i, event),
            )
            for widget in linha.winfo_children():
                widget.bind(
                    "<Button-1>",
                    lambda event, i=indice: self._selecionar_tarefa(
                        i, event.widget.master
                    ),
                )
                widget.bind(
                    "<Double-Button-1>",
                    lambda event, i=indice: self._concluir_tarefa(i, event),
                )
            self.linhas_tarefas.append(linha)

        pendentes = sum(not tarefa["feita"] for tarefa in self.tarefas)
        concluidas = len(self.tarefas) - pendentes
        self.contador.config(
            text=f"{pendentes} pendente(s)  ·  {concluidas} concluída(s)"
        )
        if self.tarefas:
            self.vazio.place_forget()
        else:
            self.selecao = None
            self.vazio.place(relx=0.5, rely=0.5, anchor="center")

    def salvar(self):
        ARQUIVO.write_text(
            json.dumps(self.tarefas, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def carregar(self):
        if ARQUIVO.exists():
            self.tarefas = json.loads(ARQUIVO.read_text(encoding="utf-8"))
        for tarefa in self.tarefas:
            if tarefa.get("prioridade") not in PRIORIDADE_CORES:
                tarefa["prioridade"] = PRIORIDADE_PADRAO
        self.atualizar_lista()


if __name__ == "__main__":
    App().mainloop()