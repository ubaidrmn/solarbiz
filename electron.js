const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
let djangoProcess;

app.on('ready', () => {
  djangoProcess = spawn('python', ['manage.py', 'runserver', '127.0.0.1:8000'], {
    cwd: __dirname + '/src/'
  });

  djangoProcess.stdout.on('data', (data) => {
    console.log(`Django: ${data}`);
  });

  const win = new BrowserWindow({ width: 1200, height: 800 });
  win.loadURL('http://127.0.0.1:8000');
});

app.on('quit', () => {
  if (djangoProcess) djangoProcess.kill();
});
