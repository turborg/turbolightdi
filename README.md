<p align="center">
<a href="https://turborg.com/TurboLightDI" target="_blank">
<img src="https://i.postimg.cc/TPTSD04k/turbolightdi.png" alt="TurboLightDI Logo" width="400px">
</a>
</p>

<div align="center">

![Python Versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue?style=flat-square)
![Development Status](https://img.shields.io/badge/status-Alpha-orange?style=flat-square)

</div>

<p align="center">
TurboLightDI is a lightweight, high-performance Inversion of Control container for Python.
</p>


## About TurboLightDI

TurboLightDI aims to provide elegant dependency injection using decorators and type hints, allowing you to build decoupled, testable, and maintainable applications.

Core features:

* Zero Configuration: Use standard Python decorators.
* Constructor Injection: Automatic wiring based on Python type hints.
* Lifecycle Management: Efficiently manages object lifecycles (singleton, prototype...)
* Third-Party Support: Use `@borg` to inject objects from libraries like Redis, SQLAlchemy or any other third party lib.
* Circular Dependency Detection: Built-in protection against recursive injections (for example, A → B, B → A).

---
## Development
```bash
uv venv --python 3.12
uv pip install .[dev]
pre-commit install
```

## Usage
**TurboLightDI** uses a special hierarchy to manage your application's lifecycle. Components are divided into **External Components** and **Internal Logic**.

### Quick Example
```python
from TurboLightDI import cy, borg, service, repository

@cy
class DatabaseConfig:
    @borg
    def session_factory(self) -> Session:
        return create_session_factory()

@repository
class UserRepository(TurboquentRepository):
    pass

@service
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
```

### External Integration
Use these decorators to integrate third-party libraries (like Redis, SQLAlchemy etc..) into your application.
* **`@cy` (Configuration Yield)**: A class-level decorator for modules that house the configurations required to yield the objects your application needs.
* **`@borg` (Bound Object Resource Graph)**: A method-level decorator used within a `@cy` class. It holds and registers third-party libraries as assimilated components in the DI graph.

### Internal Logic (components)
For classes created within your own codebase, use the following decorators to enable auto DI:

* **`@component`**: The base decorator for any general-purpose class managed by the TurboLightDIContainer.

#### Specialized Components
To maintain clean architectural separation, use these specific aliases:

| Decorator         | Role | Description                                                                                                                                                          |
|:------------------| :--- |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`@controller`** | **REST APIs** | Entry points that orchestrate RESTful communication and handle incoming requests                                                                                     |
| **`@service`**    | **Business Logic** | Encapsulates business logic.                                                                                                                                         |
| **`@repository`** | **Data Access** | Communicates with data holders. Usually implements `TurboquentRepository`, providing a powerful abstraction layer for common DB operations with minimal boilerplate. |



---
*Part of the [**Turborg**](https://turborg.com) AI-First Open Source Suite Ecosystem*
