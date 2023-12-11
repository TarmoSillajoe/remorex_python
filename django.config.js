module.exports = {
  apps: [
    {
      name: "remorex",
      cwd: process.env.HOME + "domeenid/www.remoreks.ee/remorex_python",
      script: process.env.HOME + "/virtualenv/bin/gunicorn/gunicorn",
      args: "remorex.wsgi:application",
      interpreter: process.env.HOME + "/virtualenv/bin/python3.8",
      max_memory_restart: "128M",
    },
  ],
};
