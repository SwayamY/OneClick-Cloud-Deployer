# OneClick Cloud Deployer 🚀

A **Work-in-Progress** DevOps project to deploy containerized applications from GitHub to cloud VM instances **without SSH**, using **cloud-native automation**.

## 🎯 Goal

Build a simple web backend (FastAPI) that allows:
- Cloning a GitHub repo with a `docker-compose.yml`
- Validating the compose file
- Provisioning a cloud VM with Docker pre-installed
- Running the `docker-compose` setup remotely
- Returning the external IP for live app testing

## ✅ Current Progress (10%)

| Component              | Status        |
|------------------------|---------------|
| FastAPI Project Setup  | ✅ Done        |
| GitHub Clone Endpoint  | ✅ Working     |
| Compose Validator      | ✅ Working     |
| VM Provisioning Logic  | 🚧 Planned     |
| CI/CD Setup (GitHub Actions) | ⚙️ In progress |
| External IP Return     | 🚧 Planned     |

## ⏸️ On Hold Due to Exams

- This project is on hold due to **sessionals and end-sem exams** (May 5– June 6).
- Will resume work and update progress after exams.

## ⚙️ Tech Stack

- **Backend**: FastAPI + Uvicorn  
- **Containerization**: Docker Compose  
- **Automation**: Planned GCP SDK, Bash, and native tooling  
- **CI/CD**: GitHub Actions (to be implemented)  

## 🔜 Planned Next Steps

- Validate docker-compose services
- Provision VMs with cloud-native tools
- Run container stack remotely
- Return service endpoint (external IP)
- Add user auth layer (future)

---

> This is a 30% deliverable and actively evolving. Intended for portfolio showcase in DevOps internship applications.
