import funcoesBank as fc

menu = """
[d] = Depositar
[s] = Sacar
[e] = Extrato
[q] = Sair

=> """

# Variáveis
saldo = 0.0
extrato = ''
num_saques = 0

# Loop de Seleção
while True:
    option = input(menu)

    # Opção Depósito
    if option == 'd':
        saldo, extrato = fc.deposito(saldo, extrato)

    # Opção Saque
    elif option == 's':
        saldo, extrato, num_saques = fc.saque(saldo, extrato, num_saques)

    # Opção Extrato
    elif option == 'e':
        fc.show_extrato(saldo, extrato)

    # Opção Sair
    elif option == 'q':
        break

    # Opção Default
    else:
        print('Operação inválida, pro favor selecione novamente a operação desejada.')