import xmlrpc.client
import sys
import json

def criarJson(codigo, titulo, autor, edicao, anoPublicacao) :
    livro = {}

    if (codigo > 0)        : livro["codigo"] = codigo
    if (titulo != "")      : livro["titulo"] = titulo
    if (autor != "")       : livro["autor"]  = autor
    if (edicao != "")      : livro["edicao"] = edicao
    if (anoPublicacao > 0) : livro["anoPublicacao"] = anoPublicacao

    livroJson = json.dumps(livro)

    return livroJson

def comunicarServidor(jsonEnviar, operacao) :
    servidor = xmlrpc.client.ServerProxy('http://' + ip + ':'+ porta)

    if (operacao == "Criar") :
        mensagemRecebida = servidor.CriarLivro(jsonEnviar)
    elif (operacao == "ConsultarAutor") :
        mensagemRecebida = servidor.ConsultarLivroAutor(jsonEnviar)
    elif (operacao == "ConsultarTitulo") :
        mensagemRecebida = servidor.ConsultarLivroTitulo(jsonEnviar)
    elif (operacao == "ConsultarAnoEdicao") :
        mensagemRecebida = servidor.ConsultarLivroPorAnoEdicao(jsonEnviar)
    elif (operacao == "Remover") :
        mensagemRecebida = servidor.RemoverLivro(jsonEnviar)
    elif (operacao == "Alterar") :
        mensagemRecebida = servidor.AlterarLivro(jsonEnviar)

    return mensagemRecebida    

def formatarVisualizacao(mensagemJson) :
        livroJson = json.loads(mensagemJson)

        print("----------------------------------------------------")

        for livro in livroJson:
            print("  Codigo: " + str(livro["codigo"]))
            print("  Titulo: " + livro["titulo"])
            print("  Autor:  " + livro["autor"])
            print("  edicao: " + livro["edicao"])
            print("  Ano publicacao: " + str(livro["anoPublicacao"]))
            print("  ")

        print("----------------------------------------------------")

def mainMenu() :
	escolhaPrincipal = 0

	while (escolhaPrincipal != 6):
		menuPrincipal()
		escolhaPrincipal = int(input('Escolha uma opção: '))

		if (escolhaPrincipal == 1)   : menuCriar()
		elif (escolhaPrincipal == 2) : menuConsultar()
		elif (escolhaPrincipal == 3) : menuConsultarAnoEdicao()
		elif (escolhaPrincipal == 4) : menuRemover()
		elif (escolhaPrincipal == 5) : menuAlterar()
		elif (escolhaPrincipal > 6)  : print("Opcao invalida")

def menuPrincipal():
    print('''
        Livros - Rpc

        [Menu principal]
        [1] - Criar livro
        [2] - Consultar livro
        [3] - Consultar por ano e nro de edicao
        [4] - Remover livro
        [5] - Alterar livro
        [6] - Sair
        ''')

def menuCriar():
    print("Titulo do livro: ")
    titulo = str(input())

    print("Autor do livro: ")
    autor = str(input())

    print("Edicao do livro: ")
    edicao = str(input())

    print("ano de publicacao do livro: ")
    anoPublicacao = int(input())
    
    livroJson = criarJson(0,titulo,autor,edicao,anoPublicacao)
    mensagem = comunicarServidor(livroJson,"Criar")
    print(mensagem)

def menuConsultar():
    escolhaMenu2 = 0

    while (escolhaMenu2 != 3):
        print('''
            Livros - Rpc
            
            [Consultar livro]
            [1] - Consultar pelo Autor
            [2] - Consultar pelo Titulo
            [3] - Voltar
        ''')
        escolhaMenu2 = int(input('Escolha uma opção: '))

        if (escolhaMenu2 == 1) :
            print("Autor do livro: ")
            autor = str(input())

            livroJson = criarJson(0,"",autor,"",0)
            mensagem = comunicarServidor(livroJson,"ConsultarAutor")
            formatarVisualizacao(mensagem)

            return
        elif (escolhaMenu2 == 2) :
            print("Titulo do livro: ")
            titulo = str(input())

            livroJson = criarJson(0,titulo,"","",0)
            mensagem = comunicarServidor(livroJson,"ConsultarTitulo")
            formatarVisualizacao(mensagem)

            return
        elif (escolhaMenu2 == 3) :
            return
        elif (escolhaMenu2 > 3) :
            print("Opcao invalida")

def menuConsultarAnoEdicao():
    print("Ano do livro: ")
    anoPublicacao = int(input())

    print("Edicao do livro: ")
    edicao = str(input())

    livroJson = criarJson(0,"","",edicao,anoPublicacao)
    mensagem = comunicarServidor(livroJson,"ConsultarAnoEdicao")
    formatarVisualizacao(mensagem)

def menuRemover():
    print("Titulo do livro: ")
    titulo = str(input())

    livroJson = criarJson(0,titulo,"","",0)
    mensagem = comunicarServidor(livroJson,"Remover")
    print(mensagem)

def menuAlterar():
    print("Titulo do livro: ")
    titulo = str(input())

    livroJson = criarJson(0,titulo,"","",0)
    mensagem = comunicarServidor(livroJson,"ConsultarTitulo")
    jsonRecebido = json.loads(mensagem)

    escolhaMenu5 = 0

    while (escolhaMenu5 != 5):
        print('''
            Livros - Rpc
            
            [Alterar livro]
            [1] - Alterar autor
            [2] - Alterar titulo
            [3] - Alterar edicao
            [4] - Alterar ano de publicacao"
            [5] - Voltar
        ''')
        escolhaMenu5 = int(input('Escolha uma opção: '))

        if (escolhaMenu5 == 1) :
            print("Autor do livro: ")
            autor = str(input())

            for livro in jsonRecebido:
                codigo        = livro['codigo']
                titulo        = livro['titulo']
                edicao        = livro['edicao']
                anoPublicacao = livro['anoPublicacao']
            
                livroJson = criarJson(codigo,titulo,autor,edicao,anoPublicacao)
                mensagem = comunicarServidor(livroJson,"Alterar")
                print(mensagem)

                return
        elif (escolhaMenu5 == 2) : 
            print("Titulo do livro: ")
            titulo = str(input())

            for livro in jsonRecebido:
                codigo        = livro['codigo']
                autor         = livro['autor']
                edicao        = livro['edicao']
                anoPublicacao = livro['anoPublicacao']
            
                livroJson = criarJson(codigo,titulo,autor,edicao,anoPublicacao)
                mensagem = comunicarServidor(livroJson,"Alterar")
                print(mensagem)
                
                return
        elif (escolhaMenu5 == 3) :
            print("Edicao do livro: ")
            edicao = str(input())

            for livro in jsonRecebido:
                codigo        = livro['codigo']
                autor         = livro['autor']
                titulo        = livro['titulo']
                anoPublicacao = livro['anoPublicacao']
            
                livroJson = criarJson(codigo,titulo,autor,edicao,anoPublicacao)
                mensagem = comunicarServidor(livroJson,"Alterar")
                print(mensagem)

                return
        elif (escolhaMenu5 == 4) :
            print("ano de publicacao do livro: ")
            anoPublicacao = int(input())

            for livro in jsonRecebido:
                codigo = livro['codigo']
                autor  = livro['autor']
                titulo = livro['titulo']
                edicao = livro['edicao']
            
                livroJson = criarJson(codigo,titulo,autor,edicao,anoPublicacao)
                mensagem = comunicarServidor(livroJson,"Alterar")
                print(mensagem)

                return
        elif (escolhaMenu5 == 5) :
            return
        elif (escolhaMenu5 > 5) :
            print("Opcao invalida")

if len(sys.argv) != 3:
    print('%s <ip> <porta>' %sys.argv[0])
    sys.exit(0)

ip = sys.argv[1]
porta = sys.argv[2]

mainMenu()