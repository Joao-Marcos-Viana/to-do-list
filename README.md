# Minhas tarefas | To-do List

<p align="center">
  <a href="#português-br">Português</a> |
  <a href="#english">English</a>
</p>

---

## Português (Brasil)

Aplicativo desktop de lista de tarefas, desenvolvido em Python com Tkinter. Organize atividades, defina prioridades, acompanhe o que já foi concluído e navegue pela interface usando mouse ou teclado.

### Recursos

- Adicionar, editar, concluir, reabrir e remover tarefas.
- Definir prioridade **Baixa**, **Intermediária** ou **Alta**, identificada por um indicador colorido:
  - Verde: baixa.
  - Amarelo: intermediária.
  - Vermelho: alta.
- Visualizar a quantidade de tarefas pendentes e concluídas.
- Usar os temas claro e escuro.
- Consultar o guia de atalhos pelo botão **?**.
- Navegar pelos controles com `Tab` e `Shift + Tab`, com indicação visual de foco por teclado.
- Exibir até três tarefas inicialmente; a lista cresce até cinco linhas e oferece rolagem para as demais.
- Salvar tarefas localmente em `tarefas.json`.

### Requisitos

- Windows, macOS ou Linux com Python 3 instalado.
- Tkinter disponível na instalação do Python.

O aplicativo usa apenas módulos da biblioteca padrão do Python; não é necessário instalar pacotes com `pip`. Em algumas distribuições Linux, Tkinter pode precisar ser instalado separadamente pelo gerenciador de pacotes do sistema.

### Executar a partir do código-fonte

Abra um terminal na pasta do projeto e execute:

```bash
python main.py
```

No Windows, caso o comando `python` não esteja disponível, tente:

```powershell
py -3 main.py
```

O arquivo principal é `main.py`. A janela do aplicativo será aberta; mantenha o terminal aberto enquanto estiver usando a versão executada pelo código-fonte.

### Usar o aplicativo

1. Digite o nome da tarefa no campo de texto.
2. Escolha uma prioridade. Se nenhuma outra for selecionada, a prioridade inicial é **Intermediária**.
3. Clique em **Adicionar** ou pressione `Enter`.
4. Selecione uma tarefa para habilitar ações como concluir ou remover.
5. Para editar, use o botão de edição da tarefa ou o menu do botão direito. Ajuste o nome e a prioridade no formulário e salve pelo botão de confirmação ou com `Enter`.
6. Para cancelar uma edição, pressione `Esc` ou use o botão de cancelamento.

As alterações são gravadas em `tarefas.json` automaticamente. Esse arquivo é criado no diretório de trabalho a partir do qual o programa é iniciado. Para preservar sua lista ao mover ou reinstalar o aplicativo, faça uma cópia desse arquivo e mantenha-o junto ao diretório de trabalho apropriado.

### Atalhos e ações

| Ação | Resultado |
| --- | --- |
| `Tab` / `Shift + Tab` | Navegar entre os campos e controles. |
| `Enter` no campo da tarefa | Adicionar uma tarefa ou salvar uma edição. |
| `Esc` durante uma edição | Cancelar a edição. |
| Duplo clique em uma tarefa | Concluir ou reabrir a tarefa. |
| `Espaço` com uma tarefa selecionada | Concluir ou reabrir a tarefa. |
| Botão direito em uma tarefa | Abrir as opções de editar e apagar; apagar pelo menu pede confirmação. |
| `Ctrl` + botão direito | Editar a tarefa clicada. |
| `Shift` + botão direito | Apagar a tarefa clicada sem confirmação. |
| `Ctrl` + `↑` / `Ctrl` + `↓` | Aumentar / diminuir a prioridade da tarefa selecionada. |

O botão **?** abre o guia de atalhos dentro do aplicativo.

### Armazenamento e privacidade

As tarefas são armazenadas localmente em formato JSON no arquivo `tarefas.json`. O aplicativo não precisa de conexão com a internet e não envia os dados para um serviço remoto. Evite editar o arquivo enquanto o aplicativo estiver aberto, pois a próxima gravação do programa pode substituir alterações manuais.

### Estrutura do projeto

```text
to-do-list/
├── main.py       # Aplicativo Tkinter
├── main.spec     # Configuração do PyInstaller
├── README.md     # Documentação
└── .gitignore    # Arquivos ignorados pelo Git
```

As pastas `build/` e `dist/` são artefatos gerados durante o empacotamento e não são necessárias para executar o projeto pelo código-fonte.

### Gerar um executável (opcional)

O projeto inclui `main.spec` para empacotamento com PyInstaller. Para gerar novamente o executável, instale o PyInstaller no ambiente usado para compilar e execute na pasta do projeto:

```bash
pyinstaller main.spec
```

O executável resultante será colocado em `dist/`. A compilação deve ser feita no sistema operacional de destino; um executável do Windows, por exemplo, não é um executável nativo de macOS ou Linux.

### Solução de problemas

- **A janela não abre:** confirme que a instalação do Python inclui Tkinter.
- **`python` não é reconhecido no Windows:** tente `py -3 main.py` ou ajuste a instalação do Python.
- **As tarefas parecem ter sumido:** confira se o programa foi iniciado a partir do mesmo diretório de trabalho em que está o arquivo `tarefas.json`.
- **O executável não inicia:** experimente executar pelo código-fonte para verificar se há uma mensagem de erro no terminal e gere o pacote novamente no sistema de destino.

---

## English

A desktop to-do list application built with Python and Tkinter. Organize activities, set priorities, track completed tasks, and navigate the interface using a mouse or keyboard.

### Features

- Add, edit, complete, reopen, and remove tasks.
- Set each task's priority to **Low**, **Medium**, or **High**, shown with a colored indicator:
  - Green: low.
  - Yellow: medium.
  - Red: high.
- See the number of pending and completed tasks.
- Switch between light and dark themes.
- Open the keyboard shortcuts guide with the **?** button.
- Navigate controls with `Tab` and `Shift + Tab`, with a visible keyboard-focus indicator.
- Show up to three tasks initially; the list grows to five rows and becomes scrollable for additional tasks.
- Save tasks locally in `tarefas.json`.

### Requirements

- Python 3 on Windows, macOS, or Linux.
- Tkinter available in your Python installation.

The application uses only Python standard-library modules, so no packages need to be installed with `pip`. On some Linux distributions, Tkinter may need to be installed separately using the system package manager.

### Run from source

Open a terminal in the project folder and run:

```bash
python main.py
```

On Windows, if the `python` command is unavailable, try:

```powershell
py -3 main.py
```

The main application file is `main.py`. The app window will open; keep the terminal open while using the source-code version.

### Using the application

1. Enter a task name in the text field.
2. Choose a priority. The default priority is **Medium**.
3. Click **Add** or press `Enter`.
4. Select a task to enable actions such as completing or removing it.
5. To edit a task, use its edit button or right-click menu. Update the name and priority in the form, then save with the confirmation button or `Enter`.
6. To cancel an edit, press `Esc` or use the cancel button.

Changes are saved automatically to `tarefas.json`. This file is created in the working directory from which the application is launched. To keep your task list when moving or reinstalling the app, back up this file and keep it in the appropriate working directory.

### Shortcuts and actions

| Action | Result |
| --- | --- |
| `Tab` / `Shift + Tab` | Move between fields and controls. |
| `Enter` in the task field | Add a task or save an edit. |
| `Esc` while editing | Cancel the edit. |
| Double-click a task | Complete or reopen the task. |
| `Space` with a task selected | Complete or reopen the task. |
| Right-click a task | Open the edit and delete options; deleting from the menu requires confirmation. |
| `Ctrl` + right-click | Edit the clicked task. |
| `Shift` + right-click | Delete the clicked task without confirmation. |
| `Ctrl` + `↑` / `Ctrl` + `↓` | Increase / decrease the selected task's priority. |

The **?** button opens the in-app shortcuts guide.

### Data storage and privacy

Tasks are stored locally as JSON in `tarefas.json`. The application does not require an internet connection and does not send data to a remote service. Avoid editing the file while the application is running, as the next save may overwrite manual changes.

### Project structure

```text
to-do-list/
├── main.py       # Tkinter application
├── main.spec     # PyInstaller configuration
├── README.md     # Documentation
└── .gitignore    # Git ignore rules
```

The `build/` and `dist/` folders contain packaging artifacts and are not required to run the project from source.

### Build an executable (optional)

The project includes `main.spec` for packaging with PyInstaller. To rebuild the executable, install PyInstaller in the build environment and run this command from the project folder:

```bash
pyinstaller main.spec
```

The resulting executable will be placed in `dist/`. Build on the target operating system; for example, a Windows executable is not a native macOS or Linux executable.

### Troubleshooting

- **The window does not open:** make sure your Python installation includes Tkinter.
- **`python` is not recognized on Windows:** try `py -3 main.py` or adjust your Python installation.
- **Tasks seem to be missing:** make sure the application was launched from the same working directory that contains `tarefas.json`.
- **The executable does not start:** try running from source to check for a terminal error message, then rebuild the package on the target system.
