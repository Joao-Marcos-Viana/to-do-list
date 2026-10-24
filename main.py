import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

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
ALTURA_LINHA_TAREFA = 52
MIN_TAREFAS_VISIVEIS = 3
MAX_TAREFAS_VISIVEIS = 5
TEMAS = {
    "claro": {
        "fundo": "#f3f5f9",
        "superficie": "#ffffff",
        "texto": "#172033",
        "secundario": "#687386",
        "borda": "#e4e8f0",
        "selecao": "#e9edff",
        "foco": "#72a7ff",
        "entrada": "#ffffff",
        "botao": "#edf0f6",
        "trilho": "#ffffff",
        "puxador": "#cbd2df",
    },
    "escuro": {
        "fundo": "#171b26",
        "superficie": "#222837",
        "texto": "#edf1fa",
        "secundario": "#aab4c6",
        "borda": "#343d50",
        "selecao": "#303c58",
        "foco": "#9cc2ff",
        "entrada": "#222837",
        "botao": "#30384a",
        "trilho": "#222837",
        "puxador": "#56627a",
    },
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minhas tarefas")
        self.geometry("540x520")
        self.minsize(440, 400)
        self.configure(bg=FUNDO)

        self.tarefas = []
        self.selecao = None
        self.linhas_tarefas = []
        self.rolar_ao_atualizar = False
        self.editando = None
        self.tema = "claro"
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
            borderwidth=1,
        )
        estilo.map(
            "TEntry",
            bordercolor=[("focus", TEMAS[self.tema]["foco"])],
            lightcolor=[("focus", TEMAS[self.tema]["foco"])],
            darkcolor=[("focus", TEMAS[self.tema]["foco"])],
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
        estilo.map(
            "TCombobox",
            bordercolor=[("focus", TEMAS[self.tema]["foco"])],
            lightcolor=[("focus", TEMAS[self.tema]["foco"])],
            darkcolor=[("focus", TEMAS[self.tema]["foco"])],
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
            bordercolor=[("focus", TEMAS[self.tema]["foco"])],
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
            bordercolor=[("focus", TEMAS[self.tema]["foco"])],
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
            bordercolor=[("focus", TEMAS[self.tema]["foco"])],
        )
        estilo.configure(
            "Mini.TButton",
            padding=(7, 4),
            background="#edf0f6",
            foreground=TEXTO,
            borderwidth=1,
            font=("Segoe UI", 8, "bold"),
        )
        estilo.map(
            "Mini.TButton",
            background=[("active", "#e1e6f0"), ("pressed", "#d8deea")],
            bordercolor=[("focus", TEMAS[self.tema]["foco"])],
        )
        estilo.configure(
            "Minimal.Vertical.TScrollbar",
            width=7,
            arrowsize=0,
            background="#cbd2df",
            troughcolor="#ffffff",
            bordercolor="#ffffff",
            lightcolor="#ffffff",
            darkcolor="#ffffff",
            relief="flat",
        )
        estilo.map(
            "Minimal.Vertical.TScrollbar",
            background=[("active", "#9aa6ba")],
        )

    def criar_widgets(self):
        self.principal = tk.Frame(self, bg=FUNDO, padx=28, pady=24)
        principal = self.principal
        principal.pack(fill="x")

        cabecalho = tk.Frame(principal, bg=FUNDO)
        cabecalho.pack(fill="x", pady=(0, 10))
        self.botao_ajuda = tk.Canvas(
            cabecalho,
            width=32,
            height=32,
            bg=FUNDO,
            highlightthickness=0,
            takefocus=1,
        )
        self.botao_ajuda.pack(side="left")
        self.item_circulo_ajuda = self.botao_ajuda.create_oval(
            3, 3, 29, 29, outline=TEXTO_SECUNDARIO, width=1.5
        )
        self.item_texto_ajuda = self.botao_ajuda.create_text(
            16, 16, text="?", fill=TEXTO, font=("Segoe UI", 12, "bold")
        )
        self.botao_ajuda.bind(
            "<Enter>", lambda event: event.widget.configure(cursor="hand2")
        )
        self.botao_ajuda.bind(
            "<Leave>", lambda event: event.widget.configure(cursor="")
        )
        self.botao_ajuda.bind("<Button-1>", self._abrir_atalhos_por_evento)
        self.botao_ajuda.bind("<Return>", self._abrir_atalhos_por_evento)
        self.botao_ajuda.bind("<space>", self._abrir_atalhos_por_evento)
        self.botao_ajuda.bind("<FocusIn>", self._foco_entrou_canvas)
        self.botao_ajuda.bind("<FocusOut>", self._foco_saiu_canvas)
        self.botao_tema = ttk.Button(
            cabecalho,
            text="Modo escuro",
            style="Secundario.TButton",
            command=self.alternar_tema,
            takefocus=True,
        )
        self.botao_tema.pack(side="right")
        self._tornar_acessivel(self.botao_tema)

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

        self.rotulo_formulario = tk.Label(
            principal,
            text="NOVA TAREFA",
            bg=FUNDO,
            fg=TEXTO_SECUNDARIO,
            font=("Segoe UI", 8, "bold"),
        )
        self.rotulo_formulario.pack(anchor="w", pady=(0, 7))

        entrada_linha = tk.Frame(principal, bg=FUNDO)
        entrada_linha.pack(fill="x")
        self.entrada = ttk.Entry(entrada_linha, font=("Segoe UI", 10))
        self.entrada.pack(side="left", fill="x", expand=True)
        self.entrada.bind(
            "<Return>",
            lambda event: self.adicionar() if event.keysym == "Return" else None,
        )
        self.entrada.bind("<Escape>", self._escapar_edicao)
        self.botao_salvar = ttk.Button(
            entrada_linha,
            text="Adicionar",
            style="Adicionar.TButton",
            command=self.adicionar,
            takefocus=True,
        )
        self.botao_salvar.pack(side="left", padx=(9, 0))
        self._tornar_acessivel(self.entrada)
        self._tornar_acessivel(self.botao_salvar)
        self.botao_cancelar = ttk.Button(
            entrada_linha,
            text="Cancelar",
            style="Secundario.TButton",
            command=self.cancelar_edicao,
            takefocus=True,
        )
        self._tornar_acessivel(self.botao_cancelar)
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
        self._tornar_acessivel(self.seletor_prioridade)
        self.bind_all("<Control-Up>", self._aumentar_prioridade)
        self.bind_all("<Control-Down>", self._diminuir_prioridade)

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
        cartao.grid_columnconfigure(0, weight=1)

        self.canvas_lista = tk.Canvas(
            cartao,
            bg="#ffffff",
            borderwidth=0,
            highlightthickness=0,
        )
        self.canvas_lista.grid(row=0, column=0, sticky="ew", padx=(10, 0), pady=8)
        self.conteudo_lista = tk.Frame(self.canvas_lista, bg="#ffffff")
        self.janela_lista = self.canvas_lista.create_window(
            (0, 0), window=self.conteudo_lista, anchor="nw"
        )
        self.conteudo_lista.bind("<Configure>", self._atualizar_area_rolagem)
        self.canvas_lista.bind("<Configure>", self._ajustar_largura_lista)
        self.canvas_lista.bind_all("<MouseWheel>", self._rolar_lista)

        rolagem = ttk.Scrollbar(
            cartao,
            orient="vertical",
            command=self.canvas_lista.yview,
            style="Minimal.Vertical.TScrollbar",
        )
        rolagem.grid(row=0, column=1, sticky="ns", pady=5, padx=(0, 5))
        self.canvas_lista.configure(yscrollcommand=rolagem.set)
        self.rolagem = rolagem
        self.menu_tarefa = tk.Menu(
            self,
            tearoff=False,
            bg="#ffffff",
            fg=TEXTO,
            activebackground="#fff0f0",
            activeforeground="#c03948",
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 9),
        )
        self.menu_tarefa.add_command(
            label="Editar tarefa",
            command=lambda: self.editar_tarefa(self.indice_selecionado()),
        )
        self.menu_tarefa.add_command(
            label="Apagar tarefa",
            command=lambda: self.remover_tarefa(
                self.indice_selecionado(), confirmar=True
            ),
        )

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
        botao_concluir = ttk.Button(
            acoes,
            text="Concluir / desfazer",
            style="Secundario.TButton",
            command=self.alternar,
            takefocus=True,
        )
        botao_concluir.pack(side="left")
        self._tornar_acessivel(botao_concluir)
        botao_remover = ttk.Button(
            acoes,
            text="Remover",
            style="Remover.TButton",
            command=self.remover,
            takefocus=True,
        )
        botao_remover.pack(side="right")
        self._tornar_acessivel(botao_remover)

    def indice_selecionado(self):
        return self.selecao

    def _abrir_atalhos_por_evento(self, event):
        event.widget.focus_set()
        self.mostrar_atalhos()
        return "break"

    def _foco_entrou_canvas(self, event):
        event.widget.configure(
            highlightthickness=2,
            highlightbackground=TEMAS[self.tema]["foco"],
        )

    def _foco_saiu_canvas(self, event):
        event.widget.configure(highlightthickness=0)

    def _escapar_edicao(self, event):
        if event.keysym == "Escape":
            self.cancelar_edicao()
            return "break"

    def mostrar_atalhos(self):
        guia = tk.Toplevel(self)
        guia.title("Guia de atalhos")
        guia.transient(self)
        guia.resizable(False, False)
        cores = TEMAS[self.tema]
        guia.configure(bg=cores["fundo"])
        conteudo = tk.Frame(guia, bg=cores["fundo"], padx=24, pady=20)
        conteudo.pack(fill="both", expand=True)
        tk.Label(
            conteudo,
            text="Ajuda e atalhos",
            bg=cores["fundo"],
            fg=cores["texto"],
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w", pady=(0, 12))
        atalhos = (
            ("Tab / Shift + Tab", "Navegar entre os campos e controles."),
            ("Enter no campo da tarefa", "Adicionar ou salvar a edição."),
            ("Duplo clique na tarefa", "Concluir ou reabrir a tarefa."),
            ("Botão direito", "Abrir as opções de editar e apagar (com confirmação)."),
            ("Botão Editar", "Abrir a tarefa no formulário para alterar nome/prioridade."),
            ("Ctrl + botão direito", "Editar a tarefa clicada."),
            ("Shift + botão direito", "Apagar a tarefa sem confirmação."),
            ("Ctrl + ↑ / Ctrl + ↓", "Aumentar / diminuir a prioridade selecionada."),
            ("Barra de espaço", "Concluir ou reabrir a tarefa selecionada."),
        )
        for atalho, descricao in atalhos:
            linha = tk.Frame(conteudo, bg=cores["fundo"])
            linha.pack(fill="x", pady=3)
            tk.Label(
                linha,
                text=atalho,
                width=24,
                anchor="w",
                bg=cores["fundo"],
                fg=cores["texto"],
                font=("Segoe UI", 9, "bold"),
            ).pack(side="left")
            tk.Label(
                linha,
                text=descricao,
                anchor="w",
                bg=cores["fundo"],
                fg=cores["secundario"],
                font=("Segoe UI", 9),
            ).pack(side="left")
        botao_fechar = ttk.Button(
            conteudo,
            text="Fechar",
            style="Secundario.TButton",
            command=guia.destroy,
        )
        botao_fechar.pack(anchor="e", pady=(14, 0))
        self._tornar_acessivel(botao_fechar)
        botao_fechar.focus_set()
        guia.bind("<Escape>", lambda event: event.widget.destroy())
        guia.after_idle(lambda: self._centralizar_janela(guia))

    def _centralizar_janela(self, janela):
        janela.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - janela.winfo_width()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - janela.winfo_height()) // 2
        janela.geometry(f"+{x}+{y}")

    def _tornar_acessivel(self, widget):
        widget.bind("<FocusIn>", self._foco_entrou, add="+")
        widget.bind("<FocusOut>", self._foco_saiu, add="+")

    def _foco_entrou(self, event):
        recipiente = event.widget.master
        if isinstance(recipiente, tk.Frame):
            cor_foco = TEMAS[self.tema]["foco"]
            recipiente.configure(
                highlightthickness=2,
                highlightbackground=cor_foco,
                highlightcolor=cor_foco,
            )

    def _foco_saiu(self, event):
        recipiente = event.widget.master
        if isinstance(recipiente, tk.Frame):
            self.after_idle(lambda: self._limpar_foco_se_inativo(recipiente))

    def _foco_linha_entrou(self, event):
        cor_foco = TEMAS[self.tema]["foco"]
        event.widget.configure(
            highlightthickness=2,
            highlightbackground=cor_foco,
            highlightcolor=cor_foco,
        )

    def _foco_linha_saiu(self, event):
        linha = event.widget
        self.after_idle(lambda: self._limpar_foco_se_inativo(linha))

    def _limpar_foco_se_inativo(self, recipiente):
        foco = self.focus_get()
        while foco is not None:
            if foco is recipiente:
                return
            foco = getattr(foco, "master", None)
        try:
            recipiente.configure(highlightthickness=0)
        except tk.TclError:
            pass

    def _aumentar_prioridade(self, event):
        return self._alterar_prioridade_pelo_evento(event, 1)

    def _diminuir_prioridade(self, event):
        return self._alterar_prioridade_pelo_evento(event, -1)

    def _alterar_prioridade_pelo_evento(self, event, direcao):
        indice = self._indice_da_tarefa_em(event.widget)
        if indice is None:
            return None
        self.selecao = indice
        atual = self.tarefas[indice].get("prioridade", PRIORIDADE_PADRAO)
        posicao = PRIORIDADES.index(atual) if atual in PRIORIDADES else 1
        nova_posicao = max(0, min(len(PRIORIDADES) - 1, posicao + direcao))
        if nova_posicao != posicao:
            self.tarefas[indice]["prioridade"] = PRIORIDADES[nova_posicao]
            self.salvar()
            self.atualizar_lista()
            if indice < len(self.linhas_tarefas):
                self.linhas_tarefas[indice].focus_set()
        return "break"

    def _indice_da_tarefa_em(self, widget):
        while widget is not None:
            for indice, linha in enumerate(self.linhas_tarefas):
                if widget is linha:
                    return indice
            widget = getattr(widget, "master", None)
        return None

    def alternar_tema(self):
        anterior = TEMAS[self.tema]
        self.tema = "escuro" if self.tema == "claro" else "claro"
        atual = TEMAS[self.tema]
        self._aplicar_tema_widget(self, anterior, atual)
        self._atualizar_estilos_tema()
        self.configure(bg=atual["fundo"])
        self.botao_tema.configure(
            text="Modo claro" if self.tema == "escuro" else "Modo escuro"
        )
        self.botao_ajuda.configure(bg=atual["fundo"])
        self.botao_ajuda.itemconfigure(self.item_texto_ajuda, fill=atual["texto"])
        self.botao_ajuda.itemconfigure(
            self.item_circulo_ajuda, outline=atual["secundario"]
        )
        self.menu_tarefa.configure(
            bg=atual["superficie"],
            fg=atual["texto"],
            activebackground=atual["selecao"],
            activeforeground=atual["texto"],
        )
        self.atualizar_lista()
        self.update_idletasks()

    def _aplicar_tema_widget(self, widget, anterior, atual):
        substituicoes = {
            anterior["fundo"]: atual["fundo"],
            anterior["superficie"]: atual["superficie"],
            anterior["texto"]: atual["texto"],
            anterior["secundario"]: atual["secundario"],
            anterior["borda"]: atual["borda"],
            anterior["selecao"]: atual["selecao"],
            anterior["entrada"]: atual["entrada"],
            anterior["botao"]: atual["botao"],
            anterior["trilho"]: atual["trilho"],
        }
        if isinstance(widget, (tk.Frame, tk.Label, tk.Canvas, tk.Menu)):
            try:
                bg = str(widget.cget("bg"))
                if bg in substituicoes:
                    widget.configure(bg=substituicoes[bg])
            except tk.TclError:
                pass
        if isinstance(widget, tk.Frame):
            try:
                espessura = int(widget.cget("highlightthickness"))
                if espessura == 1:
                    widget.configure(highlightbackground=atual["borda"])
                elif espessura > 1:
                    widget.configure(
                        highlightbackground=atual["foco"],
                        highlightcolor=atual["foco"],
                    )
            except tk.TclError:
                pass
        if isinstance(widget, tk.Label):
            try:
                fg = str(widget.cget("fg"))
                if fg in substituicoes:
                    widget.configure(fg=substituicoes[fg])
                elif fg == "#8992a3":
                    widget.configure(fg="#b0bacb" if self.tema == "escuro" else "#8992a3")
            except tk.TclError:
                pass
        for filho in widget.winfo_children():
            self._aplicar_tema_widget(filho, anterior, atual)

    def _atualizar_estilos_tema(self):
        cores = TEMAS[self.tema]
        estilo = ttk.Style(self)
        estilo.configure(
            "TEntry",
            fieldbackground=cores["entrada"],
            foreground=cores["texto"],
            bordercolor=cores["borda"],
            lightcolor=cores["borda"],
            darkcolor=cores["borda"],
            insertcolor=cores["texto"],
        )
        estilo.map(
            "TEntry",
            bordercolor=[("focus", cores["foco"])],
            lightcolor=[("focus", cores["foco"])],
            darkcolor=[("focus", cores["foco"])],
        )
        estilo.map(
            "Adicionar.TButton",
            background=[("active", AZUL_ESCURO), ("pressed", AZUL_ESCURO)],
            bordercolor=[("focus", cores["foco"])],
        )
        estilo.configure(
            "TCombobox",
            fieldbackground=cores["entrada"],
            foreground=cores["texto"],
            bordercolor=cores["borda"],
            lightcolor=cores["borda"],
            darkcolor=cores["borda"],
        )
        estilo.map(
            "TCombobox",
            bordercolor=[("focus", cores["foco"])],
            lightcolor=[("focus", cores["foco"])],
            darkcolor=[("focus", cores["foco"])],
        )
        estilo.configure(
            "Secundario.TButton",
            background=cores["botao"],
            foreground=cores["texto"],
        )
        estilo.map(
            "Secundario.TButton",
            background=[
                ("active", cores["selecao"]),
                ("pressed", cores["borda"]),
            ],
            bordercolor=[("focus", cores["foco"])],
        )
        estilo.configure(
            "Mini.TButton",
            background=cores["botao"],
            foreground=cores["texto"],
        )
        estilo.map(
            "Mini.TButton",
            background=[
                ("active", cores["selecao"]),
                ("pressed", cores["borda"]),
            ],
            bordercolor=[("focus", cores["foco"])],
        )
        estilo.configure(
            "Remover.TButton",
            background="#3b2830" if self.tema == "escuro" else "#fff0f0",
            foreground="#ff9eaa" if self.tema == "escuro" else "#c03948",
        )
        estilo.map(
            "Remover.TButton",
            background=[
                ("active", "#523440" if self.tema == "escuro" else "#ffe2e3"),
                ("pressed", "#63404c" if self.tema == "escuro" else "#ffd5d7"),
            ],
            bordercolor=[("focus", cores["foco"])],
        )
        estilo.configure(
            "Minimal.Vertical.TScrollbar",
            background=cores["puxador"],
            troughcolor=cores["trilho"],
            bordercolor=cores["trilho"],
            lightcolor=cores["trilho"],
            darkcolor=cores["trilho"],
        )

    def editar_tarefa(self, indice):
        if indice is None or not 0 <= indice < len(self.tarefas):
            return
        tarefa = self.tarefas[indice]
        self.editando = indice
        self.entrada.delete(0, "end")
        self.entrada.insert(0, tarefa["texto"])
        self.seletor_prioridade.set(
            tarefa.get("prioridade", PRIORIDADE_PADRAO)
        )
        self.botao_salvar.configure(text="Salvar edição")
        self.botao_cancelar.pack(side="left", padx=(6, 0))
        self._selecionar_tarefa(indice)
        self.entrada.focus_set()
        self.entrada.selection_range(0, "end")
        self.rotulo_formulario.configure(text="EDITANDO TAREFA")

    def cancelar_edicao(self):
        self.editando = None
        self.entrada.delete(0, "end")
        self.seletor_prioridade.set(PRIORIDADE_PADRAO)
        self.botao_salvar.configure(text="Adicionar")
        self.botao_cancelar.pack_forget()
        self.rotulo_formulario.configure(text="NOVA TAREFA")
        self.entrada.focus_set()

    def _atualizar_area_rolagem(self, event):
        if event.widget is self.conteudo_lista:
            self.canvas_lista.configure(scrollregion=self.canvas_lista.bbox("all"))
            if self.rolar_ao_atualizar:
                self.after_idle(
                    lambda: self.after_idle(self._rolar_para_ultima)
                )

    def _ajustar_largura_lista(self, event):
        self.canvas_lista.itemconfigure(self.janela_lista, width=event.width)

    def _ajustar_altura_janela(self):
        self.update_idletasks()
        altura = max(self.minsize()[1], self.principal.winfo_reqheight() + 2)
        largura = max(self.winfo_width(), 440)
        self.geometry(f"{largura}x{altura}")

    def _rolar_para_ultima(self):
        if self.rolar_ao_atualizar and self.tarefas:
            self.canvas_lista.yview_moveto(1.0)
            self.rolar_ao_atualizar = False

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
        cores = TEMAS[self.tema]
        for posicao, linha in enumerate(self.linhas_tarefas):
            cor_fundo = (
                cores["selecao"] if posicao == indice else cores["superficie"]
            )
            linha.configure(bg=cor_fundo)
            for filho in linha.winfo_children():
                if isinstance(filho, tk.Label):
                    filho.configure(bg=cor_fundo)
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
        tarefa = {
            "texto": texto,
            "prioridade": self.seletor_prioridade.get(),
        }
        if self.editando is None:
            tarefa["feita"] = False
            self.tarefas.append(tarefa)
            rolar_para_ultima = True
        else:
            tarefa["feita"] = self.tarefas[self.editando]["feita"]
            self.tarefas[self.editando] = tarefa
            self.selecao = self.editando
            rolar_para_ultima = False
        self.editando = None
        self.entrada.delete(0, "end")
        self.seletor_prioridade.set(PRIORIDADE_PADRAO)
        self.botao_salvar.configure(text="Adicionar")
        self.botao_cancelar.pack_forget()
        self.rotulo_formulario.configure(text="NOVA TAREFA")
        self.salvar()
        self.atualizar_lista(rolar_para_ultima=rolar_para_ultima)
        self.entrada.focus_set()

    def remover(self):
        indice = self.indice_selecionado()
        self.remover_tarefa(indice)

    def remover_tarefa(self, indice, confirmar=False):
        if indice is None:
            return
        if not 0 <= indice < len(self.tarefas):
            return
        if confirmar and not messagebox.askyesno(
            "Apagar tarefa",
            f'Deseja apagar "{self.tarefas[indice]["texto"]}"?',
            parent=self,
        ):
            return
        del self.tarefas[indice]
        if self.editando == indice:
            self.cancelar_edicao()
        elif self.editando is not None and self.editando > indice:
            self.editando -= 1
        self.selecao = None
        self.salvar()
        self.atualizar_lista()

    def _menu_contexto_tarefa(self, event, indice):
        self._selecionar_tarefa(indice, self.linhas_tarefas[indice])
        try:
            self.menu_tarefa.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu_tarefa.grab_release()

    def _clique_direito_tarefa(self, event, indice):
        self._selecionar_tarefa(indice, self.linhas_tarefas[indice])
        if event.state & 0x4:
            self.editar_tarefa(indice)
        elif event.state & 0x1:
            self.remover_tarefa(indice, confirmar=False)
        else:
            self._menu_contexto_tarefa(event, indice)
        return "break"

    def atualizar_lista(self, rolar_para_ultima=False):
        cores_tema = TEMAS[self.tema]
        self.rolar_ao_atualizar = rolar_para_ultima
        for linha in self.linhas_tarefas:
            linha.destroy()
        self.linhas_tarefas = []

        for indice, tarefa in enumerate(self.tarefas):
            cor_prioridade = PRIORIDADE_CORES.get(
                tarefa.get("prioridade", PRIORIDADE_PADRAO),
                PRIORIDADE_CORES[PRIORIDADE_PADRAO],
            )[0]
            fundo = (
                cores_tema["selecao"]
                if indice == self.selecao
                else cores_tema["superficie"]
            )
            linha = tk.Frame(
                self.conteudo_lista,
                bg=fundo,
                padx=12,
                pady=11,
                takefocus=True,
                highlightthickness=0,
            )
            linha.pack(fill="x", padx=(0, 5), pady=2)
            linha.bind("<FocusIn>", self._foco_linha_entrou)
            linha.bind("<FocusOut>", self._foco_linha_saiu)
            marca = "✔" if tarefa["feita"] else "○"
            cor_tarefa = (
                "#b0bacb" if tarefa["feita"] and self.tema == "escuro"
                else "#8992a3" if tarefa["feita"]
                else cores_tema["texto"]
            )
            tk.Label(
                linha,
                text=marca,
                bg=fundo,
                fg=cor_tarefa if tarefa["feita"] else AZUL,
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
            indicador = tk.Frame(
                linha,
                bg=cor_prioridade,
                width=13,
                height=13,
                takefocus=False,
                highlightbackground="#000000",
                highlightthickness=1,
                bd=0,
            )
            indicador.pack(side="right", padx=(10, 2))
            botao_editar = ttk.Button(
                linha,
                text="⋮",
                style="Mini.TButton",
                command=lambda i=indice: self.editar_tarefa(i),
                takefocus=True,
            )
            botao_editar.pack(side="right", padx=(4, 0))
            self._tornar_acessivel(botao_editar)
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
                if widget is not botao_editar:
                    widget.bind(
                        "<Double-Button-1>",
                        lambda event, i=indice: self._concluir_tarefa(i, event),
                    )
                widget.bind(
                    "<Button-3>",
                    lambda event, i=indice: self._clique_direito_tarefa(event, i),
                )
            linha.bind(
                "<Button-3>",
                lambda event, i=indice: self._clique_direito_tarefa(event, i),
            )
            self.linhas_tarefas.append(linha)

        tarefas_visiveis = min(
            max(len(self.tarefas), MIN_TAREFAS_VISIVEIS),
            MAX_TAREFAS_VISIVEIS,
        )
        self.canvas_lista.configure(height=tarefas_visiveis * ALTURA_LINHA_TAREFA)
        if len(self.tarefas) > MAX_TAREFAS_VISIVEIS:
            self.rolagem.grid()
        else:
            self.rolagem.grid_remove()

        def finalizar_atualizacao():
            self.canvas_lista.configure(
                scrollregion=self.canvas_lista.bbox("all")
            )
            self._ajustar_altura_janela()
            if rolar_para_ultima and self.tarefas:
                self.after_idle(lambda: self.after_idle(self._rolar_para_ultima))

        self.after_idle(finalizar_atualizacao)

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