import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';
import AdmZip from 'adm-zip';

const IAC_DIRECTORY_NAME = 'iac';
const SOURCE_DIRECTORY_NAME = 'src';
const SHARED_DIR_NAME = 'shared';
const SHARED_PYTHON_DIR_NAME = 'python';
const SQLALCHEMY_DIR_NAME = 'sqlalchemy';
const SITE_PACKAGES_DIR_NAMES = ['python', 'lib', 'python3.11', 'site-packages'];

export function adjustLayerDirectory(): void {
  // Obtém o diretório raiz do diretório fonte
  const rootDirectory = path.join(__dirname, '..');
  const iacDirectory = path.join(rootDirectory, IAC_DIRECTORY_NAME);

  console.log(`Root directory: ${rootDirectory}`);
  console.log(`Root directory files: ${fs.readdirSync(rootDirectory)}`);
  console.log(`IaC directory: ${iacDirectory}`);
  console.log(`IaC directory files: ${fs.readdirSync(iacDirectory)}`);

  // Define os diretórios de origem e destino para shared
  const sourceDirectory = path.join(rootDirectory, SOURCE_DIRECTORY_NAME, SHARED_DIR_NAME);
  const destinationDirectory = path.join(iacDirectory, SHARED_DIR_NAME, SHARED_PYTHON_DIR_NAME, SHARED_DIR_NAME);

  // Apaga o diretório de destino se ele existir
  if (fs.existsSync(destinationDirectory)) {
    fs.rmSync(destinationDirectory, { recursive: true, force: true });
  }

  // Cria o diretório de destino
  fs.mkdirSync(destinationDirectory, { recursive: true });

  // Copia o diretório fonte para o diretório de destino
  console.log(`Copying files from ${sourceDirectory} to ${destinationDirectory}`);
  copyFolderSync(sourceDirectory, destinationDirectory);

  // Cria e ajusta o diretório para sqlalchemy
  const sqlalchemySitePackagesDir = path.join(iacDirectory, SQLALCHEMY_DIR_NAME, ...SITE_PACKAGES_DIR_NAMES);

  if (!fs.existsSync(sqlalchemySitePackagesDir)) {
    fs.mkdirSync(sqlalchemySitePackagesDir, { recursive: true });
  }

  // Instala as bibliotecas do requirements.txt e cria o arquivo ZIP
  installRequirementsAndZip(rootDirectory, sqlalchemySitePackagesDir);
}

function copyFolderSync(src: string, dest: string): void {
  fs.mkdirSync(dest, { recursive: true });
  const files = fs.readdirSync(src);

  for (const file of files) {
    const current = fs.lstatSync(path.join(src, file));

    if (current.isDirectory()) {
      copyFolderSync(path.join(src, file), path.join(dest, file));
    } else if (current.isSymbolicLink()) {
      const symlink = fs.readlinkSync(path.join(src, file));
      fs.symlinkSync(symlink, path.join(dest, file));
    } else {
      fs.copyFileSync(path.join(src, file), path.join(dest, file));
    }
  }
}

function installRequirementsAndZip(rootDir: string, sitePackagesDir: string): void {
  const requirementsFile = path.join(rootDir, 'requirements.txt');
  if (!fs.existsSync(requirementsFile)) {
    throw new Error(`requirements.txt not found in ${rootDir}`);
  }

  try {
    const command = `pip install -r ${requirementsFile} --target ${sitePackagesDir}`;
    console.log(`Running command: ${command}`);
    execSync(command, { stdio: 'inherit' });
    console.log(`Successfully installed requirements from ${requirementsFile} to ${sitePackagesDir}`);

    // Cria um novo arquivo ZIP usando adm-zip
    const zip = new AdmZip();

    // Adiciona todos os arquivos do diretório site-packages ao ZIP
    addFolderToZip(sitePackagesDir, zip);

    // Salva o arquivo ZIP
    const tempZipFilePath = path.join(rootDir, 'requirements.zip');
    zip.writeZip(tempZipFilePath);
    console.log(`Created requirements.zip at ${tempZipFilePath}`);

    // Move o arquivo ZIP para o diretório site-packages dentro de iac
    const finalZipFilePath = path.join(sitePackagesDir, 'requirements.zip');
    fs.renameSync(tempZipFilePath, finalZipFilePath);
    console.log(`Moved requirements.zip to ${finalZipFilePath}`);

    // Limpa o diretório site-packages, exceto o arquivo ZIP
    const files = fs.readdirSync(sitePackagesDir);
    for (const file of files) {
      const filePath = path.join(sitePackagesDir, file);
      if (filePath !== finalZipFilePath) {
        fs.rmSync(filePath, { recursive: true, force: true });
      }
    }
    console.log(`Deleted all files in ${sitePackagesDir} except requirements.zip`);
  } catch (error) {
    console.error(`Failed to install requirements: ${error}`);
  }
}

function addFolderToZip(folderPath: string, zip: AdmZip): void {
  const files = fs.readdirSync(folderPath);

  files.forEach(file => {
    const filePath = path.join(folderPath, file);
    const stats = fs.statSync(filePath);

    if (stats.isDirectory()) {
      addFolderToZip(filePath, zip);
    } else {
      zip.addLocalFile(filePath);
    }
  });
}

if (require.main === module) {
  adjustLayerDirectory();
}
