# Privacy and data flow

Current flow: browser form inputs -> FastAPI validation -> scientific engine ->
SQLAlchemy simulation record -> JSON response and history endpoint. The application
does not currently collect accounts, emails, uploads, analytics, or AI prompts.

Simulation inputs and outputs are persisted locally. There is no deletion/export
workflow, retention policy, user ownership, privacy notice, or production backup
policy. These remain incomplete requirements for multi-user deployment.
