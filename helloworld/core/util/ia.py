import os
import ast
from typing import List, Tuple


def get_method_signatures(file_content: str) -> List[str]:
    """
    Analisa o conteúdo de um arquivo Python e retorna as assinaturas dos métodos.

    :param file_content: O conteúdo do arquivo Python como uma string.
    :return: Uma lista contendo as assinaturas dos métodos.
    """
    signatures = []
    try:
        # Analisa o código em uma árvore sintática
        tree = ast.parse(file_content)

        # Percorre todos os nós da árvore em busca de funções
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Monta a assinatura do método com o nome e parâmetros
                args = [arg.arg for arg in node.args.args]
                async_prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
                signature = f"{async_prefix}def {node.name}({', '.join(args)}):"
                signatures.append(signature)
    except SyntaxError:
        # Pula arquivos que possam conter erros de sintaxe
        pass

    return signatures


def read_python_files_from_directory(directory: str) -> List[Tuple[str, List[str]]]:
    """
    Percorre todos os arquivos de um diretório, lê os arquivos Python (.py),
    e retorna o endereço completo e a lista de assinaturas de métodos de cada arquivo.

    :param directory: O caminho do diretório a ser analisado.
    :return: Uma lista de tuplas (endereço_do_arquivo, lista_de_assinaturas).
    """
    results = []

    # Percorre o diretório recursivamente
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):  # Filtra apenas arquivos Python
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()

                # Obtém as assinaturas de métodos do arquivo
                method_signatures = get_method_signatures(file_content)
                if method_signatures:
                    results.append((file_path, method_signatures))

    return results


def print_method_signatures(directory: str) -> None:
    """
    Imprime o caminho completo do arquivo e as assinaturas de métodos de cada arquivo Python.

    :param directory: O caminho do diretório a ser analisado.
    """
    signatures_by_file = read_python_files_from_directory(directory)

    for file_path, signatures in signatures_by_file:
        print(f"\nArquivo: {file_path}")
        print("Assinaturas de Métodos:")
        for signature in signatures:
            print(f"  {signature}")


if __name__ == "__main__":
    # Exemplo de uso: altere o caminho para o diretório que você deseja analisar
    project_directory = "/home/edicleo/dev/helloworld/backend/libs/auth"

    # Chama a função para imprimir assinaturas de métodos
    print_method_signatures(project_directory)