const { app, BrowserWindow, ipcMain, dialog } = require('electron');
app.commandLine.appendSwitch('disable-web-security');
const fs = require('fs');
const path = require('path');
const excel = require('exceljs'); // Make sure to install the 'exceljs' library using npm

let mainWindow;

app.on('ready', () => {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 702,
    webPreferences: {
      nodeIntegration: true, // Enable Node.js integration
      contextIsolation: false, // Disable context isolation
      preload: path.join(__dirname, 'preload.js'), // Path to your preload script
    },
  });

  mainWindow.loadFile('main_layout.html');

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
});

ipcMain.on('open-manage-patients', () => {
  mainWindow.loadFile('manage_patients.html');
});

ipcMain.on('open-add-patient', () => {
  mainWindow.loadFile('add_patient.html');
});

ipcMain.on('open-run-ml', () => {
  mainWindow.loadFile('run_ml.html');
});

ipcMain.on('submit-form', (event, formData) => {
  const { name, ownerName,phone, email,breed,yearOfBirth,neutered } = formData;

  // Create a directory in the 'patient_data' folder based on name and phone
  const patientDirectory = path.join(__dirname, 'patient_data', `${name}_${phone}`);
  fs.mkdirSync(patientDirectory, { recursive: true });

  // Create an Excel file and add patient information
  const workbook = new excel.Workbook();
  const worksheet = workbook.addWorksheet('Patient Info');
  worksheet.addRow(['Name', 'Owner','Phone', 'Email','Breed','Year of Birth','Neutered']);
  worksheet.addRow([name,ownerName, phone, email,breed,yearOfBirth,neutered]);

  const excelFilePath = path.join(patientDirectory, 'patient_info.xlsx');
  workbook.xlsx.writeFile(excelFilePath).then(() => {
    dialog.showMessageBox({ message: 'Patient information saved!' });
  });
});


app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});
