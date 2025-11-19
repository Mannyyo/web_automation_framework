# Web Automation Framework

Framework de automação web desenvolvido em Python, utilizando Selenium, com arquitetura moderna baseada em:

- **BrowserManager** (wrapper com retry, logging, waits e ações robustas)
- **Page Object Model (POM)**
- **Component Objects**
- **Flow Objects**
- **Estrutura modular e escalável**

Este framework foi projetado para automações administrativas e operacionais, como navegação em sistemas web, extração de relatórios, preenchimento de formulários e geração de tabelas Excel.

---

# 📁 Estrutura do Projeto

```

web_automation_framework/
│
├── core/
│   ├── browser_manager.py      # Wrapper do Selenium
│   ├── base_page.py            # Base para todas as Page Objects
│   └── config.py               # Configurações (em breve)
│
├── pages/
│   ├── login_page.py           # Página de login do sistema
│   └── user_home_page.py       # Home do usuário após login (menus e navegação)
│
├── components/
│   └── noticia_modal.py        # Modal que aparece após login
│
├── flows/
│   └── consultar_protocolos_flow.py  # Fluxo de Login → Home → Protocolos
│
├── utils/
│   ├── logger.py               # Logger configurado
│   └── decorators.py           # Decorators úteis (retry, time_it)
│
├── excel/
│   └── excel_manager.py        # Manipulação de arquivos Excel
│
├── examples/
│   └── exemplo_relatorio_sitac.py     # Exemplo inicial (pré-POM)
│
└── README.md

````

---

# 🚀 Principais Conceitos do Framework

## ✓ **BrowserManager — Alto nível sobre Selenium**
O `BrowserManager` centraliza todas as ações do Selenium:

- `.click()`, `.type()`, `.wait_for()`, `.get_text()`
- retry automático com o decorator `retry_on_fail`
- logs detalhados
- gerenciamento de abas, frames, JS, scroll
- robustez contra elementos dinâmicos

Nenhum Page Object toca diretamente no Selenium.

---

## ✓ **BasePage — Camada base do POM**
A `BasePage` oferece:

- `click()`
- `type()`
- `wait()`
- `get_text()`
- `execute_js()`
- `scroll_to()`
- `open(url)`

Todas as Pages derivam dela.

---

## ✓ **Page Objects**
Representam **páginas reais** do sistema.

Exemplos criados:

### `LoginPage`
- Abrir URL de login  
- Preencher usuário e senha  
- Submeter formulário  
- Verificar se login foi bem-sucedido  

### `UserHomePage`
Representa a página inicial pós-login:
- Menus laterais
- Submenus dinâmicos
- Acesso ao módulo “Protocolos”
- Acesso às categorias:
  - "Aguardando resposta do despacho"
  - "Departamento de Fiscalização"
  - etc.

---

## ✓ **Component Objects**
Representam partes reutilizáveis da interface.

### `NoticiaModal`
- Detecta e fecha o modal de notícias exibido após o login

---

## ✓ **Flow Objects**
Controlam fluxos completos de negócio.

### `ConsultarProtocolosFlow`
Fluxo:  
Login → Fechar Modal → Abrir “Protocolos” → “A Receber” → Categoria X

Exemplo de uso:

```python
flow = ConsultarProtocolosFlow(browser)
flow.executar_fluxo(username, password, categoria=1)
````

Ou versão semântica:

```python
flow.executar_fluxo_fiscalizacao(username, password)
```

---

# 🧪 Exemplo de Uso Completo

```python
from core.browser_manager import Browser
from flows.consultar_protocolos_flow import ConsultarProtocolosFlow

browser = Browser(browser="chrome", headless=False)

flow = ConsultarProtocolosFlow(browser)
flow.executar_fluxo(
    username="meu_usuario",
    password="minha_senha",
    categoria=1
)

browser.quit()
```

---

# 📌 Próximos Passos do Projeto

* Criar **ProtocolosPage** (tabela e ações avançadas)
* Criar **TableComponent**
* Criar **models** para representar itens da tabela
* Implementar geração automática de relatórios
* Aperfeiçoar Flow Objects avançados

---

# 🛠 Requisitos

* Python 3.10+
* Selenium 4.x
* webdriver-manager
* openpyxl
* logging configurado

---

# 📄 Licença

Projeto interno — uso livre e modificação permitida.