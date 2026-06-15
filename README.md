<div align="center">
  <h1>Event Planning</h1>
  
[![NestJS](https://img.shields.io/badge/NestJS-11.0.1-E0234E?style=flat-square&logo=nestjs)](https://nestjs.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16.2.1-000000?style=flat-square&logo=next.js)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.2.4-61DAFB?style=flat-square&logo=react)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4-06B6D4?style=flat-square&logo=tailwindcss)](https://tailwindcss.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13.5-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Prisma](https://img.shields.io/badge/Prisma-7.6.0-2D3748?style=flat-square&logo=prisma)](https://www.prisma.io/)
[![Redis](https://img.shields.io/badge/Redis-7-D82C20?style=flat-square&logo=redis)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)
</div>


## Prerequisites
- Git
- Docker Desktop (with Docker Compose plugin)
- Free local ports: `3000` (frontend) and `3100` (backend)
- Optional for local non-Docker runs: Node.js `22.x` and npm

## Clone the Project
```powershell
git clone --recurse-submodules https://gitlab.hof-university.de/events/infrastructure.git
cd infrastructure
```

## Start the Project

### Environment Variables
- Copy the .env.example
- Rename it to .env
- Fill in the required values (e.g., database credentials, JWT secret)
### Development mode (hot reload)
```powershell
docker compose -f docker-compose.dev.yml up --build
```
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:3100`

### Production mode
```powershell
docker compose up --build
```
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:3100`

## Mock Server

Der Mock-Server ersetzt das echte Backend durch ein fake während der Entwicklung, um diese zu vereinfachen und backend und frondend Entwicklung von einander zu trennen.

### Voraussetzungen

- Deine Node.js Version muss mindestens v22.12 oder höher sein !
[Link zum herunterladen der Node.js Version](https://nodejs.org/de)
- Im bachend einmal 
```bash
npm install
```
- ausführen 

### Starten der Mock servers

- Im backend
```bash
npm run mock
```
- ausführen. Der Server läuft dann auf `http://localhost:4010`.

- **Wenn Änderungen am Backend gemacht wurden dann muss erst noch die `swagger.yml` neu generiert werden** um den Mock server zu starten, das bedeutet das man erst:

```bash
cd backend
npm run start:dev
```
- machen muss um die `swagger.yml` zu aktualisieren(neu zu generieren)
- um Ressourcen zu sparen sollte man nun NestJS wieder stoppen dafür **Strg + C** im Terminal drücken, dann wieder normal

```bash
npm run mock
```
- ausführen

### Mit Docker Starten

#### Der Unterschied:
- `npm run mock` → Prism läuft direkt auf deinem Computer
- `docker compose up prism` → Prism läuft in einem Container, zusammen mit den anderen Services (Postgres, NestJS, Next.js)

```bash
docker compose up prism
```

### Zwischen Mock und echtem Backend wechseln

In der `.env` Datei im Frontend-Ordner die URL anpassen:

- **Mock-Server nutzen** NEXT_PUBLIC_API_URL=http://localhost:**4010**

- **Echtes Backend nutzen** NEXT_PUBLIC_API_URL=http://localhost:**3100**
