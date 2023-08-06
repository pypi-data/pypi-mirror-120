# Verwendung des Robot Framework mit der 5Minds-Engine

- [Voraussetzung](#voraussetzung)
- [Verwendung](#verwendung)
  * [BPMN-Datei veröffentlichen](#bpmn-datei-veroffentlichen)
  * [Prozessmodell starten](#prozessmodell-starten)
  * [Ergebnisse von beendeten Prozessen abfragen](#ergebnisse-von-beendeten-prozessen-abfragen)
  * [Umgang mit External-Tasks](#umgang-mit-external-tasks)
  * [Umgang mit Benutzer-Task (User-Task)](#umgang-mit-benutzer-task-user-task)
  * [Umgang mit Ereignissen (Events)](#umgang-mit-ereignissen-events)
    + [Signale](#signale)
    + [Nachrichten (Messages)](#nachrichten-messages)
## Voraussetzung

## Verwendung

### BPMN-Datei veröffentlichen

```robotframework
*** Settings ***
Library         ProcessCubeLibrary     engine_url=http://localhost:56000

*** Tasks ***
Successfully deploy
    Deploy Processmodel    examples/hello_robot_framework.bpmn
```

### Prozessmodell starten

### Ergebnisse von beendeten Prozessen abfragen

### Umgang mit External-Tasks

### Umgang mit Benutzer-Task (User-Task)

### Umgang mit Ereignissen (Events)

#### Signale

#### Nachrichten (Messages)

