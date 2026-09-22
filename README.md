# Order Server API

Servicio Backend para la gestión de órdenes desarrollado con **FastAPI** y **Python 3.13**, aplicando principios de **Arquitectura Hexagonal (Clean Architecture)**, pruebas automatizadas con aislamiento total, migraciones automáticas con **Alembic** y contenedorización con **Docker**.

---

## 🛠️ Tecnologías y Herramientas

* **Lenguaje:** Python 3.13
* **Framework Web:** FastAPI
* **ORM & Migraciones:** SQLAlchemy + Alembic
* **Gestor de Dependencias:** Poetry 2.4.3
* **Base de Datos:** SQLite (desarrollo local) / Soporte para PostgreSQL
* **Contenedorización:** Docker (Multi-stage build) & Docker Compose
* **Testing:** Pytest + TestClient (cobertura > 85%)
* **Calidad de Código:** Ruff (Linter), MyPy (Type Checker), pip-audit (Seguridad)
* **CI/CD:** GitHub Actions

---

## 📐 Arquitectura

El proyecto está diseñado bajo **Arquitectura Hexagonal** para desacoplar completamente la lógica de negocio de la infraestructura:

```text
src/order_server/
├── domain/            # Entidades, Enums e Interfaces de Repositorio (Puertos)
├── application/       # Casos de uso (Lógica de negocio) y DTOs
├── infrastructure/    # Adaptadores de BD (SQLAlchemy), Modelos ORM, Hashers
└── config/            # Configuración de base de datos y variables de entorno
```
