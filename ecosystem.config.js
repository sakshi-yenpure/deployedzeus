module.exports = {
  apps: [
    {
      name: "frontend",
      script: "npx",
      args: "serve -s build -l 3000",
      cwd: "/home/salsak/zeus/frontend",
      env: {
        NODE_ENV: "production"
      }
    },
    {
      name: "backend",
      script: "manage.py",
      args: "runserver 0.0.0.0:8000",
      cwd: "/home/salsak/zeus/backend",
      interpreter: "/home/salsak/zeus/backend/venv/bin/python",
      env: {
        DEBUG: "True",
        PYTHONUNBUFFERED: "1",
        DJANGO_SETTINGS_MODULE: "backend.settings"
      }
    }
  ]
};
