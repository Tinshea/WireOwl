# WireOwl

**WireOwl** est un visualisateur de trames réseau développé dans le cadre d’un projet universitaire à Sorbonne Université. Il permet d’analyser, filtrer, visualiser et exporter des paquets réseau via une interface graphique intuitive. Ce projet a été l’occasion d'explorer en profondeur les couches réseau et les protocoles courants (TCP, UDP, HTTP, IPv4/IPv6, MAC).

## 🎓 Objectifs pédagogiques

- Comprendre le fonctionnement des couches réseau.
- Manipuler et analyser des trames réseau.
- Implémenter des parsers pour différents protocoles (TCP, HTTP...).
- Développer une interface graphique pour la visualisation et le filtrage des trames.
- Générer des rapports PDF automatisés.

---

## 🧩 Fonctionnalités principales

- 🧪 **Analyse de trames** : extraction des adresses MAC, IP, flags TCP, méthodes HTTP, etc.
- 🗂️ **Filtrage avancé** : par protocole, adresses IP/MAC, ports, etc.
- 🖼️ **Interface graphique** : affichage interactif avec `tkinter`.
- 📄 **Export PDF** : génération de rapports détaillés des trames et visualisation type "flowgraph".
- 🧹 **Nettoyage** : suppression automatique du cache PyCache.

---

## ⚙️ Installation

### ✅ Prérequis

- Python 3.11
- `pip`

### 🔧 Installation des dépendances

```bash
make setup
```

Installe automatiquement tous les modules requis.

---

## 🚀 Utilisation

### Lancer le programme

```bash
make run
```

### Nettoyer le projet

```bash
make clean
```

Supprime les fichiers de cache Python (`__pycache__`).

---

## 🧠 Architecture du projet

| Fichier            | Rôle                                                                 |
|--------------------|----------------------------------------------------------------------|
| `main.py`          | Point d’entrée du programme.                                         |
| `source.py`        | Gère l’IHM, les interactions et l’analyse globale.                   |
| `trame.py`         | Analyse des adresses MAC/IP.                                         |
| `tcp.py`           | Extraction des flags et informations TCP.                            |
| `httpmodule.py`    | Détection des requêtes/réponses HTTP.                                |
| `filtrage.py`      | Système de filtrage et création de la base de données SQLite.        |
| `pdf.py`           | Génération et mise en forme des rapports PDF.                        |

---

## 🧪 Protocoles étudiés

- Ethernet (MAC)
- IPv4 / IPv6
- TCP / UDP
- HTTP

---

## 🔍 Exemples de filtres disponibles

- `protocol == TCP`
- `ip.src != 192.168.1.1`
- `http.version == 1.1`

---

## 👨‍💻 Auteurs

- **Malek Bouzarkouna** [@Tinshea](https://github.com/Tinshea)
- **Sevag Baboyan** [@SesevagB](https://github.com/SesevagB)

---

## 🏛️ Université

Projet réalisé à **Sorbonne Université**, dans le cadre du cursus en informatique.
