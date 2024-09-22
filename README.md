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


## Explore mais

Para saber mais detalhes sobre como utilizar **Helloworld Core**, confira também os seguintes projetos de referência:

- [**Helloworld Auth**](https://github.com/edicleoline/helloworld-auth): Sistema de autenticação e autorização robusto usando JWT e várias estratégias de autenticação.
- [**Helloworld Account**](https://github.com/edicleoline/helloworld-account): Serviço de gerenciamento de contas de usuário.

Esses projetos demonstram o uso completo do **Helloworld Core** em cenários reais.