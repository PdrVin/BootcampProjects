from abc import ABC, abstractmethod
from datetime import datetime
import textwrap


class Cliente:
    def __init__(self, address: str):
        self.address = address
        self.accounts = []

    @staticmethod
    def make_transact(account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, name: str, birth_date: str, address: str):
        super().__init__(address)
        self.cpf = cpf
        self.name = name
        self.birth_date = birth_date


class Conta:
    def __init__(self, number: int, client: PessoaFisica):
        self._balance = 0.0
        self._number = number
        self._agency = "0001"
        self._client = client
        self._history = Historico()

    @classmethod
    def new_account(cls, number: int, client: PessoaFisica):
        return cls(number, client)

    @property
    def saldo(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def agency(self):
        return self._agency

    @property
    def client(self):
        return self._client

    @property
    def history(self):
        return self._history

    def sacar(self, value: float):
        if value > self.saldo:
            print('\033[91m'
                  'Operação falhou! Você não tem saldo suficiente.'
                  '\033[m')

        elif value > 0:
            self._balance -= value
            print(f'\033[92m'
                  f'Retirada efetuado com sucesso!\n'
                  f'\033[91m'
                  f'Retirada:\tR$ {value:.2f}'
                  f'\033[m')
            return True

        else:
            print('\033[91m'
                  'Operação falhou! Valor informado é inválido.'
                  '\033[m')

        return False

    def depositar(self, value: float):
        if value > 0:
            self._balance += value
            print(f'\033[92m'
                  f'Depósito efetuado com sucesso!\n'
                  f'Depósito:\tR$ {value:.2f}'
                  f'\033[m')

        else:
            print('\033[91m'
                  'Operação falhou! Valor informado inválido.'
                  '\033[m')
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, number: int, client: PessoaFisica, limit=500.0, limit_saques=3):
        super().__init__(number, client)
        self._limit = limit
        self._limit_saques = limit_saques

    def sacar(self, value: float):
        num_saques = len(
            [transact for transact in self.history.transactions
             if transact['type'] == Saque.__name__]
        )

        limit_exceeded = value > self._limit
        saques_exceeded = num_saques >= self._limit_saques

        if limit_exceeded:
            print('\033[91m'
                  'Operação falhou! Valor do saque maior que o limite permitido.'
                  '\033[m')
        elif saques_exceeded:
            print('\033[91m'
                  'Operação falhou! Número de saques excedidos.'
                  '\033[m')
        else:
            return super().sacar(value)

        return False

    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agency}
            C/C:\t\t{self.number}
            Titular:\t{self.client.name}
        """


class Historico:
    def __init__(self):
        self._transactions = list()

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type":
                    "\033[91m" + "Retirada"
                    if transaction.__class__.__name__ == "Saque"
                    else "\033[92m" + "Deposito",
                "value": transaction.value,
                "date": datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def value(self) -> float:
        pass

    @classmethod
    @abstractmethod
    def register(cls, account):
        pass


class Saque(Transacao):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account: ContaCorrente):
        transaction_sucessed = account.sacar(self.value)

        if transaction_sucessed:
            account.history.add_transaction(self)


class Deposito(Transacao):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account: ContaCorrente):
        transaction_sucessed = account.depositar(self.value)

        if transaction_sucessed:
            account.history.add_transaction(self)


def menu():
    title = " MENU "
    display = f"""
    {title:=^26}
    [D]\tDepositar
    [S]\tSacar
    [E]\tExtrato
    [C]\tNovo Cliente
    [N]\tNova Conta
    [L]\tListar Contas
    [Q]\tSair
    => """
    return input(textwrap.dedent(display))


# Filtrar Clientes
def filter_client(cpf: str, clients: list) -> PessoaFisica:
    filtered_clients = [client for client in clients if client.cpf == cpf]
    return filtered_clients[0] if filtered_clients else None


# Recuperar Conta Cliente
def recover_account(client: PessoaFisica) -> ContaCorrente:
    if not client.accounts:
        print('\033[91m'
              'Cliente não possui conta!'
              '\033[m')
    return client.accounts[0]


# Deposito
def depositar(clients: list):
    cpf = input("Informe o CPF do Cliente: ")
    client = filter_client(cpf, clients)

    if not client:
        print('\033[91m'
              'Cliente não encontrado!'
              '\033[m')
        return

    value = float(input("Informe o valor do depósito: "))
    transaction = Deposito(value)

    account = recover_account(client)
    if not account:
        return

    client.make_transact(account, transaction)


# Saque
def sacar(clients: list):
    cpf = input("Informe o CPF do Cliente: ")
    client = filter_client(cpf, clients)

    if not client:
        print('\033[91m'
              'Cliente não encontrado!'
              '\033[m')
        return

    value = float(input("Informe o valor do saque: "))
    transaction = Saque(value)

    account = recover_account(client)
    if not account:
        return

    client.make_transact(account, transaction)


# Exibir Extrato
def show_extract(clients: list):
    cpf = input("Informe o CPF do Cliente: ")
    client = filter_client(cpf, clients)

    if not client:
        print('\033[91m'
              'Cliente não encontrado!'
              '\033[m')
        return

    account = recover_account(client)
    if not account:
        return

    title = ' EXTRATO '
    print(f'{title:=^26}')

    transactions = account.history.transactions
    extract = ""

    if not transactions:
        extract = "Não foram realizadas movimentações!"
    else:
        for transaction in transactions:
            extract += (f"{transaction['type']}:\t"
                        f"R${transaction['value']:>8.2f}"
                        f"\033[m\n")

    print(extract)
    print(f'\033[94m'
          f'Saldo:\t\tR${account.saldo:>8.2f}'
          f'\033[m')
    print(f'{"":=^26}')


# Criar Cliente
def create_client(clients: list):
    cpf = input("Informe o CPF do Cliente: ")
    client = filter_client(cpf, clients)

    if client:
        print('\033[91m'
              'Usuário já cadastrado com este CPF!'
              '\033[m')
        return

    clients.append(PessoaFisica(**{
        'cpf': cpf,
        'name': input('Informe o Nome Completo: '),
        'birth_date': input('Informe a Data de Nascimento (dd-mm-aaaa): '),
        'address': input('Informe o Endereço (logradouro, num, bairro, cidade/uf): ')
    }))

    print('\033[92m'
          'Usuário cadastrado com sucesso!'
          '\033[m')


# Criar Conta Corrente
def create_current_account(num_account: int, clients: list, accounts: list):
    cpf = input("Informe o CPF do cliente: ")
    client = filter_client(cpf, clients)

    if not client:
        print('\033[91m'
              'Usuário não encontrado, Fluxo de criação de conta encerrado!'
              '\033[m')
        return

    account = ContaCorrente.new_account(num_account, client)
    accounts.append(account)
    client.accounts.append(account)

    print('\033[92m'
          'Conta criada com sucesso!'
          '\033[m')


# Listar Contas
def list_accounts(accounts: list):
    for account in accounts:
        print('=' * 30)
        print(textwrap.dedent(str(account)))


# Execucão
def main():
    clientes = list()
    contas = list()

    # Loop de Seleção
    while True:
        # Exibição Menu
        option = menu().upper()

        # Opção Depósito
        if option == 'D':
            depositar(clientes)

        # Opção Saque
        elif option == 'S':
            sacar(clientes)

        # Opção Extrato
        elif option == 'E':
            show_extract(clientes)

        # Opção Novo Cliente
        elif option == 'C':
            create_client(clientes)

        # Opção Nova Conta
        elif option == 'N':
            num_conta = len(contas) + 1
            create_current_account(num_conta, clientes, contas)

        # Opção Listar Contas
        elif option == 'L':
            list_accounts(contas)

        # Opção Sair
        elif option == 'Q':
            break

        # Opção Default
        else:
            print('\033[91m'
                  'Operação inválida, por favor selecione novamente a operação desejada.'
                  '\033[m')


main()
