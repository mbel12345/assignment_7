# Project Setup

## Set up Repo
In Github:
Create new repo called assignment_7 and make sure it is public

In WSL/VS Code Terminal:
```bash
mkdir assignment_7
cd assignment_7/
git init
git branch -m main
git remote add origin git@github.com:mbel12345/assignment_7.git
vim README.md
git add . -v
git commit -m "Initial commit"
git push -u origin main
```

## Set up virtual environment
In WSL/VS Code Terminal:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Build the container, run it, and push to DockerHub
In SWL/VS Code Terminal:
```bash

# Build container
docker build -t qr-code-generator-app .

# Run container with defaults (not recommened, you need a mount if you want to the view the QR codes)
docker container rm -f qr-generator && docker run -d --name qr-generator qr-code-generator-app

# Run container with proper directory mounts and override default url
docker container rm -f qr-generator && docker run -d --name qr-generator -v ./qr_codes:/app/qr_codes qr-code-generator-app --url http://www.njit.edu

# If this shows no output, the app is working. Check qr_codes directory on localhost, a new QR code should have been generated.
docker logs qr-generator

# Push to DockerHub
docker login
docker tag qr-code-generator-app msb64/qr-code-generator-app
docker push msb64/qr-code-generator-app
```
