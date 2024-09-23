# Helloworld Core

"Don't worry, even though this README is in Portuguese, all the code speaks fluent Python... and English! So feel free to dive in — no need for a translator, just your coding skills! 😎"

**Helloworld Core** é uma biblioteca projetada para agilizar o desenvolvimento de aplicações robustas e escaláveis. Implementa padrões essenciais como Use Cases, Unit of Work e Repository, além de suportar uma abordagem orientada a eventos.

Inclui implementações de mensageria, permitindo processamento e troca de mensagens em larga escala. Serviço de envio de e-mails com suporte a templates, idiomas e gerenciamento de prioridades. Features que garantem uma integração eficiente e flexível em aplicações complexas.


## Principais Características

### Unit of Work

Nossa implementação de Unit of Work assegura que todas as operações de banco de dados sejam tratadas como uma única transação, garantindo Atomicidade e Consistência. Além disso, é possível compartilhar diversas fontes de dados na mesma unidade de trabalho, facilitando a coordenação de transações complexas.

### Repository Pattern

Utilizamos o Repository Pattern para abstrair o acesso aos dados. Isso permite que a lógica de negócios interaja com dados de forma consistente, independentemente da fonte. O padrão promove um design limpo, separando preocupações e facilitando testes.

### Event-Driven Architecture

A biblioteca suporta uma arquitetura orientada a eventos, permitindo a comunicação assíncrona entre diferentes componentes do sistema. Isso é alcançado através de um sistema de eventos robusto, que facilita a implementação de reações a ações específicas, como atualizações de estado e notificações.

### Adaptadores de Infraestrutura

Helloworld Core oferece adaptadores de infraestrutura para SQLAlchemy e MongoDB, permitindo integração rápida e eficiente com diferentes bancos de dados. Além de adaptadores que certamente o ajudarão evoluir sua stack. Os adaptadores são configuráveis e podem ser estendidos para atender a necessidades específicas.

## Exemplo de Uso

Aqui está um exemplo básico de como usar a biblioteca para trabalhar com múltiplas fontes de dados.

```python
from helloworld.core.services import service_manager
from helloworld.core.infra.data import SQLADatabaseSessionManager, MongoDatabaseSessionManager

def db_session_manager_after_commit(enitities: Sequence[Dict]):
    print("Hey, you just committed the following entities to the database:", enitities)

(await service_manager.register("database", "auth", SQLADatabaseSessionManager))\
    .init("postgresql+asyncpg://postgres:password@localhost:5432/helloworld_auth")\
    .listen("after_commit", db_session_manager_after_commit)

(await service_manager.register("database", "main", SQLADatabaseSessionManager))\
    .init("postgresql+asyncpg://postgres:password@localhost:5432/helloworld")\
    .listen("after_commit", db_session_manager_after_commit)

(await service_manager.register("database", "nosql", MongoDatabaseSessionManager))\
    .init("mongodb://localhost:27017", "helloworld")
```

E aqui, um exemplo de como inicializar serviços de mensageria e mailing.

```python
from helloworld.core.mailing import Template
from helloworld.core.mailing.services import MailingService
from helloworld.core.infra.messaging import KafkaProducer
from helloworld.core.infra.mailing import KafkaSender, SMTPSender

await ((await service_manager.register("messaging", "mailing", KafkaProducer))
    .init(bootstrap_servers="localhost:9092")) \
    .start()

(await service_manager.register("mailing", "public", MailingService)) \
    .init() \
    .templates.register(Template("welcome", "en", "<html>Welcome, {{ first_name }}!</html>")) \
    .templates.register(Template("welcome", "pt", "<html>Bem-vindo, {{ first_name }}!</html>")) \
    .templates.register(Template("auto-password-reset", "en", "<html>Reset password, {{ first_name }} {{ last_name }}!</html>")) \
    .senders.register(sender=KafkaSender, priority="critical", producer=service_manager.get("messaging", "mailing")) \
    .senders.register(sender=SMTPSender, priority="medium")
```

Implementar um Caso de Uso é simples, ainda mais quando você pode utilizar diferentes Repositórios apontando para fonte de dados independentes.

```python
from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.auth.features.identity import IdentityRepository, IdentityEntity

class IdentifyUseCase(BaseUseCaseUnitOfWork[str, str], ABC):
    async def execute(self, identifier: str) -> str | None:
        raise NotImplementedError

class IdentifyUseCaseImpl(IdentifyUseCase):
    async def execute(self, identifier: str) -> str | None:        
        async with self.unit_of_work as unit_of_work:
            
            # IdentityRepository é uma abstração. Utilizamos Injeção 
            # de Dependência para resolver a implementação e trazer uma instância
            identity_repository: IdentityRepository = await unit_of_work.repository_factory.instance(IdentityRepository)
            
            # Solução simples e muito eficaz para realizar filtros
            identity_entity: IdentityEntity | None = await identity_repository.find(id=identifier)
            
            # Operações CRUD sem mistérios
            await identity_repository.save(IdentityEntity(email="bob@uncle.com"))
            await identity_repository.delete(entity_id="01J8DBYAAE5M3D4H5XGMPRRWHX")
            
            # Exemplo
            from mypackage.features.example import MyRepository
            
            # Uma implementação NoSQL foi implementada para este repositório,
            # e não precisamos saber onde está. Nosso gerenciador de DI resolverá.
            # Você pode usar outra fonte de dados, em outra tecnologia, no mesmo Unit of Work!
            my_repository: MyRepository = await unit_of_work.repository_factory.instance(MyRepository)
            
            # Não, você não precisa se preocupar com as transações realizadas.
            # Utilizamos Contexto! Todos os repositórios compartilham a mesma Unit Of Work.
            # O contexto trata os commit's e rollback's de forma automática.
```

## TODO

Aqui estão algumas funcionalidades que já estamos implementando no **helloworld-core**:

- **Migrations**: Adicionar suporte a banco de dados evolutivo.

## Explore mais

Para saber mais detalhes sobre como utilizar **Helloworld Core**, confira também os seguintes projetos de referência:

- [**Helloworld Account**](https://github.com/edicleoline/helloworld-account): Serviço de gerenciamento de contas de usuário.
- [**Helloworld Auth**](https://github.com/edicleoline/helloworld-auth): Sistema de autenticação e autorização robusto usando JWT e várias estratégias de autenticação.

Esses projetos demonstram o uso completo do **Helloworld Core** em cenários reais.

## Support
If you enjoy this project, consider supporting me on [Patreon](https://www.patreon.com/edicleoline).