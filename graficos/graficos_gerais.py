import matplotlib.pyplot as plt
import numpy as np

# Estilo base
plt.style.use('bmh')

# ==========================================
# 1. DADOS REAIS EXTRAÍDOS DOS TESTES
# ==========================================

cenarios = ['100 Utilizadores', '200 Utilizadores', '500 Utilizadores']
x = np.arange(len(cenarios))
largura = 0.2

# ==========================================
# NODE.JS
# ==========================================

# Latência Mediana (ms)
node_rest = [340, 1400, 2400]
node_graphql = [1100, 3400, 5500]
node_soap = [960, 2700, 5600]
node_grpc = [55, 54, 53]

# Throughput (Requests/s)
node_rest_rps = [11.77, 12.97, 12.67]
node_graphql_rps = [11.97, 13.07, 11.98]
node_soap_rps = [11.31, 12.10, 12.03]
node_grpc_rps = [11.85, 12.96, 13.14]

# ==========================================
# PYTHON
# ==========================================

# Latência Mediana (ms)
py_rest = [950, 12000, 20000]
py_graphql = [1300, 13000, 48000]
py_soap = [45000, 43000, 59000]
py_grpc = [140, 160, 150]

# Throughput (Requests/s)
py_rest_rps = [1.89, 2.61, 2.77]
py_graphql_rps = [1.84, 2.50, 1.93]
py_soap_rps = [1.26, 1.06, 0.94]
py_grpc_rps = [2.28, 2.64, 3.31]

# ==========================================
# CORES
# ==========================================

cor_rest = '#3498db'
cor_graphql = '#9b59b6'
cor_soap = '#f1c40f'
cor_grpc = '#e74c3c'

# ==========================================
# FUNÇÃO PARA ADICIONAR RÓTULOS
# ==========================================

def adicionar_rotulos(ax, barras):
    for barra in barras:
        altura = barra.get_height()

        if altura == 0:
            continue

        if altura >= 1000:
            texto = f'{altura:.0f}'
        elif altura >= 100:
            texto = f'{altura:.1f}'
        else:
            texto = f'{altura:.2f}'

        ax.annotate(
            texto,
            xy=(barra.get_x() + barra.get_width()/2, altura),
            xytext=(0, 4),
            textcoords="offset points",
            ha='center',
            va='bottom',
            fontsize=9,
            fontweight='bold'
        )

# ==========================================
# FIGURA 1 E 2 - LATÊNCIA
# ==========================================

def gerar_grafico_latencia(
    titulo,
    nome_ficheiro,
    dados_rest,
    dados_graphql,
    dados_soap,
    dados_grpc
):
    fig, ax = plt.subplots(figsize=(12, 7))

    bar1 = ax.bar(
        x - largura*1.5,
        dados_rest,
        largura,
        label='REST',
        color=cor_rest,
        edgecolor='black',
        linewidth=0.8
    )

    bar2 = ax.bar(
        x - largura*0.5,
        dados_graphql,
        largura,
        label='GraphQL',
        color=cor_graphql,
        edgecolor='black',
        linewidth=0.8
    )

    bar3 = ax.bar(
        x + largura*0.5,
        dados_soap,
        largura,
        label='SOAP',
        color=cor_soap,
        edgecolor='black',
        linewidth=0.8
    )

    bar4 = ax.bar(
        x + largura*1.5,
        dados_grpc,
        largura,
        label='gRPC',
        color=cor_grpc,
        edgecolor='black',
        linewidth=0.8
    )

    ax.set_title(
        titulo,
        fontsize=16,
        fontweight='bold',
        pad=15
    )

    ax.set_ylabel(
        'Tempo Mediano de Resposta (ms)',
        fontsize=12,
        fontweight='bold'
    )

    ax.set_xticks(x)
    ax.set_xticklabels(
        cenarios,
        fontsize=11,
        fontweight='bold'
    )

    ax.legend(fontsize=11)

    ax.grid(
        True,
        axis='y',
        alpha=0.6,
        linestyle='--'
    )

    adicionar_rotulos(ax, bar1)
    adicionar_rotulos(ax, bar2)
    adicionar_rotulos(ax, bar3)
    adicionar_rotulos(ax, bar4)

    plt.tight_layout()
    plt.savefig(
        nome_ficheiro,
        dpi=300,
        bbox_inches='tight'
    )
    plt.close()

# ==========================================
# FIGURA 3 - THROUGHPUT
# ==========================================

def gerar_grafico_rps():
    fig, ax = plt.subplots(figsize=(12, 7))

    kw_node = {
        'linewidth': 3,
        'markersize': 9
    }

    kw_py = {
        'linestyle': '--',
        'linewidth': 3,
        'markersize': 9
    }

    ax.plot(
        cenarios,
        node_rest_rps,
        marker='o',
        label='REST Node.js',
        color=cor_rest,
        **kw_node
    )

    ax.plot(
        cenarios,
        node_graphql_rps,
        marker='o',
        label='GraphQL Node.js',
        color=cor_graphql,
        **kw_node
    )

    ax.plot(
        cenarios,
        node_soap_rps,
        marker='o',
        label='SOAP Node.js',
        color=cor_soap,
        **kw_node
    )

    ax.plot(
        cenarios,
        node_grpc_rps,
        marker='o',
        label='gRPC Node.js',
        color=cor_grpc,
        **kw_node
    )

    ax.plot(
        cenarios,
        py_rest_rps,
        marker='s',
        label='REST Python',
        color=cor_rest,
        **kw_py
    )

    ax.plot(
        cenarios,
        py_graphql_rps,
        marker='s',
        label='GraphQL Python',
        color=cor_graphql,
        **kw_py
    )

    ax.plot(
        cenarios,
        py_soap_rps,
        marker='s',
        label='SOAP Python',
        color=cor_soap,
        **kw_py
    )

    ax.plot(
        cenarios,
        py_grpc_rps,
        marker='s',
        label='gRPC Python',
        color=cor_grpc,
        **kw_py
    )

    ax.set_title(
        'Comparativo de Throughput (RPS)',
        fontsize=16,
        fontweight='bold',
        pad=15
    )

    ax.set_ylabel(
        'Requisições por Segundo (RPS)',
        fontsize=12,
        fontweight='bold'
    )

    ax.tick_params(axis='x', labelsize=11)

    ax.grid(True, alpha=0.6, linestyle='--')

    ax.legend(
        ncol=2,
        fontsize=10,
        loc='upper right'
    )

    plt.tight_layout()

    plt.savefig(
        'grafico_rps.png',
        dpi=300,
        bbox_inches='tight'
    )

    plt.close()

# ==========================================
# FIGURA 4 - REST VS gRPC
# ==========================================

def gerar_grafico_rest_vs_grpc():
    fig, ax = plt.subplots(figsize=(12, 7))

    kw_linha = {
        'linewidth': 3,
        'markersize': 10
    }

    ax.plot(
        cenarios,
        node_rest,
        marker='o',
        label='REST Node.js',
        color=cor_rest,
        **kw_linha
    )

    ax.plot(
        cenarios,
        node_grpc,
        marker='D',
        label='gRPC Node.js',
        color='#e67e22',
        **kw_linha
    )

    ax.plot(
        cenarios,
        py_rest,
        marker='s',
        linestyle='--',
        label='REST Python',
        color='#2980b9',
        **kw_linha
    )

    ax.plot(
        cenarios,
        py_grpc,
        marker='X',
        linestyle='--',
        label='gRPC Python',
        color='#c0392b',
        **kw_linha
    )

    ax.set_title(
        'REST vs gRPC - Evolução da Latência',
        fontsize=16,
        fontweight='bold',
        pad=15
    )

    ax.set_ylabel(
        'Tempo Mediano de Resposta (ms)',
        fontsize=12,
        fontweight='bold'
    )

    ax.tick_params(axis='x', labelsize=11)

    ax.grid(True, alpha=0.6, linestyle='--')

    ax.legend(fontsize=11)

    plt.tight_layout()

    plt.savefig(
        'grafico_rest_vs_grpc.png',
        dpi=300,
        bbox_inches='tight'
    )

    plt.close()

# ==========================================
# FIGURA 5 - NODE VS PYTHON
# ==========================================

def grafico_node_vs_python():
    protocolos = ['REST', 'GraphQL', 'SOAP', 'gRPC']

    node = [
        np.mean(node_rest),
        np.mean(node_graphql),
        np.mean(node_soap),
        np.mean(node_grpc)
    ]

    python = [
        np.mean(py_rest),
        np.mean(py_graphql),
        np.mean(py_soap),
        np.mean(py_grpc)
    ]

    x = np.arange(len(protocolos))
    largura = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    barras1 = ax.bar(x - largura/2, node, largura, label='Node.js')
    barras2 = ax.bar(x + largura/2, python, largura, label='Python')

    ax.set_title('Latência Média por Tecnologia')
    ax.set_ylabel('Latência Média (ms)')
    ax.set_xticks(x)
    ax.set_xticklabels(protocolos)

    adicionar_rotulos(ax, barras1)
    adicionar_rotulos(ax, barras2)

    ax.legend()

    plt.tight_layout()
    plt.savefig('node_vs_python.png', dpi=300)
    plt.close()


# ==========================================
# FIGURA 6 - ESCALABILIDADE NODE.JS
# ==========================================

def grafico_node_linhas():
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(cenarios, node_rest, marker='o', linewidth=3, label='REST')
    ax.plot(cenarios, node_graphql, marker='s', linewidth=3, label='GraphQL')
    ax.plot(cenarios, node_soap, marker='^', linewidth=3, label='SOAP')
    ax.plot(cenarios, node_grpc, marker='D', linewidth=3, label='gRPC')

    ax.set_title('Escalabilidade Node.js')
    ax.set_ylabel('Latência Mediana (ms)')

    ax.grid(True, alpha=0.5)
    ax.legend()

    plt.tight_layout()
    plt.savefig('node_linhas.png', dpi=300)
    plt.close()


# ==========================================
# FIGURA 7 - ESCALABILIDADE PYTHON
# ==========================================

def grafico_python_linhas():
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(cenarios, py_rest, marker='o', linewidth=3, label='REST')
    ax.plot(cenarios, py_graphql, marker='s', linewidth=3, label='GraphQL')
    ax.plot(cenarios, py_soap, marker='^', linewidth=3, label='SOAP')
    ax.plot(cenarios, py_grpc, marker='D', linewidth=3, label='gRPC')

    ax.set_title('Escalabilidade Python')
    ax.set_ylabel('Latência Mediana (ms)')

    ax.grid(True, alpha=0.5)
    ax.legend()

    plt.tight_layout()
    plt.savefig('python_linhas.png', dpi=300)
    plt.close()


# ==========================================
# FIGURA 8 - THROUGHPUT MÉDIO
# ==========================================

def grafico_throughput_medio():
    protocolos = ['REST', 'GraphQL', 'SOAP', 'gRPC']

    node = [
        np.mean(node_rest_rps),
        np.mean(node_graphql_rps),
        np.mean(node_soap_rps),
        np.mean(node_grpc_rps)
    ]

    python = [
        np.mean(py_rest_rps),
        np.mean(py_graphql_rps),
        np.mean(py_soap_rps),
        np.mean(py_grpc_rps)
    ]

    x = np.arange(len(protocolos))
    largura = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    barras1 = ax.bar(x - largura/2, node, largura, label='Node.js')
    barras2 = ax.bar(x + largura/2, python, largura, label='Python')

    ax.set_title('Throughput Médio')
    ax.set_ylabel('Requests/s')

    ax.set_xticks(x)
    ax.set_xticklabels(protocolos)

    adicionar_rotulos(ax, barras1)
    adicionar_rotulos(ax, barras2)

    ax.legend()

    plt.tight_layout()
    plt.savefig('throughput_medio.png', dpi=300)
    plt.close()


# ==========================================
# FIGURA 9 - COMPARAÇÃO GERAL
# ==========================================

def grafico_geral():
    tecnologias = [
        'REST\nNode',
        'GraphQL\nNode',
        'SOAP\nNode',
        'gRPC\nNode',
        'REST\nPython',
        'GraphQL\nPython',
        'SOAP\nPython',
        'gRPC\nPython'
    ]

    valores = [
        np.mean(node_rest),
        np.mean(node_graphql),
        np.mean(node_soap),
        np.mean(node_grpc),
        np.mean(py_rest),
        np.mean(py_graphql),
        np.mean(py_soap),
        np.mean(py_grpc)
    ]

    fig, ax = plt.subplots(figsize=(12, 7))

    barras = ax.bar(tecnologias, valores)

    ax.set_title('Comparação Geral de Latência')
    ax.set_ylabel('Latência Média (ms)')

    adicionar_rotulos(ax, barras)

    plt.tight_layout()
    plt.savefig('comparacao_geral.png', dpi=300)
    plt.close()   
# ==========================================
# EXECUÇÃO
# ==========================================

print("A gerar Figura 1 - Node.js...")
gerar_grafico_latencia(
    'Comparativo de Latência por Protocolo em Node.js',
    'grafico_comparativo_node.png',
    node_rest,
    node_graphql,
    node_soap,
    node_grpc
)

print("A gerar Figura 2 - Python...")
gerar_grafico_latencia(
    'Comparativo de Latência por Protocolo em Python',
    'grafico_comparativo_python.png',
    py_rest,
    py_graphql,
    py_soap,
    py_grpc
)

print("A gerar Figura 3 - Throughput...")
gerar_grafico_rps()

print("A gerar Figura 4 - REST vs gRPC...")
gerar_grafico_rest_vs_grpc()

print("A gerar Figura 5 - Node vs Python...")
grafico_node_vs_python()

print("A gerar Figura 6 - Escalabilidade Node.js...")
grafico_node_linhas()

print("A gerar Figura 7 - Escalabilidade Python...")
grafico_python_linhas()

print("A gerar Figura 8 - Throughput Médio...")
grafico_throughput_medio()

print("A gerar Figura 9 - Comparação Geral...")
grafico_geral()

print("\nGráficos gerados com sucesso!")